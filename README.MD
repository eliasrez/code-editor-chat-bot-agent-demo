# Ai Code Assistant demo

This is a AI code assistant agent built in python.
The idea is to demonstrate how to use a generative AI (i.e Anthropic) for help with code generation, debugging while extending the agent with some file editing tools allowing it to create, delete, list, read and edit files.
The AI agent will know when it needs to use the tools and use them in order to act on our project files.

## Credits

The code is based on the tutorial by Thorsten Ball in ["How to Build an Agent"](https://ampcode.com/how-to-build-an-agent) from ampcode.com. Thank you, Thorsten. Brilliant guide.

## Features

- Single-file execution.
- No virtual environment or manual dependency installation required (except for `uv`).
- The AI agent can:
  - Read file contents.
  - List directory contents.
  - Edit existing files or create new ones.
- Interactive chat interface.
- Error handling and feedback.
- Logging of agent tool usage.

## Requirements

- `uv` package manager (see installation instructions below)
- Python 3.12 or higher (though `uv` will [handle this automatically](https://docs.astral.sh/uv/concepts/python-versions/))
- Anthropic API key (you can get one from [Anthropic's Console](https://console.anthropic.com/settings/keys))

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

## option 1:  Running the Agent API and FrontEnd locally
```
cd backend
uv run api.py
```

``` 
cd frontend
npm run dev
```




## option 2: Running the Agent in CLI Mode

1. Export your Anthropic API key:

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

2. Run the agent in CLI Mode:

```bash
uv run main.py
```


## option 3: Running the Agent API and frontend inside docker
```
docker-compose up
```



## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
