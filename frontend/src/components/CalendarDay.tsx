interface CalendarDayProps {
  date: string // YYYY-MM-DD
  dayNumber: number
  isCurrentMonth: boolean
  isToday: boolean
  isCompleted: boolean
  isAbsent: boolean
  absenceReason?: string | null
  onToggleCompletion: () => void
  onToggleAbsence: () => void
  disabled?: boolean
}

function CalendarDay({
  date,
  dayNumber,
  isCurrentMonth,
  isToday,
  isCompleted,
  isAbsent,
  absenceReason,
  onToggleCompletion,
  onToggleAbsence,
  disabled = false,
}: CalendarDayProps) {
  const isFuture = new Date(date) > new Date()

  const getBackgroundClass = () => {
    if (!isCurrentMonth) return 'bg-gray-50 text-gray-300'
    if (isCompleted) return 'bg-green-500 text-white hover:bg-green-600'
    if (isAbsent) return 'bg-gray-300 text-gray-600 hover:bg-gray-400'
    if (isFuture) return 'bg-white text-gray-400'
    return 'bg-white text-gray-700 hover:bg-gray-100'
  }

  const handleClick = () => {
    if (disabled || !isCurrentMonth || isFuture) return
    onToggleCompletion()
  }

  const handleRightClick = (e: React.MouseEvent) => {
    e.preventDefault()
    if (disabled || !isCurrentMonth || isFuture) return
    onToggleAbsence()
  }

  return (
    <button
      onClick={handleClick}
      onContextMenu={handleRightClick}
      disabled={disabled || !isCurrentMonth || isFuture}
      className={`
        relative w-full aspect-square flex items-center justify-center
        text-sm font-medium rounded-lg transition-colors
        ${getBackgroundClass()}
        ${isToday ? 'ring-2 ring-indigo-500 ring-offset-1' : ''}
        ${disabled ? 'cursor-not-allowed opacity-50' : 'cursor-pointer'}
        focus:outline-none focus:ring-2 focus:ring-indigo-500
      `}
      title={absenceReason ? `Absent: ${absenceReason}` : undefined}
      aria-label={`${dayNumber}: ${isCompleted ? 'completed' : isAbsent ? 'absent' : 'not completed'}`}
    >
      {dayNumber}
      {isAbsent && !isCompleted && (
        <span className="absolute bottom-0.5 left-1/2 -translate-x-1/2 text-xs">
          {'\u{1F3D6}'} {/* beach umbrella */}
        </span>
      )}
    </button>
  )
}

export default CalendarDay
