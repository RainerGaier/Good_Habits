import { useMemo } from 'react'
import CalendarDay from './CalendarDay'
import Button from './Button'

interface CalendarProps {
  year: number
  month: number
  completions: Set<string>
  absences: Map<string, string | null>
  onToggleCompletion: (date: string, isCompleted: boolean) => void
  onToggleAbsence: (date: string, isAbsent: boolean, reason?: string | null) => void
  onPreviousMonth: () => void
  onNextMonth: () => void
  onToday: () => void
  loading?: boolean
}

function Calendar({
  year,
  month,
  completions,
  absences,
  onToggleCompletion,
  onToggleAbsence,
  onPreviousMonth,
  onNextMonth,
  onToday,
  loading = false,
}: CalendarProps) {
  const currentDate = new Date(year, month, 1)
  const monthName = currentDate.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })

  const calendarDays = useMemo(() => {
    const days: Array<{
      date: string
      dayNumber: number
      isCurrentMonth: boolean
    }> = []

    // First day of the month
    const firstDay = new Date(year, month, 1)
    const startingDayOfWeek = firstDay.getDay()

    // Days from previous month
    const prevMonthLastDay = new Date(year, month, 0).getDate()
    for (let i = startingDayOfWeek - 1; i >= 0; i--) {
      const day = prevMonthLastDay - i
      const prevMonth = month === 0 ? 12 : month
      const prevYear = month === 0 ? year - 1 : year
      const date = `${prevYear}-${String(prevMonth).padStart(2, '0')}-${String(day).padStart(2, '0')}`
      days.push({ date, dayNumber: day, isCurrentMonth: false })
    }

    // Days in current month
    const daysInMonth = new Date(year, month + 1, 0).getDate()
    for (let day = 1; day <= daysInMonth; day++) {
      const date = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`
      days.push({ date, dayNumber: day, isCurrentMonth: true })
    }

    // Days from next month to fill grid (6 rows x 7 cols = 42)
    const remainingDays = 42 - days.length
    for (let day = 1; day <= remainingDays; day++) {
      const nextMonth = month === 11 ? 1 : month + 2
      const nextYear = month === 11 ? year + 1 : year
      const date = `${nextYear}-${String(nextMonth).padStart(2, '0')}-${String(day).padStart(2, '0')}`
      days.push({ date, dayNumber: day, isCurrentMonth: false })
    }

    return days
  }, [year, month])

  const today = new Date().toISOString().split('T')[0]

  const weekDays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

  return (
    <div className="bg-white rounded-lg shadow-md p-4">
      {/* Header with navigation */}
      <div className="flex items-center justify-between mb-4">
        <Button variant="ghost" size="sm" onClick={onPreviousMonth}>
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
        </Button>

        <div className="flex items-center gap-2">
          <h2 className="text-lg font-semibold text-gray-900">{monthName}</h2>
          <Button variant="ghost" size="sm" onClick={onToday}>
            Today
          </Button>
        </div>

        <Button variant="ghost" size="sm" onClick={onNextMonth}>
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </Button>
      </div>

      {/* Legend */}
      <div className="flex items-center justify-center gap-4 mb-4 text-xs text-gray-500">
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 rounded bg-green-500"></div>
          <span>Completed</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 rounded bg-gray-300"></div>
          <span>Absent</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 rounded bg-white border border-gray-200"></div>
          <span>Missed</span>
        </div>
      </div>

      {/* Weekday headers */}
      <div className="grid grid-cols-7 gap-1 mb-1">
        {weekDays.map((day) => (
          <div
            key={day}
            className="text-center text-xs font-medium text-gray-500 py-2"
          >
            {day}
          </div>
        ))}
      </div>

      {/* Calendar grid */}
      <div className="grid grid-cols-7 gap-1">
        {calendarDays.map(({ date, dayNumber, isCurrentMonth }) => {
          const isCompleted = completions.has(date)
          const isAbsent = absences.has(date)
          const absenceReason = absences.get(date)

          return (
            <CalendarDay
              key={date}
              date={date}
              dayNumber={dayNumber}
              isCurrentMonth={isCurrentMonth}
              isToday={date === today}
              isCompleted={isCompleted}
              isAbsent={isAbsent}
              absenceReason={absenceReason}
              onToggleCompletion={() => onToggleCompletion(date, isCompleted)}
              onToggleAbsence={() => onToggleAbsence(date, isAbsent, absenceReason)}
              disabled={loading}
            />
          )
        })}
      </div>

      {/* Instructions */}
      <p className="text-xs text-gray-400 text-center mt-4">
        Click to toggle completion. Right-click to mark absence.
      </p>
    </div>
  )
}

export default Calendar
