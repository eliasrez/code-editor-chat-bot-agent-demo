# Web UI Visual Preview

Since I can't show actual screenshots, here's a detailed description of what the interface looks like:

## Overall Layout

```
┌────────────────────────────────────────────────────────────────────────┐
│  AI Code Assistant                                                     │
│  Chat with AI to manipulate files in your project                     │
│  [Purple gradient header - modern and clean]                          │
├──────────────┬─────────────────────────────────────────────────────────┤
│              │                                                         │
│  📁 EXPLORER │                    MAIN CONTENT AREA                    │
│              │                                                         │
│  📁 frontend │  ┌─────────────────┬──────────────────────────────┐   │
│    📄 src    │  │                 │                              │   │
│  📄 main.py  │  │      CHAT       │       FILE VIEWER            │   │
│  📄 api.py   │  │                 │                              │   │
│  📄 README   │  │                 │                              │   │
│              │  │                 │                              │   │
│              │  │                 │                              │   │
│              │  │                 │                              │   │
│              │  │                 │                              │   │
│  [Resizable] │  │  [Messages]     │  [Code with syntax          │   │
│              │  │                 │   highlighting]              │   │
│              │  │                 │                              │   │
│              │  │                 │                              │   │
│              │  │  ┌────────────┐ │                              │   │
│              │  │  │ Your input │ │                              │   │
│              │  │  └────────────┘ │                              │   │
│              │  │     [Send]      │                              │   │
│              │  └─────────────────┴──────────────────────────────┘   │
│              │                                                         │
└──────────────┴─────────────────────────────────────────────────────────┘
```

## Detailed Component Views

### 1. Header
```
╔══════════════════════════════════════════════════════════════════════╗
║  🎨 AI Code Assistant                                                ║
║  Chat with AI to manipulate files in your project                   ║
╚══════════════════════════════════════════════════════════════════════╝
   ↑ Gradient background: purple-blue (#667eea) to purple (#764ba2)
   ↑ White text with slight shadow
   ↑ Clean, modern look
```

### 2. File Explorer (Left Sidebar)
```
┌─────────────────┐
│   EXPLORER      │
├─────────────────┤
│ 📁 .git/        │
│ 📄 .gitignore   │
│ 📄 LICENSE      │
│ 📄 README.MD    │
│ 📄 agent.log    │
│ 📁 frontend/    │
│ 📄 main.py      │
│ 📁 runbook/     │
│ 📁 tools/       │
└─────────────────┘
  ↑ Dark gray background (#252526)
  ↑ Lighter on hover (#2a2d2e)
  ↑ Emoji icons for visual clarity
  ↑ Click to open files
  ↑ Resizable by dragging right edge
```

### 3. Chat Panel
```
┌───────────────────────────────────────┐
│  Chat                        [Clear]  │
├───────────────────────────────────────┤
│                                       │
│  YOU                                  │
│  ┌─────────────────────────────────┐ │
│  │ Show me the contents of main.py │ │
│  └─────────────────────────────────┘ │
│                                       │
│  ASSISTANT                            │
│  ┌─────────────────────────────────┐ │
│  │ I'll read that file for you...  │ │
│  │                                 │ │
│  │ ```python                       │ │
│  │ import os                       │ │
│  │ import sys                      │ │
│  │ ```                             │ │
│  └─────────────────────────────────┘ │
│                                       │
│  ● ● ● (typing indicator)            │
│                                       │
├───────────────────────────────────────┤
│  ┌─────────────────────────────────┐ │
│  │ Ask AI to read, edit files...  │ │
│  └─────────────────────────────────┘ │
│                            [Send]     │
└───────────────────────────────────────┘
  ↑ User messages: Blue left border
  ↑ Assistant messages: Green left border
  ↑ Code blocks: Syntax highlighted
  ↑ Scrollable message history
  ↑ Auto-scroll to latest message
```

