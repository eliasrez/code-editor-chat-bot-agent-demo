# CLI vs Web UI Comparison

Both versions use the same AI agent core, but offer different user experiences.

## CLI Version (main.py)

### Pros
- **Lightweight**: Single Python file, no frontend dependencies
- **Fast startup**: Runs immediately with `uv run main.py`
- **Simple**: Just text input/output
- **Terminal native**: Great for SSH sessions, scripts, automation
- **Low resource usage**: Minimal memory footprint

### Cons
- No visual file browser
- No syntax highlighting
- Can't see multiple things at once
- Less intuitive for beginners
- No persistent UI state

### Best For
- Quick file operations
- Automated scripts
- Remote server work
- Developers comfortable with CLI
- Low-resource environments

### Usage
```bash
export ANTHROPIC_API_KEY="your-key"
uv run main.py
```

## Web UI Version (api.py + frontend/)

### Pros
- **Visual interface**: See file tree, code, and chat simultaneously
- **Syntax highlighting**: Beautiful code display with 20+ languages
- **Better UX**: Click files, resize panels, modern design
- **Easier for beginners**: More discoverable features
- **Rich formatting**: Markdown rendering, code blocks
- **Persistent view**: Keep multiple files open

### Cons
- More complex setup (backend + frontend)
- Higher resource usage (~100MB+ RAM)
- Requires Node.js and npm
- Slightly slower startup
- More moving parts to debug

### Best For
- Interactive development
- Learning and exploration
- Multi-file work
- Teams (easier to demo)
- Users who prefer GUIs

### Usage
```bash
export ANTHROPIC_API_KEY="your-key"
./start-web.sh  # or start-web.bat on Windows
```

## Feature Comparison

| Feature | CLI | Web UI |
|---------|-----|--------|
| File reading | ✅ | ✅ |
| File editing | ✅ | ✅ |
| File creation | ✅ | ✅ |
| Syntax highlighting | ❌ | ✅ |
| File browser | ❌ | ✅ |
| Visual code viewer | ❌ | ✅ |
| Split panels | ❌ | ✅ |
| Markdown rendering | ❌ | ✅ |
| Session persistence | ✅ | ✅ |
| Conversation history | ✅ | ✅ |
| Startup time | < 1s | ~3s |
| Memory usage | ~50MB | ~150MB |
| Setup complexity | Low | Medium |
| Cross-platform | ✅ | ✅ |

## Technical Differences

### Architecture

**CLI:**
```
User Input → AIAgent → Claude API → Tool Execution → Response
```

**Web UI:**
```
Browser → FastAPI → AIAgent → Claude API → Tool Execution → FastAPI → Browser
                                                                    ↓
                                                              React Components
```

### Code Reuse

The Web UI **reuses** the CLI's core:
- Same `AIAgent` class from `main.py`
- Same tool definitions
- Same execution logic
- FastAPI just wraps it with HTTP endpoints

### Files Involved

**CLI Only:**
- `main.py` (218 lines)

**Web UI:**
- `api.py` (Backend wrapper)
- `frontend/` (React application)
  - Components: ChatPanel, FileExplorer, FileViewer
  - ~500 lines of JSX/CSS total

## When to Use Each

### Use CLI if you:
- Want minimal setup
- Are working over SSH
- Need to script/automate
- Prefer terminal workflows
- Have limited resources
- Want the simplest option

### Use Web UI if you:
- Want a visual interface
- Are new to AI agents
- Work with many files
- Need syntax highlighting
- Want to demo to others
- Prefer modern UX

## Can I Use Both?

**Yes!** They can coexist:

1. Both use the same agent logic
2. They don't interfere with each other
3. You can switch based on your task
4. Same API key works for both

Example workflow:
- Use CLI for quick one-off edits
- Use Web UI for exploratory work and complex tasks

## Migration Path

### From CLI to Web:
No changes needed - just install frontend and run both!

### From Web to CLI:
Your agent logic is in `main.py` - works standalone

## Performance Considerations

### CLI
- Near-instant startup
- Low memory (single Python process)
- No network overhead
- Direct tool execution

### Web UI
- 2-3 second startup (both servers)
- Higher memory (Python + Node.js)
- Localhost HTTP (minimal overhead)
- Same tool execution speed

For the actual AI responses and tool execution, **performance is identical** since they use the same core agent.

## Conclusion

Both are valid choices:

- **CLI**: Traditional, efficient, simple
- **Web UI**: Modern, visual, user-friendly

Choose based on your preferences and use case. The beauty of this setup is you don't have to choose - you can use both!
