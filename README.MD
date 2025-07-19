# AI Code Assistant

A conversational AI agent powered by Claude that can read, list, and edit files in your system. The agent provides a simple chat interface where you can interact with files through natural language commands.

## Features

- Read file contents
- List directory contents
- Edit existing files or create new ones
- Interactive chat interface
- Error handling and feedback

## Requirements

- Python 3.12 or higher
- uv package manager
- Anthropic API key

## Running the Agent

1. Export your Anthropic API key:

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

2. Run the agent:

```bash
uv run --python python3.12 main.py
```

The agent leverages uv's inline dependencies handling from the script headers, so no manual dependency installation is needed.

## Credits

This code is based on the tutorial by Thorsten Ball in ["How to Build an Agent"](https://ampcode.com/how-to-build-an-agent) from ampcode.com.

Thank you, Thorsten. Brilliant guide, though I'll need a long detox after all that Go syntax!
