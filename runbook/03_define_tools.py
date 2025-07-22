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


# ```bash
# export ANTHROPIC_API_KEY="your-api
# uv run --python python3.12 runbook/03_define_tools.py
# ```
# Should print: Agent initialized with 3 tools
