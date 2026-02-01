import { useState, useEffect, useCallback } from 'react'
import { api } from '@/services/api'
import type { HabitWithStats, HabitCreate, HabitUpdate } from '@/types/habit'

interface UseHabitsReturn {
  habits: HabitWithStats[]
  loading: boolean
  error: string | null
  refetch: () => Promise<void>
  createHabit: (data: HabitCreate) => Promise<void>
  updateHabit: (id: string, data: HabitUpdate) => Promise<void>
  deleteHabit: (id: string) => Promise<void>
  toggleCompletion: (habit: HabitWithStats) => Promise<void>
}

export function useHabits(): UseHabitsReturn {
  const [habits, setHabits] = useState<HabitWithStats[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchHabits = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await api.habits.list()
      setHabits(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch habits')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchHabits()
  }, [fetchHabits])

  const createHabit = useCallback(
    async (data: HabitCreate) => {
      await api.habits.create(data)
      await fetchHabits()
    },
    [fetchHabits]
  )

  const updateHabit = useCallback(
    async (id: string, data: HabitUpdate) => {
      await api.habits.update(id, data)
      await fetchHabits()
    },
    [fetchHabits]
  )

  const deleteHabit = useCallback(
    async (id: string) => {
      await api.habits.delete(id)
      await fetchHabits()
    },
    [fetchHabits]
  )

  const toggleCompletion = useCallback(
    async (habit: HabitWithStats) => {
      const today = new Date().toISOString().split('T')[0]
      if (habit.completed_today) {
        await api.habits.uncomplete(habit.id, today)
      } else {
        await api.habits.complete(habit.id)
      }
      await fetchHabits()
    },
    [fetchHabits]
  )

  return {
    habits,
    loading,
    error,
    refetch: fetchHabits,
    createHabit,
    updateHabit,
    deleteHabit,
    toggleCompletion,
  }
}
