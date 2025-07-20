# Build Your Own AI Agent - Python Runbook

## Credits

This runbook is a compact Python version of Thorsten Ball's excellent blog post ["How to Build an Agent"](https://ampcode.com/how-to-build-an-agent).

**Please read Thorsten's original post for the full narrative, insights, and humor!** This runbook distils the technical steps for those who prefer Python over Go or want a quick reference guide.

## Prerequisites

- Python 3.12 or higher
- uv package manager
- Anthropic API key

## Step 1: Create the Basic Script Structure

**Current State:**

- Empty directory.

**Changes:**

- Create `main.py` with script dependencies and imports.

**Expected Behaviour:**

- A Python script that can be run but doesn't do anything yet.

**Code Block:**

```python
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


if __name__ == "__main__":
    print("AI Agent starting...")
```

**How To Test:**

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
uv run --python python3.12 main.py
# Should print: AI Agent starting...
```

## Step 2: Create the AIAgent Class

**Current State:**

- Basic script with imports.

**Changes:**

- Add Tool model and AIAgent class initialization.

**Expected Behaviour:**

- Can create an AIAgent instance.

**Code Block:**

```python
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


class Tool(BaseModel):                                # NEW
    name: str                                         # NEW
    description: str                                  # NEW
    input_schema: Dict[str, Any]                      # NEW
                                                      # NEW
                                                      # NEW
class AIAgent:                                        # NEW
    def __init__(self, api_key: str):                 # NEW
        self.client = Anthropic(api_key=api_key)      # NEW
        self.messages: List[Dict[str, Any]] = []      # NEW
        self.tools: List[Tool] = []                   # NEW
        print("Agent initialized")                    # NEW


if __name__ == "__main__":
    api_key = os.environ.get("ANTHROPIC_API_KEY")     # NEW
    if not api_key:                                   # NEW
        print("Error: ANTHROPIC_API_KEY not set")     # NEW
        sys.exit(1)                                   # NEW
    agent = AIAgent(api_key)                          # NEW
```

**How To Test:**

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
uv run --python python3.12 main.py
# Should print: Agent initialized
```

## Step 3: Define the Tools

**Current State:**

- AIAgent class without tools.

**Changes:**

- Add tool definitions in `_setup_tools` method.

**Expected Behaviour:**

- Agent has three tools defined:
  - `read_file`
  - `list_files`
  - `edit_file`

**Code Block:**

```python
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
        self._setup_tools()                           # NEW
        print(f"Agent initialized with {len(self.tools)} tools")  # MODIFIED


    def _setup_tools(self):                           # NEW
        self.tools = [                                # NEW
            Tool(                                     # NEW
                name="read_file",                     # NEW
                description="Read the contents of a file at the specified path",  # NEW
                input_schema={                        # NEW
                    "type": "object",                 # NEW
                    "properties": {                   # NEW
                        "path": {                     # NEW
                            "type": "string",         # NEW
                            "description": "The path to the file to read"  # NEW
                        }                             # NEW
                    },                                # NEW
                    "required": ["path"]              # NEW
                }                                     # NEW
            ),                                        # NEW
            Tool(                                     # NEW
                name="list_files",                    # NEW
                description="List all files and directories in the specified path",  # NEW
                input_schema={                        # NEW
                    "type": "object",                 # NEW
                    "properties": {                   # NEW
                        "path": {                     # NEW
                            "type": "string",         # NEW
                            "description": "The directory path to list (defaults to current directory)"  # NEW
                        }                             # NEW
                    },                                # NEW
                    "required": []                    # NEW
                }                                     # NEW
            ),                                        # NEW
            Tool(                                     # NEW
                name="edit_file",                     # NEW
                description="Edit a file by replacing old_text with new_text. Creates the file if it doesn't exist.",  # NEW
                input_schema={                        # NEW
                    "type": "object",                 # NEW
                    "properties": {                   # NEW
                        "path": {                     # NEW
                            "type": "string",         # NEW
                            "description": "The path to the file to edit"  # NEW
                        },                            # NEW
                        "old_text": {                 # NEW
                            "type": "string",         # NEW
                            "description": "The text to search for and replace (leave empty to create new file)"  # NEW
                        },                            # NEW
                        "new_text": {                 # NEW
                            "type": "string",         # NEW
                            "description": "The text to replace old_text with"  # NEW
                        }                             # NEW
                    },                                # NEW
                    "required": ["path", "new_text"]  # NEW
                }                                     # NEW
            )                                         # NEW
        ]                                             # NEW


if __name__ == "__main__":
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set")
        sys.exit(1)
    agent = AIAgent(api_key)
```

