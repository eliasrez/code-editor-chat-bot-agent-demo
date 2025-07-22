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
import logging                                        # NEW
from typing import List, Dict, Any
from anthropic import Anthropic
from pydantic import BaseModel

# Set up logging                                      # NEW
logging.basicConfig(                                  # NEW
    level=logging.INFO,                               # NEW
    format='%(asctime)s - %(message)s',               # NEW
    handlers=[                                        # NEW
        logging.FileHandler('agent.log')              # NEW
    ]                                                 # NEW
)                                                     # NEW
                                                      # NEW
# Suppress verbose HTTP logs                          # NEW
logging.getLogger('httpcore').setLevel(logging.WARNING)  # NEW
logging.getLogger('httpx').setLevel(logging.WARNING)     # NEW


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

# ```bash
# export ANTHROPIC_API_KEY="your-api-key-here"
# uv run --python python3.12 runbook/02_agent_class.py
# ```
# Should print: Agent initialized
