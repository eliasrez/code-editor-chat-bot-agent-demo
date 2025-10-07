import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism'
import './FileViewer.css'

function FileViewer({ file, content }) {
  const getLanguage = (filename) => {
    const ext = filename.split('.').pop()
    const langMap = {
      'js': 'javascript',
      'jsx': 'javascript',
      'ts': 'typescript',
      'tsx': 'typescript',
      'py': 'python',
      'java': 'java',
      'cpp': 'cpp',
      'c': 'c',
      'cs': 'csharp',
      'go': 'go',
      'rs': 'rust',
      'rb': 'ruby',
      'php': 'php',
      'html': 'html',
      'css': 'css',
      'json': 'json',
      'xml': 'xml',
      'yaml': 'yaml',
      'yml': 'yaml',
      'md': 'markdown',
      'sh': 'bash',
      'sql': 'sql'
    }
    return langMap[ext] || 'text'
  }

  return (
    <div className="file-viewer">
      <div className="file-viewer-header">
        <h3>{file.name}</h3>
        <span className="file-path">{file.path}</span>
      </div>
      <div className="file-content">
        <SyntaxHighlighter
          language={getLanguage(file.name)}
          style={vscDarkPlus}
          showLineNumbers
          customStyle={{
            margin: 0,
            padding: '20px',
            fontSize: '13px',
            background: '#1e1e1e'
          }}
        >
          {content}
        </SyntaxHighlighter>
      </div>
    </div>
  )
}

export default FileViewer
