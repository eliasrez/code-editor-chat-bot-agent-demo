# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "anthropic", # type: ignore
#     "pydantic",
# ]
# ///

import os
import sys
import argparse
import logging
from typing import List, Dict, Any
from anthropic import Anthropic
from pydantic import BaseModel

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('agent.log')
    ]
)

# Suppress verbose HTTP logs
logging.getLogger('httpcore').setLevel(logging.WARNING)
logging.getLogger('httpx').setLevel(logging.WARNING)


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
        print(f"Agent initialized with {len(self.tools)} tools")


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


    def _execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> str:  # NEW
        try:                                                                     # NEW
            if tool_name == "read_file":                                         # NEW
                return self._read_file(tool_input["path"])                       # NEW
            elif tool_name == "list_files":                                      # NEW
                return self._list_files(tool_input.get("path", "."))             # NEW
            elif tool_name == "edit_file":                                       # NEW
                return self._edit_file(                                          # NEW
                    tool_input["path"],                                          # NEW
                    tool_input.get("old_text", ""),                              # NEW
                    tool_input["new_text"]                                       # NEW
                )                                                                # NEW
            else:                                                                # NEW
                return f"Unknown tool: {tool_name}"                              # NEW
        except Exception as e:                                                   # NEW
            return f"Error executing {tool_name}: {str(e)}"                      # NEW


    def _read_file(self, path: str) -> str:                                      # NEW
        try:                                                                     # NEW
            with open(path, 'r', encoding='utf-8') as f:                         # NEW
                content = f.read()                                               # NEW
            return f"File contents of {path}:\n{content}"                        # NEW
        except FileNotFoundError:                                                # NEW
            return f"File not found: {path}"                                     # NEW
        except Exception as e:                                                   # NEW
            return f"Error reading file: {str(e)}"                               # NEW
    

    def _list_files(self, path: str) -> str:                                     # NEW
        try:                                                                     # NEW
            if not os.path.exists(path):                                         # NEW
                return f"Path not found: {path}"                                 # NEW

            items = []                                                           # NEW
            for item in sorted(os.listdir(path)):                                # NEW
                item_path = os.path.join(path, item)                             # NEW
                if os.path.isdir(item_path):                                     # NEW
                    items.append(f"[DIR]  {item}/")                              # NEW
                else:                                                            # NEW
                    items.append(f"[FILE] {item}")                               # NEW

            if not items:                                                        # NEW
                return f"Empty directory: {path}"                                # NEW
            
            return f"Contents of {path}:\n" + "\n".join(items)                   # NEW
        except Exception as e:                                                   # NEW
            return f"Error listing files: {str(e)}"                              # NEW
    

    def _edit_file(self, path: str, old_text: str, new_text: str) -> str:          # NEW
        try:                                                                       # NEW
            if os.path.exists(path) and old_text:                                  # NEW
                with open(path, 'r', encoding='utf-8') as f:                       # NEW
                    content = f.read()                                             # NEW
                
                if old_text not in content:                                        # NEW
                    return f"Text not found in file: {old_text}"                   # NEW
                
                content = content.replace(old_text, new_text)                      # NEW
                
                with open(path, 'w', encoding='utf-8') as f:                       # NEW
                    f.write(content)                                               # NEW
                
                return f"Successfully edited {path}"                               # NEW
            else:                                                                  # NEW
                # Only create directory if path contains subdirectories            # NEW
                dir_name = os.path.dirname(path)                                   # NEW
                if dir_name:                                                       # NEW
                    os.makedirs(dir_name, exist_ok=True)                           # NEW
                
                with open(path, 'w', encoding='utf-8') as f:                       # NEW
                    f.write(new_text)                                              # NEW
                
                return f"Successfully created {path}"                              # NEW
        except Exception as e:                                                     # NEW
            return f"Error editing file: {str(e)}"                                 # NEW


if __name__ == "__main__":
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set")
        sys.exit(1)
    agent = AIAgent(api_key)
    # Test the tools                                                               # NEW
    print(agent._list_files("."))                                                  # NEW

# ```bash
# export ANTHROPIC_API_KEY="your-api
# uv run --python python3.12 runbook/04_implement_tool_execution.py
# ```
# Should print: 
# Agent initialized with 3 tools
# Contents of .:
# [FILE] main.py
# ... (other files in directory)
