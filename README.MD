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
- uv package manager (see installation instructions below)
- Anthropic API key

## Installing uv

`uv` is an extremely fast Python package manager that simplifies running Python scripts with inline dependencies.

It allows you to run Python scripts [without needing to create a virtual environment or manually install dependencies](https://docs.astral.sh/uv/guides/scripts/#declaring-script-dependencies).

To [install](https://docs.astral.sh/uv/getting-started/installation/) `uv`::

### Linux/macOS

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

After installation, verify it's working:

```bash
uv --version
```

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

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

This code is based on the tutorial by Thorsten Ball in ["How to Build an Agent"](https://ampcode.com/how-to-build-an-agent) from ampcode.com.

Thank you, Thorsten. Brilliant guide, though I'll need a long detox after all that Go syntax!
