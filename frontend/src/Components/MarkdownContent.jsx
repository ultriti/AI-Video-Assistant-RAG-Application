import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

const MarkdownContent = ({ content, className = '' }) => (
  <div className={`markdown-content ${className}`}>
    <ReactMarkdown remarkPlugins={[remarkGfm]}>
      {content || ''}
    </ReactMarkdown>
  </div>
)

export default MarkdownContent
