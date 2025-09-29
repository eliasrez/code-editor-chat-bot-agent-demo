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
from anthropic import Anthropic  # type: ignore
from pydantic import BaseModel


if __name__ == "__main__":
    print("AI Agent starting...")

# ```bash
# export ANTHROPIC_API_KEY="your-api-key-here"
# uv run runbook/01_basic_script.py
# ```
# Should print: AI Agent starting...
