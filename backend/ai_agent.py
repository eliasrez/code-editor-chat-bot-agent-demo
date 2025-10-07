# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "anthropic",
#     "pydantic",
# ]
# ///

import os
import logging
from typing import List, Dict, Any
from anthropic import Anthropic  # type: ignore
from pydantic import BaseModel  # type: ignore

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    handlers=[logging.FileHandler("agent.log")],
)

# Suppress verbose HTTP logs
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)


class Tool(BaseModel):
    name: str
    description: str
    input_schema: Dict[str, Any]


class AIAgent:
    """
    A conversational AI agent that uses the Anthropic API and provides
    file editing capabilities via tools.
    """
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
        self.messages: List[Dict[str, Any]] = []
        self.tools: List[Tool] = []
        self._setup_tools()

    def _setup_tools(self):
        """Defines the tools available to the AI agent."""
        self.tools = [
            Tool(
                name="read_file",
                description="Read the contents of a file at the specified path",
                input_schema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path to the file to read",
                        }
                    },
                    "required": ["path"],
                },
            ),
            Tool(
                name="list_files",
                description="List all files and directories in the specified path",
                input_schema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The directory path to list (defaults to current directory)",
                        }
                    },
                    "required": [],
                },
            ),
            Tool(
                name="edit_file",
                description="Edit a file by replacing old_text with new_text. Creates the file if it doesn't exist.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path to the file to edit",
                        },
                        "old_text": {
                            "type": "string",
                            "description": "The text to search for and replace (leave empty to create new file)",
                        },
                        "new_text": {
                            "type": "string",
                            "description": "The text to replace old_text with",
                        },
                    },
                    "required": ["path", "new_text"],
                },
            ),
        ]

    def _execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> str:
        """Executes a defined tool and returns the result."""
        logging.info(f"Executing tool: {tool_name} with input: {tool_input}")
        try:
            if tool_name == "read_file":
                return self._read_file(tool_input["path"])
            elif tool_name == "list_files":
                return self._list_files(tool_input.get("path", "."))
            elif tool_name == "edit_file":
                return self._edit_file(
                    tool_input["path"],
                    tool_input.get("old_text", ""),
                    tool_input["new_text"],
                )
            else:
                return f"Unknown tool: {tool_name}"
        except Exception as e:
            logging.error(f"Error executing {tool_name}: {str(e)}")
            return f"Error executing {tool_name}: {str(e)}"

    def _read_file(self, path: str) -> str:
        """Helper to read file content."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            return f"File contents of {path}:\n{content}"
        except FileNotFoundError:
            return f"File not found: {path}"
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def _list_files(self, path: str) -> str:
        """Helper to list directory contents."""
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
        """Helper to edit or create a file."""
        try:
            if os.path.exists(path) and old_text:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()

                if old_text not in content:
                    return f"Text not found in file: {old_text}"

                content = content.replace(old_text, new_text)

                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)

                return f"Successfully edited {path}"
            else:
                # Only create directory if path contains subdirectories
                dir_name = os.path.dirname(path)
                if dir_name:
                    os.makedirs(dir_name, exist_ok=True)

                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_text)

                return f"Successfully created {path}"
        except Exception as e:
            return f"Error editing file: {str(e)}"

    def chat(self, user_input: str) -> str:
        """Sends a message to the Claude model, handling tool use."""
        logging.info(f"User input: {user_input}")
        self.messages.append({"role": "user", "content": user_input})

        tool_schemas = [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.input_schema,
            }
            for tool in self.tools
        ]

        while True:
            try:
                # API Call to Claude
                response = self.client.messages.create(
                    model="claude-sonnet-4-5-20250929",
                    max_tokens=4096,
                    system="You are a helpful coding assistant operating in a terminal environment. Output only plain text without markdown formatting, as your responses appear directly in the terminal. Be concise but thorough, providing clear and practical advice with a friendly tone. Don't use any asterisk characters in your responses.",
                    messages=self.messages,
                    tools=tool_schemas,
                )

                assistant_message = {"role": "assistant", "content": []}
                tool_results = []
                
                # Process response and collect tool calls
                for content in response.content:
                    if content.type == "text":
                        assistant_message["content"].append(
                            {"type": "text", "text": content.text}
                        )
                    elif content.type == "tool_use":
                        assistant_message["content"].append(
                            {
                                "type": "tool_use",
                                "id": content.id,
                                "name": content.name,
                                "input": content.input,
                            }
                        )
                        print(f"using tool:", content.name, content.input) # Log to stdout for CLI visibility
                        
                        # Execute tool
                        result = self._execute_tool(content.name, content.input)
                        logging.info(
                            f"Tool result: {result[:500]}..."
                        )  # Log first 500 chars
                        
                        # Prepare tool result for next API call
                        tool_results.append(
                            {
                                "type": "tool_result",
                                "tool_use_id": content.id,
                                "content": result,
                            }
                        )

                self.messages.append(assistant_message)

                if tool_results:
                    # If tools were used, append results and loop for another Claude call
                    self.messages.append({"role": "user", "content": tool_results})
                else:
                    # If no tools were used, return the text response
                    return response.content[0].text if response.content else ""

            except Exception as e:
                return f"Error: {str(e)}"