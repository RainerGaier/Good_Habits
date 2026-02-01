/**
 * TypeScript interfaces for habit-related types.
 * These mirror the backend Pydantic schemas exactly.
 */

// Completion rate nested object
export interface CompletionRate {
  week: number
  month: number
  all_time: number
}

// Habit with computed statistics (GET /habits response)
export interface HabitWithStats {
  id: string
  name: string
  description: string | null
  created_at: string // ISO datetime string
  updated_at: string // ISO datetime string
  current_streak: number
  best_streak: number
  completion_rate: CompletionRate
  completed_today: boolean
}

// Create habit request
export interface HabitCreate {
  name: string
  description?: string | null
}

// Update habit request
export interface HabitUpdate {
  name?: string
  description?: string | null
}

// Habit response (POST/PUT response)
export interface HabitResponse {
  id: string
  name: string
  description: string | null
  created_at: string
  updated_at: string
}

// Completion response
export interface CompletionResponse {
  habit_id: string
  date: string // YYYY-MM-DD format
  completed: boolean
}