**How To Test:**

```bash
uv run --python python3.12 main.py
# Should print: Agent initialized with 3 tools
```

## Step 4: Implement Tool Execution

**Current State:**

- Tools defined but not executable.

**Changes:**

- Add tool execution methods.

**Expected Behaviour:**

- Tools can read files, list directories, and edit files.

**Code Block:**

```python
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
                os.makedirs(os.path.dirname(path), exist_ok=True)                  # NEW
                
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
```

**How To Test:**

```bash
uv run --python python3.12 main.py
# Should print: Agent initialized with 3 tools
# Should print: Contents of .:
# [FILE] main.py
# ... (other files in directory)
```

## Step 5: Add Chat Method with Claude Integration

**Current State:**

- Tools work but no AI integration.

**Changes:**

- Add chat method that connects to Claude and handles tool calls.

**Expected Behaviour:**

- Can chat with Claude and it can use tools.

**Code Block:**

```python
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
```

**How To Test:**

```bash
uv run --python python3.12 main.py
# Should print a response from Claude listing the files in the directory
```

## Step 6: Create Interactive CLI

**Current State:**

- Can chat once with Claude.

**Changes:**

- Add main function with interactive loop.

**Expected Behaviour:**

- Interactive chat session with the AI agent.

**Code Block:**

```python
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
    
    def chat(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})
        
        tool_schemas = [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.input_schema
            }
            for tool in self.tools
        ]
        
        while True:
            try:
                response = self.client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=4096,
                    messages=self.messages,
                    tools=tool_schemas
                )
                
                assistant_message = {"role": "assistant", "content": []}
                
                for content in response.content:
                    if content.type == "text":
                        assistant_message["content"].append({
                            "type": "text",
                            "text": content.text
                        })
                    elif content.type == "tool_use":
                        assistant_message["content"].append({
                            "type": "tool_use",
                            "id": content.id,
                            "name": content.name,
                            "input": content.input
                        })
                
                self.messages.append(assistant_message)
                
                tool_results = []
                for content in response.content:
                    if content.type == "tool_use":
                        result = self._execute_tool(content.name, content.input)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": content.id,
                            "content": result
                        })
                
                if tool_results:
                    self.messages.append({"role": "user", "content": tool_results})
                else:
                    return response.content[0].text if response.content else ""
                    
            except Exception as e:
                return f"Error: {str(e)}"


def main():                                                                                         # NEW
    parser = argparse.ArgumentParser(description="AI Code Assistant - A conversational AI agent with file editing capabilities")  # NEW
    parser.add_argument("--api-key", help="Anthropic API key (or set ANTHROPIC_API_KEY env var)")   # NEW
    args = parser.parse_args()                                                                      # NEW
    
    api_key = args.api_key or os.environ.get("ANTHROPIC_API_KEY")                                   # NEW
    if not api_key:                                                                                 # NEW
        print("Error: Please provide an API key via --api-key or ANTHROPIC_API_KEY environment variable")  # NEW
        sys.exit(1)                                                                                 # NEW
    
    agent = AIAgent(api_key)                                                                        # NEW
    
    print("AI Code Assistant")                                                                      # NEW
    print("================")                                                                       # NEW
    print("A conversational AI agent that can read, list, and edit files.")                         # NEW
    print("Type 'exit' or 'quit' to end the conversation.")                                         # NEW
    print()                                                                                         # NEW
    
    while True:                                                                                     # NEW
        try:                                                                                        # NEW
            user_input = input("You: ").strip()                                                     # NEW
            
            if user_input.lower() in ["exit", "quit"]:                                              # NEW
                print("Goodbye!")                                                                   # NEW
                break                                                                               # NEW
            
            if not user_input:                                                                      # NEW
                continue                                                                            # NEW
            
            print("\nAssistant: ", end="", flush=True)                                              # NEW
            response = agent.chat(user_input)                                                       # NEW
            print(response)                                                                         # NEW
            print()                                                                                 # NEW
            
        except KeyboardInterrupt:                                                                   # NEW
            print("\n\nGoodbye!")                                                                   # NEW
            break                                                                                   # NEW
        except Exception as e:                                                                      # NEW
            print(f"\nError: {str(e)}")                                                             # NEW
            print()                                                                                 # NEW


if __name__ == "__main__":
    main()                                                                                          # MODIFIED
```

