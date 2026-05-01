import React from 'react'
import ReactMarkdown from 'react-markdown'
import { Bot, UserRound } from 'lucide-react'
import { Message } from '../types'

interface MessageBubbleProps {
  message: Message
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.role === 'user'

  const formatTime = (date: Date) =>
    new Date(date).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
    })

  if (message.isLoading) {
    return (
      <div className="message-row assistant">
        <div className="avatar assistant-avatar">
          <Bot size={18} />
        </div>
        <div className="message-stack">
          <div className="bubble assistant-bubble loading-bubble">
            <span>Analyzing</span>
            <span className="typing-dot" />
            <span className="typing-dot" />
            <span className="typing-dot" />
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className={`message-row ${isUser ? 'user' : 'assistant'}`}>
      {!isUser && (
        <div className="avatar assistant-avatar">
          <Bot size={18} />
        </div>
      )}

      <div className="message-stack">
        {!isUser && <p className="message-name">Gemmy AI</p>}
        <div className={`bubble ${isUser ? 'user-bubble' : 'assistant-bubble'}`}>
          {isUser ? (
            <p>{message.content}</p>
          ) : (
            <div className="markdown-content">
              <ReactMarkdown>{message.content}</ReactMarkdown>
            </div>
          )}
        </div>
        <p className={`message-time ${isUser ? 'right' : ''}`}>{formatTime(message.timestamp)}</p>
      </div>

      {isUser && (
        <div className="avatar user-avatar">
          <UserRound size={18} />
        </div>
      )}
    </div>
  )
}

export default MessageBubble
