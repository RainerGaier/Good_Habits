import { useState, useEffect, useCallback } from 'react'
import { api } from '@/services/api'
import type { AbsenceItem } from '@/types/habit'

interface UseCalendarDataReturn {
  completions: Set<string>
  absences: Map<string, string | null> // date -> reason
  loading: boolean
  error: string | null
  refetch: () => Promise<void>
  toggleCompletion: (date: string, isCompleted: boolean) => Promise<void>
  addAbsence: (date: string, reason?: string) => Promise<void>
  removeAbsence: (date: string) => Promise<void>
  year: number
  month: number
  setYear: (year: number) => void
  setMonth: (month: number) => void
}

export function useCalendarData(
  habitId: string,
  initialYear: number,
  initialMonth: number
): UseCalendarDataReturn {
  const [year, setYear] = useState(initialYear)
  const [month, setMonth] = useState(initialMonth)
  const [completions, setCompletions] = useState<Set<string>>(new Set())
  const [absences, setAbsences] = useState<Map<string, string | null>>(new Map())
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Calculate date range for the month
  const startDate = `${year}-${String(month + 1).padStart(2, '0')}-01`
  const lastDay = new Date(year, month + 1, 0).getDate()
  const endDate = `${year}-${String(month + 1).padStart(2, '0')}-${String(lastDay).padStart(2, '0')}`

  const fetchData = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)

      const [completionsRes, absencesRes] = await Promise.all([
        api.completions.list(habitId, startDate, endDate),
        api.absences.list(habitId, startDate, endDate),
      ])

      setCompletions(new Set(completionsRes.completions))
      setAbsences(
        new Map(absencesRes.absences.map((a: AbsenceItem) => [a.date, a.reason]))
      )
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch calendar data')
    } finally {
      setLoading(false)
    }
  }, [habitId, startDate, endDate])

  useEffect(() => {
    fetchData()
  }, [fetchData])

  const toggleCompletion = useCallback(
    async (date: string, isCompleted: boolean) => {
      if (isCompleted) {
        await api.habits.uncomplete(habitId, date)
      } else {
        await api.habits.complete(habitId, date)
      }
      await fetchData()
    },
    [habitId, fetchData]
  )

  const addAbsence = useCallback(
    async (date: string, reason?: string) => {
      await api.absences.create(habitId, { date, reason })
      await fetchData()
    },
    [habitId, fetchData]
  )

  const removeAbsence = useCallback(
    async (date: string) => {
      await api.absences.delete(habitId, date)
      await fetchData()
    },
    [habitId, fetchData]
  )

  return {
    completions,
    absences,
    loading,
    error,
    refetch: fetchData,
    toggleCompletion,
    addAbsence,
    removeAbsence,
    year,
    month,
    setYear,
    setMonth,
  }
}
