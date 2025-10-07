# AI Code Assistant - Web Application

A modern web interface for the AI Code Assistant with real-time chat, file explorer, and code viewer.

## Features

- **Interactive Chat Interface**: Conversational AI that can read, edit, and create files
- **File Explorer**: Browse your project structure in a sidebar
- **Code Viewer**: Syntax-highlighted file viewer with 20+ language support
- **Resizable Panels**: Drag to resize the file explorer
- **Dark Theme**: Beautiful VS Code-inspired dark theme
- **Real-time Updates**: See file changes immediately
- **Session Management**: Maintain conversation context

## Architecture

### Backend (FastAPI)
- **api.py**: REST API wrapper around the existing AI agent
- Endpoints for chat, file operations, and session management
- CORS enabled for local development
- Streaming support for real-time responses

### Frontend (React + Vite)
- **Modern React**: Functional components with hooks
- **Vite**: Lightning-fast build tool and dev server
- **Component Structure**:
  - `ChatPanel`: Main chat interface with markdown and code highlighting
  - `FileExplorer`: Tree view of project files
  - `FileViewer`: Syntax-highlighted code display

## Prerequisites

1. **Python 3.12+** and **uv** (for backend)
2. **Node.js 16+** and **npm** (for frontend)
3. **Anthropic API Key**

## Installation & Setup

### 1. Backend Setup

The backend uses your existing AI agent code with a FastAPI wrapper.

```bash
# Set your API key
export ANTHROPIC_API_KEY="your-api-key-here"

# Run the backend (uses uv for dependencies)
uv run api.py
```

The API will start on `http://localhost:8000`

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will start on `http://localhost:5173`

## Usage

1. **Start the backend**: `uv run api.py` (in project root)
2. **Start the frontend**: `npm run dev` (in frontend directory)
3. **Open browser**: Navigate to `http://localhost:5173`

### Example Interactions

Try these commands in the chat:

- "List all Python files in the current directory"
- "Show me the contents of main.py"
- "Create a new file called test.py with a hello world function"
- "Add error handling to the read_file function in main.py"
- "What does the AIAgent class do?"

## API Endpoints

### Chat
- `POST /api/chat` - Send a message and get response
- `POST /api/chat/stream` - Stream chat responses (SSE)

### Files
- `POST /api/files/read` - Read file contents
- `POST /api/files/list` - List directory contents

### Session Management
- `GET /api/conversation/history/{session_id}` - Get conversation history
- `DELETE /api/conversation/{session_id}` - Clear conversation

## Project Structure

```
.
├── api.py                          # FastAPI backend
├── main.py                         # Original CLI agent
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatPanel.jsx      # Chat interface
│   │   │   ├── ChatPanel.css
│   │   │   ├── FileExplorer.jsx   # File tree view
│   │   │   ├── FileExplorer.css
│   │   │   ├── FileViewer.jsx     # Code viewer
│   │   │   └── FileViewer.css
│   │   ├── App.jsx                # Main app component
│   │   ├── App.css
│   │   ├── main.jsx               # React entry point
│   │   └── index.css              # Global styles
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── WEB_APP_README.md
```

## Customization

### Change Theme Colors

Edit `frontend/src/index.css` and component CSS files. Main colors:
- Primary: `#667eea` (purple-blue)
- Secondary: `#764ba2` (purple)
- Background: `#1e1e1e` (dark gray)
- Panel: `#252526` (slightly lighter gray)

### Add New File Operations

1. Add tool to `main.py` in `AIAgent._setup_tools()`
2. Add execution logic in `AIAgent._execute_tool()`
3. Add API endpoint in `api.py`
4. Use in frontend via chat or add UI controls

### Modify AI Behavior

Edit the system prompt in `api.py` or `main.py`:
```python
system="Your custom instructions here..."
```

## Building for Production

### Frontend
```bash
cd frontend
npm run build
```

This creates an optimized build in `frontend/dist/`

### Deployment Options

1. **Single Server**: 
   - Serve frontend static files with FastAPI
   - Use `StaticFiles` middleware

2. **Separate Hosting**:
   - Frontend: Vercel, Netlify, or Cloudflare Pages
   - Backend: Railway, Render, or AWS

3. **Docker**:
   - Create Dockerfile for backend
   - Multi-stage build for frontend

## Troubleshooting

### Backend won't start
- Check `ANTHROPIC_API_KEY` is set
- Verify port 8000 is available
- Check `api.log` for errors

### Frontend can't connect to backend
- Ensure backend is running on port 8000
- Check browser console for CORS errors
- Verify proxy settings in `vite.config.js`

### File operations fail
- Check file permissions
- Verify paths are correct
- Look at backend logs in terminal

## Performance Tips

1. **Large files**: The file viewer may be slow with very large files (>1MB)
2. **Many files**: File explorer loads entire directory at once
3. **Long conversations**: Consider clearing chat history periodically

## Security Notes

This is a development tool. For production:
- Add authentication (JWT, OAuth)
- Implement rate limiting
- Validate all file paths (prevent directory traversal)
- Use environment-specific CORS settings
- Add request size limits
- Implement proper session management

## Future Enhancements

Potential features to add:
- [ ] Real-time streaming chat responses
- [ ] Diff view for file changes before applying
- [ ] Multiple file tabs
- [ ] Search functionality
- [ ] Git integration
- [ ] Terminal emulator panel
- [ ] Collaborative editing
- [ ] File upload/download
- [ ] Keyboard shortcuts
- [ ] Mobile responsive design

## License

MIT License (same as the original project)

## Credits

Built on top of the Single-File AI Agent Tutorial:
- Original CLI by Thorsten Ball
- Implementation by Francis Beeson
- Web UI extension
