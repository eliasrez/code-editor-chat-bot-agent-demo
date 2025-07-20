# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "anthropic",
#     "pydantic",
# ]
# ///

import os
import sys
import argparse
from typing import List, Dict, Any
from anthropic import Anthropic
from pydantic import BaseModel


class Tool(BaseModel):
    name: str
    description: str
    input_schema: Dict[str, Any]
    

class AIAgent:
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
        self.messages: List[Dict[str, Any]] = []
        self.tools: List[Tool] = []
        self._setup_tools()
        # REMOVED: print(f"Agent initialized with {len(self.tools)} tools")
    
    def _setup_tools(self):
        self.tools = [
            Tool(
                name="read_file",
                description="Read the contents of a file at the specified path",
                input_schema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path to the file to read"
                        }
                    },
                    "required": ["path"]
                }
            ),
            Tool(
                name="list_files",
                description="List all files and directories in the specified path",
                input_schema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The directory path to list (defaults to current directory)"
                        }
                    },
                    "required": []
                }
            ),
            Tool(
                name="edit_file",
                description="Edit a file by replacing old_text with new_text. Creates the file if it doesn't exist.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path to the file to edit"
                        },
                        "old_text": {
                            "type": "string",
                            "description": "The text to search for and replace (leave empty to create new file)"
                        },
                        "new_text": {
                            "type": "string",
                            "description": "The text to replace old_text with"
                        }
                    },
                    "required": ["path", "new_text"]
                }
            )
        ]
    
    def _execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> str:
        try:
            if tool_name == "read_file":
                return self._read_file(tool_input["path"])
            elif tool_name == "list_files":
                return self._list_files(tool_input.get("path", "."))
            elif tool_name == "edit_file":
                return self._edit_file(
                    tool_input["path"],
                    tool_input.get("old_text", ""),
                    tool_input["new_text"]
                )
            else:
                return f"Unknown tool: {tool_name}"
        except Exception as e:
            return f"Error executing {tool_name}: {str(e)}"
    
    def _read_file(self, path: str) -> str:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            return f"File contents of {path}:\n{content}"
        except FileNotFoundError:
            return f"File not found: {path}"
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def _list_files(self, path: str) -> str:
        try:
            if not os.path.exists(path):
                return f"Path not found: {path}"
            
            items = []
            for item in sorted(os.listdir(path)):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    items.append(f"[DIR]  {item}/")
                else:
                    items.append(f"[FILE] {item}")
            
            if not items:
                return f"Empty directory: {path}"
            
            return f"Contents of {path}:\n" + "\n".join(items)
        except Exception as e:
            return f"Error listing files: {str(e)}"
    
    def _edit_file(self, path: str, old_text: str, new_text: str) -> str:
        try:
            if os.path.exists(path) and old_text:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if old_text not in content:
                    return f"Text not found in file: {old_text}"
                
                content = content.replace(old_text, new_text)
                
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                return f"Successfully edited {path}"
            else:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_text)
                
                return f"Successfully created {path}"
        except Exception as e:
            return f"Error editing file: {str(e)}"
    
    def chat(self, user_input: str) -> str:                             # NEW
        self.messages.append({"role": "user", "content": user_input})   # NEW
        
        tool_schemas = [                                                # NEW
            {                                                           # NEW
                "name": tool.name,                                      # NEW
                "description": tool.description,                        # NEW
                "input_schema": tool.input_schema                       # NEW
            }                                                           # NEW
            for tool in self.tools                                      # NEW
        ]                                                               # NEW
        
        while True:                                                     # NEW
            try:                                                        # NEW
                response = self.client.messages.create(                 # NEW
                    model="claude-sonnet-4-20250514",                 # NEW
                    max_tokens=4096,                                    # NEW
                    messages=self.messages,                             # NEW
                    tools=tool_schemas                                  # NEW
                )                                                       # NEW
                
                assistant_message = {"role": "assistant", "content": []}# NEW
                
                for content in response.content:                        # NEW
                    if content.type == "text":                          # NEW
                        assistant_message["content"].append({           # NEW
                            "type": "text",                             # NEW
                            "text": content.text                        # NEW
                        })                                              # NEW
                    elif content.type == "tool_use":                    # NEW
                        assistant_message["content"].append({           # NEW
                            "type": "tool_use",                         # NEW
                            "id": content.id,                           # NEW
                            "name": content.name,                       # NEW
                            "input": content.input                      # NEW
                        })                                              # NEW
                
                self.messages.append(assistant_message)                 # NEW
                
                tool_results = []                                       # NEW
                for content in response.content:                        # NEW
                    if content.type == "tool_use":                      # NEW
                        result = self._execute_tool(content.name, content.input)  # NEW
                        tool_results.append({                           # NEW
                            "type": "tool_result",                      # NEW
                            "tool_use_id": content.id,                  # NEW
                            "content": result                           # NEW
                        })                                              # NEW

                if tool_results:                                        # NEW
                    self.messages.append({"role": "user", "content": tool_results})  # NEW
                else:                                                   # NEW
                    return response.content[0].text if response.content else ""  # NEW
                    
            except Exception as e:                                      # NEW
                return f"Error: {str(e)}"                               # NEW


if __name__ == "__main__":
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set")
        sys.exit(1)
    agent = AIAgent(api_key)
    # Test chat                                                         # NEW
    response = agent.chat("What files are in the current directory?")   # NEW
    print(response)                                                     # NEW

# ```bash
# export ANTHROPIC_API_KEY="your-api
# uv run --python python3.12 runbook/05_add_chat_method.py
# ```
# Should print a response from Claude listing the files in the directory
