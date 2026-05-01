import React, { useCallback, useState } from 'react'
import axios from 'axios'
import {
  CalendarDays,
  ChevronDown,
  ChevronUp,
  Clock3,
  Compass,
  Leaf,
  MapPin,
  Sparkles,
  UsersRound,
  WalletCards,
} from 'lucide-react'
import Hero from './components/Hero'
import ChatInterface from './components/ChatInterface'
import { Message, TravelQuery } from './types'

const POPULAR_DESTINATIONS = [
  'Chiang Mai',
  'Phuket',
  'Krabi',
  'Chiang Rai',
  'Nan',
  'Koh Samui',
  'Pattaya',
  'Mae Hong Son',
  'Trang',
  'Hua Hin',
]

const MONTHS = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
  'July',
  'August',
  'September',
  'October',
  'November',
  'December',
]

const ACTIVITY_TYPES = [
  { value: '', label: 'Any type' },
  { value: 'nature', label: 'Nature' },
  { value: 'culture', label: 'Culture' },
  { value: 'adventure', label: 'Adventure' },
  { value: 'relaxation', label: 'Relaxation' },
  { value: 'family', label: 'Family' },
]

const BUDGET_TYPES = [
  { value: '', label: 'Not specified' },
  { value: 'budget', label: 'Budget' },
  { value: 'mid', label: 'Mid-range' },
  { value: 'luxury', label: 'Luxury' },
]

const GROUP_TYPES = [
  { value: '', label: 'Not specified' },
  { value: 'solo', label: 'Solo' },
  { value: 'couple', label: 'Couple' },
  { value: 'friends', label: 'Friends' },
  { value: 'family', label: 'Family' },
]

const DEFAULT_QUERY: TravelQuery = {
  destination: '',
  month: '',
  duration: '',
  activityType: '',
  budget: '',
  groupType: '',
}

const WELCOME_MESSAGE: Message = {
  id: 'welcome',
  role: 'assistant',
  content: `Hi, I am ready to help you plan a Thailand trip that fits your timing, budget, and travel style.

Fill in the planner above or type a question such as "Plan a 3-day mid-range trip to Chiang Mai in December."`,
  timestamp: new Date(),
}

function buildNaturalMessage(query: TravelQuery): string {
  const parts: string[] = []

  if (query.destination) {
    parts.push(`I want to travel to ${query.destination}`)
  } else {
    parts.push('I want to plan a trip in Thailand')
  }

  if (query.month) {
    const monthIndex = MONTHS.indexOf(query.month)
    if (monthIndex >= 0) {
      parts.push(`in ${query.month} (month ${monthIndex + 1})`)
    }
  }

  if (query.duration) {
    parts.push(`for ${query.duration} days`)
  }

  if (query.groupType) {
    parts.push(`as a ${query.groupType} trip`)
  }

  if (query.activityType) {
    parts.push(`with ${query.activityType} activities`)
  }

  if (query.budget) {
    const budgetLabel: Record<string, string> = {
      budget: 'budget',
      mid: 'mid-range',
      luxury: 'luxury',
    }
    parts.push(`on a ${budgetLabel[query.budget] || query.budget} budget`)
  }

  return `${parts.join(' ')}. Please check the crowd level and suggest activities, food, transportation, itinerary, and budget.`
}

