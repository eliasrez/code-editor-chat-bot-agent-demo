# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACES                          │
├──────────────────────┬──────────────────────────────────────────┤
│                      │                                           │
│   CLI (main.py)      │        Web UI (Browser)                  │
│                      │                                           │
│   Terminal           │   ┌─────────────────────────────────┐   │
│   └─ Input prompt    │   │  React Frontend (Port 5173)     │   │
│   └─ Text output     │   │                                 │   │
│                      │   │  ┌──────────────────────────┐   │   │
│                      │   │  │  ChatPanel Component     │   │   │
│                      │   │  │  - Message display       │   │   │
│                      │   │  │  - Input field           │   │   │
│                      │   │  │  - Markdown rendering    │   │   │
│                      │   │  └──────────────────────────┘   │   │
│                      │   │                                 │   │
│                      │   │  ┌──────────────────────────┐   │   │
│                      │   │  │  FileExplorer Component  │   │   │
│                      │   │  │  - Directory tree        │   │   │
│                      │   │  │  - File selection        │   │   │
│                      │   │  └──────────────────────────┘   │   │
│                      │   │                                 │   │
│                      │   │  ┌──────────────────────────┐   │   │
│                      │   │  │  FileViewer Component    │   │   │
│                      │   │  │  - Syntax highlighting   │   │   │
│                      │   │  │  - Line numbers          │   │   │
│                      │   │  └──────────────────────────┘   │   │
│                      │   └─────────────────────────────────┘   │
│                      │            │                             │
│                      │            │ HTTP/REST                   │
│                      │            ↓                             │
│                      │   ┌─────────────────────────────────┐   │
│                      │   │  FastAPI Backend (Port 8000)    │   │
│                      │   │                                 │   │
│                      │   │  Endpoints:                     │   │
│                      │   │  - POST /api/chat               │   │
│                      │   │  - POST /api/files/read         │   │
│                      │   │  - POST /api/files/list         │   │
│                      │   │  - GET /api/conversation/...    │   │
│                      │   └─────────────────────────────────┘   │
│                      │            │                             │
└──────────────────────┴────────────┼─────────────────────────────┘
                                    │
                                    ↓
            ┌───────────────────────────────────────────┐
            │         AIAgent Class (Shared)            │
            │                                           │
            │  ┌─────────────────────────────────────┐ │
            │  │  Conversation Management            │ │
            │  │  - Message history                  │ │
            │  │  - Context tracking                 │ │
            │  └─────────────────────────────────────┘ │
            │                                           │
            │  ┌─────────────────────────────────────┐ │
            │  │  Claude API Integration             │ │
            │  │  - Model: claude-sonnet-4-5         │ │
            │  │  - Tool use protocol                │ │
            │  │  - Response parsing                 │ │
            │  └─────────────────────────────────────┘ │
            │                                           │
            │  ┌─────────────────────────────────────┐ │
            │  │  Tool Execution Engine              │ │
            │  │  - read_file()                      │ │
            │  │  - list_files()                     │ │
            │  │  - edit_file()                      │ │
            │  └─────────────────────────────────────┘ │
            └───────────────────────────────────────────┘
                         │              │
                         ↓              ↓
            ┌──────────────────┐  ┌──────────────────┐
            │  Claude API      │  │  File System     │
            │  (Anthropic)     │  │  - Read files    │
            │                  │  │  - Write files   │
            │  - Tool use      │  │  - List dirs     │
            │  - Reasoning     │  │                  │
            └──────────────────┘  └──────────────────┘