### 4. File Viewer
```
┌─────────────────────────────────────────────────┐
│  main.py                                        │
│  ./main.py                                      │
├─────────────────────────────────────────────────┤
│  1  # /// script                                │
│  2  # requires-python = ">=3.12"                │
│  3  # dependencies = [                          │
│  4  #     "anthropic",                          │
│  5  #     "pydantic",                           │
│  6  # ]                                         │
│  7  # ///                                       │
│  8                                              │
│  9  import os                                   │
│ 10  import sys                                  │
│ 11  import argparse                             │
│                                                 │
│  [Scrollable content with line numbers]        │
│  [Syntax highlighting based on file type]      │
└─────────────────────────────────────────────────┘
  ↑ Monaco Editor-style highlighting
  ↑ Line numbers on the left
  ↑ Color-coded syntax:
     - Comments: Green
     - Strings: Orange
     - Keywords: Purple
     - Functions: Yellow
```

## Color Scheme

The interface uses a professional dark theme:

### Primary Colors
- **Background**: `#1e1e1e` (Dark gray - main background)
- **Panels**: `#252526` (Slightly lighter - panels and headers)
- **Borders**: `#3e3e42` (Medium gray - separators)
- **Text**: `#d4d4d4` (Light gray - main text)

### Accent Colors
- **Primary Gradient**: `#667eea → #764ba2` (Purple-blue gradient)
- **User Messages**: `#667eea` (Blue-purple)
- **Assistant Messages**: `#4ec9b0` (Teal-green)
- **Hover States**: `#4e4e52` (Lighter gray)

### Syntax Highlighting
- **Keywords**: Purple/Pink
- **Strings**: Orange/Amber
- **Comments**: Green
- **Functions**: Yellow
- **Numbers**: Light green
- **Operators**: Gray

## Interaction States

### Normal State
- Clean, minimal design
- Clear visual hierarchy
- Easy to scan

### Hover State
- File items highlight
- Buttons lighten slightly
- Cursor changes to pointer

### Active State
- Input fields have blue border
- Buttons have gradient background
- Selected items stay highlighted

### Loading State
- Typing indicator (animated dots)
- Disabled input
- Visual feedback

## Responsive Behavior

### Resizing
- Drag the divider between Explorer and Content
- Minimum width: 150px
- Maximum width: 500px
- Smooth, fluid animation

### Scrolling
- Independent scroll in each panel
- Smooth scrollbar styling
- Auto-scroll in chat to latest message

## Empty States

### No Files Selected
Only chat panel is visible
File viewer appears when you click a file

### No Messages
Chat shows helpful placeholder:
```
     Start a conversation with the AI assistant
     
     Try: "Show me the contents of main.py"
```

### No Files in Directory
Explorer shows:
```
     No files found
```

## Visual Hierarchy

1. **Header** (Most prominent)
   - Gradient background
   - Large title
   - Spans full width

2. **Main Content** (Primary focus)
   - Largest area
   - Split panels
   - Most interaction happens here

3. **Sidebar** (Secondary)
   - Subdued colors
   - Support role
   - Navigation purpose

## Animation & Polish

### Smooth Transitions
- Hover states: 0.2s
- Panel resizing: Smooth dragging
- Typing indicator: Bouncing dots

### Visual Feedback
- Button hover effects
- Focus states on inputs
- Loading indicators

### Professional Touches
- Consistent spacing
- Aligned elements
- Proper contrast ratios
- Accessible colors

## Comparison to Popular Apps

The design is inspired by:
- **VS Code**: Dark theme, file explorer, syntax highlighting
- **ChatGPT**: Clean chat interface, message bubbles
- **GitHub**: Code display, file viewer
- **Notion**: Modern layout, smooth interactions

## Mobile Considerations

Currently optimized for desktop (1280px+)
Future enhancements could include:
- Collapsible sidebar
- Stacked layout on small screens
- Touch-friendly controls

## Accessibility

- High contrast ratios
- Keyboard navigation supported
- Focus indicators
- Semantic HTML
- ARIA labels (can be added)

## Print Preview

If you run the application, you'll see all these elements come together in a cohesive, professional interface that's both beautiful and functional!

**To see it yourself:**
1. Follow QUICKSTART.md
2. Open http://localhost:5173
3. Start exploring!

The interface is intuitive enough that you can start using it immediately without a tutorial.
