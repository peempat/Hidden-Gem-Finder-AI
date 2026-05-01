export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
  isLoading?: boolean
}

export interface TravelQuery {
  destination: string
  month: string
  duration: string
  activityType: string
  budget: string
  groupType: string
}