```

## Data Flow

### CLI Flow
```
1. User types message in terminal
2. AIAgent.chat() receives message
3. Message sent to Claude API with tool definitions
4. Claude decides which tools to use
5. AIAgent executes tools (read/write/list files)
6. Tool results sent back to Claude
7. Claude formulates response
8. Response printed to terminal
```

### Web UI Flow
```
1. User types message in browser chat
2. HTTP POST to /api/chat endpoint
3. FastAPI calls AIAgent.chat()
4. AIAgent sends to Claude API (same as CLI)
5. Claude uses tools via AIAgent
6. Tools execute on server filesystem
7. Results go back to Claude
8. Response returned via FastAPI
9. React displays formatted response in UI
```

## Component Responsibilities

### Frontend (React)

**ChatPanel.jsx**
- Manages conversation state
- Sends messages to backend
- Renders chat history with markdown
- Handles loading states

**FileExplorer.jsx**
- Fetches directory structure
- Displays file tree
- Handles file selection
- Manages expanded folders

**FileViewer.jsx**
- Displays file contents
- Syntax highlighting
- Shows file metadata

**App.jsx**
- Overall layout
- Panel resizing
- State coordination

### Backend (FastAPI)

**api.py**
- HTTP endpoint handlers
- Session management
- CORS configuration
- AIAgent lifecycle

**main.py**
- Core AI agent logic
- Tool definitions
- Claude API integration
- File operations

## Technology Stack

### CLI
```
Python 3.12+
├── anthropic (Claude API client)
├── pydantic (Data validation)
└── uv (Package management)
```

### Web Backend
```
Python 3.12+
├── anthropic (Claude API)
├── pydantic (Validation)
├── fastapi (Web framework)
├── uvicorn (ASGI server)
└── uv (Package management)
```

### Web Frontend
```
Node.js 16+
├── React 18 (UI library)
├── Vite (Build tool)
├── react-markdown (Markdown rendering)
├── react-syntax-highlighter (Code highlighting)
└── axios (HTTP client)
```

## Security Model

### CLI
- Direct file system access
- No network exposure
- API key in environment

### Web UI
- Backend has file system access
- Frontend makes HTTP requests
- CORS protects endpoints
- No authentication (local dev only)

### Production Considerations
For production deployment, add:
- Authentication (JWT/OAuth)
- Path validation (prevent traversal)
- Rate limiting
- Input sanitization
- HTTPS
- Session security

## Scalability

### Current (Single User)
- One agent instance per session
- In-memory session storage
- Local filesystem only

### Future (Multi-User)
Would need:
- Database for sessions
- User authentication
- Workspace isolation
- Message queue for long operations
- Horizontal scaling with load balancer

## Extension Points

### Adding New Tools
1. Define tool in `AIAgent._setup_tools()`
2. Implement in `AIAgent._execute_tool()`
3. Optionally add API endpoint
4. Use via natural language

### Frontend Customization
- Modify component CSS for styling
- Add new React components
- Extend API with new endpoints
- Add features like file upload

### Backend Enhancement
- Add new API routes in FastAPI
- Implement caching layer
- Add background tasks
- Integrate with databases

## Development Workflow

```
┌─────────────┐
│  Edit Code  │
└──────┬──────┘
       │
       ↓
┌─────────────┐       ┌──────────────┐
│   Backend   │       │   Frontend   │
│   (uv run)  │       │  (npm run)   │
└──────┬──────┘       └──────┬───────┘
       │                     │
       │   Hot Reload        │  Hot Reload
       │   (automatic)       │  (automatic)
       │                     │
       ↓                     ↓
┌─────────────────────────────────┐
│       Test in Browser           │
│    http://localhost:5173        │
└─────────────────────────────────┘
```

## Logging and Debugging

### CLI
- Logs to `agent.log`
- Console output for user
- Exception tracebacks

### Web UI
- Backend logs to console
- Frontend logs to browser console
- Network tab for API debugging
- React DevTools for component state

## Performance Characteristics

**Bottlenecks:**
1. Claude API response time (1-5 seconds)
2. Large file operations
3. Directory listing with many files

**Optimizations:**
- Async operations where possible
- Streaming responses (implemented)
- Caching (future enhancement)
- Lazy loading (future enhancement)

This architecture provides a solid foundation that's easy to understand, extend, and deploy.
