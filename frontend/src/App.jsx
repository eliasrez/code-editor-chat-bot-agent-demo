import { useState, useRef, useEffect } from 'react'
import ChatPanel from './components/ChatPanel'
import FileExplorer from './components/FileExplorer'
import FileViewer from './components/FileViewer'
import './App.css'

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [fileContent, setFileContent] = useState('')
  const [sidebarWidth, setSidebarWidth] = useState(250)
  const [isResizing, setIsResizing] = useState(false)

  const handleFileSelect = async (file) => {
    if (file.type === 'file') {
      setSelectedFile(file)
      try {
        const response = await fetch('/api/files/read', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ path: file.path })
        })
        const data = await response.json()
        setFileContent(data.content)
      } catch (error) {
        console.error('Error reading file:', error)
        setFileContent(`Error loading file: ${error.message}`)
      }
    }
  }

  const startResizing = () => {
    setIsResizing(true)
  }

  const stopResizing = () => {
    setIsResizing(false)
  }

  const resize = (e) => {
    if (isResizing) {
      const newWidth = e.clientX
      if (newWidth > 150 && newWidth < 500) {
        setSidebarWidth(newWidth)
      }
    }
  }

  useEffect(() => {
    if (isResizing) {
      document.addEventListener('mousemove', resize)
      document.addEventListener('mouseup', stopResizing)
    }
    return () => {
      document.removeEventListener('mousemove', resize)
      document.removeEventListener('mouseup', stopResizing)
    }
  }, [isResizing])

  return (
    <div className="app">
      <div className="header">
        <h1>AI Code Assistant</h1>
        <p>Chat with AI to manipulate files in your project</p>
      </div>
      
      <div className="main-content">
        <div className="sidebar" style={{ width: `${sidebarWidth}px` }}>
          <FileExplorer onFileSelect={handleFileSelect} />
        </div>
        
        <div 
          className="resizer" 
          onMouseDown={startResizing}
        />
        
        <div className="content-area">
          <div className="panels">
            <ChatPanel />
            {selectedFile && (
              <FileViewer 
                file={selectedFile} 
                content={fileContent}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
