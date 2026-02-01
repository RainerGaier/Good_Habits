import { useState } from 'react'
import Button from './Button'

interface AbsenceFormProps {
  date: string
  onSubmit: (reason?: string) => Promise<void>
  onCancel: () => void
}

function AbsenceForm({ date, onSubmit, onCancel }: AbsenceFormProps) {
  const [reason, setReason] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const formattedDate = new Date(date + 'T00:00:00').toLocaleDateString('en-US', {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    try {
      await onSubmit(reason.trim() || undefined)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <p className="text-gray-600">
        Mark <span className="font-semibold">{formattedDate}</span> as a planned absence?
      </p>

      <div>
        <label
          htmlFor="absence-reason"
          className="block text-sm font-medium text-gray-700 mb-1"
        >
          Reason <span className="text-gray-400">(optional)</span>
        </label>
        <input
          id="absence-reason"
          type="text"
          value={reason}
          onChange={(e) => setReason(e.target.value)}
          placeholder="e.g., Vacation, Sick day"
          maxLength={100}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          autoFocus
        />
      </div>

      <div className="flex justify-end gap-3 pt-2">
        <Button
          type="button"
          variant="secondary"
          onClick={onCancel}
          disabled={isSubmitting}
        >
          Cancel
        </Button>
        <Button type="submit" variant="primary" disabled={isSubmitting}>
          {isSubmitting ? 'Saving...' : 'Mark Absent'}
        </Button>
      </div>
    </form>
  )
}

export default AbsenceForm
