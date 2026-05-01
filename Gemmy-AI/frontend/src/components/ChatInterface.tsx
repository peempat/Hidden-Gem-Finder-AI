import React, { useEffect, useRef } from 'react'
import { Send } from 'lucide-react'
import { Message } from '../types'
import MessageBubble from './MessageBubble'

interface ChatInterfaceProps {
  messages: Message[]
  input: string
  isLoading: boolean
  onInputChange: (value: string) => void
  onSend: () => void
}

const QUICK_SUGGESTIONS = [
  'Recommend relaxing places in Thailand',
  'Is Chiang Mai good next month?',
  'Suggest a Phuket summer trip',
  'Low-crowd beach destinations for May',
]

const ChatInterface: React.FC<ChatInterfaceProps> = ({
  messages,
  input,
  isLoading,
  onInputChange,
  onSend,
}) => {
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      if (!isLoading && input.trim()) {
        onSend()
      }
    }
  }

  const handleSuggestionClick = (suggestion: string) => {
    onInputChange(suggestion)
    inputRef.current?.focus()
  }

  return (
    <div className="chat-panel">
      <div className="chat-header">
        <div>
          <p>Gemmy AI</p>
          <span>Ready to shape a trip around you</span>
        </div>
      </div>

      <div className="messages-area chat-scroll">
        {messages.map((msg) => (
          <MessageBubble key={msg.id} message={msg} />
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="quick-suggestions" aria-label="Example questions">
        {QUICK_SUGGESTIONS.map((suggestion) => (
          <button
            key={suggestion}
            onClick={() => handleSuggestionClick(suggestion)}
            disabled={isLoading}
            type="button"
          >
            {suggestion}
          </button>
        ))}
      </div>

      <div className="chat-input-bar">
        <textarea
          ref={inputRef}
          value={input}
          onChange={(e) => onInputChange(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your message..."
          disabled={isLoading}
          rows={1}
          onInput={(e) => {
            const target = e.target as HTMLTextAreaElement
            target.style.height = 'auto'
            target.style.height = Math.min(target.scrollHeight, 120) + 'px'
          }}
        />

        <button
          className="send-button"
          onClick={onSend}
          disabled={isLoading || !input.trim()}
          type="button"
          aria-label="Send message"
        >
          {isLoading ? <span className="small-spinner" /> : <Send size={18} />}
        </button>
      </div>
    </div>
  )
}

export default ChatInterface