const App: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([WELCOME_MESSAGE])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [chatHistory, setChatHistory] = useState<{ role: string; content: string }[]>([])
  const [query, setQuery] = useState<TravelQuery>(DEFAULT_QUERY)
  const [showForm, setShowForm] = useState(true)

  const updateQuery = (field: keyof TravelQuery, value: string) => {
    setQuery((prev) => ({ ...prev, [field]: value }))
  }

  const sendMessage = useCallback(
    async (messageText: string) => {
      if (!messageText.trim() || isLoading) return

      const userMessage: Message = {
        id: Date.now().toString(),
        role: 'user',
        content: messageText,
        timestamp: new Date(),
      }

      const loadingMessage: Message = {
        id: `loading-${Date.now()}`,
        role: 'assistant',
        content: '',
        timestamp: new Date(),
        isLoading: true,
      }

      setMessages((prev) => [...prev, userMessage, loadingMessage])
      setInput('')
      setIsLoading(true)

      try {
        const historyForApi = chatHistory.map((h) => ({
          role: h.role,
          content: h.content,
        }))

        const response = await axios.post('/api/chat', {
          message: messageText,
          history: historyForApi,
        })

        const aiText = response.data.response || 'Sorry, I cannot answer right now.'

        const aiMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: aiText,
          timestamp: new Date(),
        }

        setMessages((prev) => prev.filter((m) => !m.isLoading).concat(aiMessage))
        setChatHistory((prev) => [
          ...prev,
          { role: 'user', content: messageText },
          { role: 'assistant', content: aiText },
        ])
      } catch (error) {
        const errMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content:
            'Unable to connect to the AI right now. Please make sure the backend is running on port 8000 and GROQ_API_KEY is configured.',
          timestamp: new Date(),
        }
        setMessages((prev) => prev.filter((m) => !m.isLoading).concat(errMessage))
      } finally {
        setIsLoading(false)
      }
    },
    [isLoading, chatHistory]
  )

  const handleFormSubmit = () => {
    if (!query.destination && !query.month) {
      alert('Please enter a destination or travel month first.')
      return
    }
    setShowForm(false)
    sendMessage(buildNaturalMessage(query))
  }

  const handleDestinationClick = (destination: string) => {
    updateQuery('destination', destination)
    if (!showForm) setShowForm(true)
  }

  return (
    <div className="page-shell">
      <Hero />

      <main id="planner" className="content-wrap">
        <section className="destination-strip" aria-labelledby="popular-destinations">
          <p id="popular-destinations" className="section-label">
            Popular Destinations
          </p>
          <div className="destination-pills">
            {POPULAR_DESTINATIONS.map((dest) => (
              <button
                key={dest}
                onClick={() => handleDestinationClick(dest)}
                className={`destination-pill ${query.destination === dest ? 'active' : ''}`}
                type="button"
              >
                {dest}
              </button>
            ))}
          </div>
        </section>

        <section className="planner-card" aria-labelledby="planner-heading">
          <button className="planner-toggle" onClick={() => setShowForm((v) => !v)} type="button">
            <span className="planner-toggle-title">
              <Sparkles size={18} />
              <span id="planner-heading">Trip Planner</span>
            </span>
            {showForm ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
          </button>

          {showForm && (
            <div className="planner-body">
              <div className="planner-grid">
                <label className="field-group">
                  <span>
                    <MapPin size={16} />
                    Destination
                  </span>
                  <input
                    type="text"
                    value={query.destination}
                    onChange={(e) => updateQuery('destination', e.target.value)}
                    placeholder="e.g. Chiang Mai, Phuket"
                  />
                </label>

                <label className="field-group">
                  <span>
                    <CalendarDays size={16} />
                    Travel Month
                  </span>
                  <select value={query.month} onChange={(e) => updateQuery('month', e.target.value)}>
                    <option value="">Select a month</option>
                    {MONTHS.map((m) => (
                      <option key={m} value={m}>
                        {m}
                      </option>
                    ))}
                  </select>
                </label>

                <label className="field-group">
                  <span>
                    <Clock3 size={16} />
                    Duration
                  </span>
                  <input
                    type="number"
                    value={query.duration}
                    onChange={(e) => updateQuery('duration', e.target.value)}
                    placeholder="e.g. 3"
                    min="1"
                    max="30"
                  />
                </label>

                <label className="field-group">
                  <span>
                    <Leaf size={16} />
                    Activity Type
                  </span>
                  <select
                    value={query.activityType}
                    onChange={(e) => updateQuery('activityType', e.target.value)}
                  >
                    {ACTIVITY_TYPES.map((a) => (
                      <option key={a.value} value={a.value}>
                        {a.label}
                      </option>
                    ))}
                  </select>
                </label>

                <label className="field-group">
                  <span>
                    <WalletCards size={16} />
                    Budget
                  </span>
                  <select value={query.budget} onChange={(e) => updateQuery('budget', e.target.value)}>
                    {BUDGET_TYPES.map((b) => (
                      <option key={b.value} value={b.value}>
                        {b.label}
                      </option>
                    ))}
                  </select>
                </label>

                <label className="field-group">
                  <span>
                    <UsersRound size={16} />
                    Group Type
                  </span>
                  <select
                    value={query.groupType}
                    onChange={(e) => updateQuery('groupType', e.target.value)}
                  >
                    {GROUP_TYPES.map((g) => (
                      <option key={g.value} value={g.value}>
                        {g.label}
                      </option>
                    ))}
                  </select>
                </label>
              </div>

              <button className="primary-action" onClick={handleFormSubmit} disabled={isLoading} type="button">
                <Compass size={19} />
                {isLoading ? 'Analyzing...' : 'Plan My Trip'}
              </button>
            </div>
          )}
        </section>

        <section className="chat-frame" aria-label="Trip planning chat">
          <ChatInterface
            messages={messages}
            input={input}
            isLoading={isLoading}
            onInputChange={setInput}
            onSend={() => sendMessage(input)}
          />
        </section>

        <p className="footer-note">
          Travel details may change by season. Please verify key information before your trip.
        </p>
      </main>
    </div>
  )
}

export default App
