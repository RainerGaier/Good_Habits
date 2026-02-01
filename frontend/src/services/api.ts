/**
 * API service for backend communication
 */

import type {
  HabitWithStats,
  HabitCreate,
  HabitUpdate,
  HabitResponse,
  CompletionResponse,
  CompletionsListResponse,
  AbsencesListResponse,
  AbsenceCreate,
  AbsenceResponse,
} from '@/types/habit'

const API_BASE = '/api'

export async function fetchApi<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  })

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`)
  }

  // Handle 204 No Content
  if (response.status === 204) {
    return undefined as T
  }

  return response.json()
}

export const api = {
  get: <T>(endpoint: string) => fetchApi<T>(endpoint),

  post: <T>(endpoint: string, data: unknown) =>
    fetchApi<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  put: <T>(endpoint: string, data: unknown) =>
    fetchApi<T>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  delete: <T>(endpoint: string) =>
    fetchApi<T>(endpoint, {
      method: 'DELETE',
    }),

  // Habit-specific API methods
  habits: {
    list: () => api.get<HabitWithStats[]>('/habits'),

    get: (id: string) => api.get<HabitResponse>(`/habits/${id}`),

    create: (data: HabitCreate) => api.post<HabitResponse>('/habits', data),

    update: (id: string, data: HabitUpdate) =>
      api.put<HabitResponse>(`/habits/${id}`, data),

    delete: (id: string) => api.delete<void>(`/habits/${id}`),

    complete: (id: string, date?: string) =>
      api.post<CompletionResponse>(
        `/habits/${id}/complete`,
        date ? { date } : {}
      ),

    uncomplete: (id: string, date: string) =>
      api.delete<void>(`/habits/${id}/completions/${date}`),
  },

  completions: {
    list: (habitId: string, startDate?: string, endDate?: string) => {
      let url = `/habits/${habitId}/completions`
      if (startDate && endDate) {
        url += `?start_date=${startDate}&end_date=${endDate}`
      }
      return api.get<CompletionsListResponse>(url)
    },
  },

  absences: {
    list: (habitId: string, startDate?: string, endDate?: string) => {
      let url = `/habits/${habitId}/absences`
      if (startDate && endDate) {
        url += `?start_date=${startDate}&end_date=${endDate}`
      }
      return api.get<AbsencesListResponse>(url)
    },

    create: (habitId: string, data?: AbsenceCreate) =>
      api.post<AbsenceResponse>(`/habits/${habitId}/absences`, data || {}),

    delete: (habitId: string, date: string) =>
      api.delete<void>(`/habits/${habitId}/absences/${date}`),
  },
}
