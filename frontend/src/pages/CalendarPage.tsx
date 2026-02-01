import { useState } from 'react'
import { useCalendarData } from '@/hooks/useCalendarData'
import { useToast } from '@/hooks/useToast'
import Calendar from '@/components/Calendar'
import Modal from '@/components/Modal'
import Button from '@/components/Button'
import AbsenceForm from '@/components/AbsenceForm'

interface CalendarPageProps {
  habitId: string
  habitName: string
  onBack: () => void
}

function CalendarPage({ habitId, habitName, onBack }: CalendarPageProps) {
  const today = new Date()

  const {
    completions,
    absences,
    loading,
    error,
    toggleCompletion,
    addAbsence,
    removeAbsence,
    year,
    month,
    setYear,
    setMonth,
  } = useCalendarData(habitId, today.getFullYear(), today.getMonth())

  const { showToast } = useToast()
  const [absenceDate, setAbsenceDate] = useState<string | null>(null)

  const handlePreviousMonth = () => {
    if (month === 0) {
      setYear(year - 1)
      setMonth(11)
    } else {
      setMonth(month - 1)
    }
  }

  const handleNextMonth = () => {
    if (month === 11) {
      setYear(year + 1)
      setMonth(0)
    } else {
      setMonth(month + 1)
    }
  }

  const handleToday = () => {
    const now = new Date()
    setYear(now.getFullYear())
    setMonth(now.getMonth())
  }

  const handleToggleCompletion = async (date: string, isCompleted: boolean) => {
    try {
      await toggleCompletion(date, isCompleted)
      showToast(
        isCompleted ? 'Completion removed' : 'Marked as complete',
        'success'
      )
    } catch {
      showToast('Failed to update completion', 'error')
    }
  }

  const handleToggleAbsence = (date: string, isAbsent: boolean) => {
    if (isAbsent) {
      // Remove absence
      handleRemoveAbsence(date)
    } else {
      // Show form to add absence
      setAbsenceDate(date)
    }
  }

  const handleAddAbsence = async (reason?: string) => {
    if (!absenceDate) return
    try {
      await addAbsence(absenceDate, reason)
      showToast('Marked as absent', 'success')
      setAbsenceDate(null)
    } catch {
      showToast('Failed to mark absence', 'error')
    }
  }

  const handleRemoveAbsence = async (date: string) => {
    try {
      await removeAbsence(date)
      showToast('Absence removed', 'success')
    } catch {
      showToast('Failed to remove absence', 'error')
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading calendar...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-4xl mb-4">{'\u{26A0}\u{FE0F}'}</div>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">
            Something went wrong
          </h2>
          <p className="text-gray-500 mb-4">{error}</p>
          <Button onClick={onBack}>Go Back</Button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-2xl mx-auto px-4 py-6">
          <div className="flex items-center gap-4">
            <button
              onClick={onBack}
              className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
              aria-label="Go back"
            >
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">{habitName}</h1>
              <p className="text-sm text-gray-500 mt-1">Calendar View</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-2xl mx-auto px-4 py-6">
        <Calendar
          year={year}
          month={month}
          completions={completions}
          absences={absences}
          onToggleCompletion={handleToggleCompletion}
          onToggleAbsence={handleToggleAbsence}
          onPreviousMonth={handlePreviousMonth}
          onNextMonth={handleNextMonth}
          onToday={handleToday}
          loading={loading}
        />
      </main>

      {/* Absence Modal */}
      <Modal
        isOpen={Boolean(absenceDate)}
        onClose={() => setAbsenceDate(null)}
        title="Mark Absence"
      >
        {absenceDate && (
          <AbsenceForm
            date={absenceDate}
            onSubmit={handleAddAbsence}
            onCancel={() => setAbsenceDate(null)}
          />
        )}
      </Modal>
    </div>
  )
}

export default CalendarPage
