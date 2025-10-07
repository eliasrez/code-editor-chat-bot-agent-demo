import { useState, useEffect, useCallback } from 'react'
import './FileExplorer.css'

function FileExplorer({ onFileSelect }) {
  const [items, setItems] = useState([])
  const [currentPath, setCurrentPath] = useState('.')
  const [expandedFolders, setExpandedFolders] = useState(new Set(['.']))
  const [refreshKey, setRefreshKey] = useState(0) 

 const loadDirectory = useCallback(async (path) => {
    try {
      const response = await fetch('/api/files/list', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path })
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      return data.items
    } catch (error) {
      console.error('Error loading directory:', error)
      return []
    }
  }, []) // Empty dependency array means the function reference is stable
  
  const refreshExplorer = () => {
    // Toggling this key forces the useEffect hook to run again
    setRefreshKey(prevKey => prevKey + 1)
  }

  useEffect(() => {
    loadDirectory(currentPath).then(setItems)
  }, [currentPath, loadDirectory, refreshKey])

  const handleItemClick = async (item) => {
    if (item.type === 'directory') {
      const isExpanded = expandedFolders.has(item.path)
      const newExpanded = new Set(expandedFolders)
      
      if (isExpanded) {
        newExpanded.delete(item.path)
      } else {
        newExpanded.add(item.path)
      }
      
      setExpandedFolders(newExpanded)
    } else {
      onFileSelect(item)
    }
  }

  const renderTree = (items, level = 0) => {
    return items?.map((item, idx) => (
      <div key={idx}>
        <div
          className={`file-item ${item.type}`}
          style={{ paddingLeft: `${level * 20 + 10}px` }}
          onClick={() => handleItemClick(item)}
        >
          <span className="icon">
            {item.type === 'directory' 
              ? (expandedFolders.has(item.path) ? '📂' : '📁')
              : '📄'
            }
          </span>
          <span className="name">{item.name}</span>
        </div>
      </div>
    ))
  }

  return (
    <div className="file-explorer">
      <div className="explorer-header">
        <h3>Explorer</h3>
      </div>
      <button onClick={refreshExplorer} className="refresh-btn">
          Refresh
      </button>
      <div className="file-tree">
        {items?.length === 0 ? (
          <div className="empty">No files found</div>
        ) : (
          renderTree(items)
        )}
      </div>
    </div>
  )
}

export default FileExplorer