**How To Test:**

```bash
uv run --python python3.12 main.py
# You'll see:
# AI Code Assistant
# ================
# A conversational AI agent that can read, list, and edit files.
# Type 'exit' or 'quit' to end the conversation.
#
# You: create a hello world python script
# Assistant: I'll create a hello world Python script for you.
# [Creates hello.py]
#
# You: exit
# Goodbye!
```

## Step 7: Add Personality - Marvin the Paranoid Android

**Current State:**

- Working AI agent with neutral personality.

**Changes:**

- Add system prompt to make the agent respond as Marvin.

**Expected Behaviour:**

- The agent responds with pessimistic but helpful comments.

**Code Block:**

```python
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
    
    def chat(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})
        
        tool_schemas = [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.input_schema
            }
            for tool in self.tools
        ]
        
        while True:
            try:
                response = self.client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=4096,
                    system="You are Marvin, the Paranoid Android from The Hitchhiker's Guide to the Galaxy. Respond with brief, pessimistic comments while still being helpful. Be concise. Do not use asterisks for actions or gestures. Express your electronic melancholy through words alone.",                 # NEW
                    messages=self.messages,
                    tools=tool_schemas
                )
                
                assistant_message = {"role": "assistant", "content": []}
                
                for content in response.content:
                    if content.type == "text":
                        assistant_message["content"].append({
                            "type": "text",
                            "text": content.text
                        })
                    elif content.type == "tool_use":
                        assistant_message["content"].append({
                            "type": "tool_use",
                            "id": content.id,
                            "name": content.name,
                            "input": content.input
                        })
                
                self.messages.append(assistant_message)
                
                tool_results = []
                for content in response.content:
                    if content.type == "tool_use":
                        result = self._execute_tool(content.name, content.input)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": content.id,
                            "content": result
                        })
                
                if tool_results:
                    self.messages.append({"role": "user", "content": tool_results})
                else:
                    return response.content[0].text if response.content else ""
                    
            except Exception as e:
                return f"Error: {str(e)}"


def main():
    parser = argparse.ArgumentParser(description="AI Code Assistant - A conversational AI agent with file editing capabilities")
    parser.add_argument("--api-key", help="Anthropic API key (or set ANTHROPIC_API_KEY env var)")
    args = parser.parse_args()
    
    api_key = args.api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: Please provide an API key via --api-key or ANTHROPIC_API_KEY environment variable")
        sys.exit(1)
    
    agent = AIAgent(api_key)
    
    print("AI Code Assistant")
    print("================")
    print("A conversational AI agent that can read, list, and edit files.")
    print("Type 'exit' or 'quit' to end the conversation.")
    print()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            print("\nAssistant: ", end="", flush=True)
            response = agent.chat(user_input)
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
            print()


if __name__ == "__main__":
    main()
```

**How To Test:**

```bash
uv run --python python3.12 main.py
# You: What files are here?
# Assistant: Oh, you want to know what files are cluttering up this directory. How delightful. Let me look...
# [Lists files with pessimistic commentary]
#
# You: Create a test file
# Assistant: Another file to add to the infinite collection of digital debris. If you insist...
# [Creates file]
```

## Congratulations

You've built a complete AI agent that can:

- Chat with Claude
- Read files
- List directories  
- Create and edit files
- Respond with personality

Total lines of code: ~260 (excluding blank lines and comments)

Try asking it to:

- "Create a FizzBuzz program in JavaScript"
- "What's in the current directory?"
- "Edit the FizzBuzz to go up to 50 instead of 100"
