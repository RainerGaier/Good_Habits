import { useState, useEffect } from 'react'
import type { HabitWithStats } from '@/types/habit'
import Button from './Button'

// Form data always has name (required) and description (optional)
interface HabitFormData {
  name: string
  description: string | null
}

interface HabitFormProps {
  habit?: HabitWithStats | null
  onSubmit: (data: HabitFormData) => Promise<void>
  onCancel: () => void
}

function HabitForm({ habit, onSubmit, onCancel }: HabitFormProps) {
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const isEditing = Boolean(habit)

  useEffect(() => {
    if (habit) {
      setName(habit.name)
      setDescription(habit.description || '')
    } else {
      setName('')
      setDescription('')
    }
  }, [habit])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!name.trim()) {
      setError('Name is required')
      return
    }

    if (name.length > 100) {
      setError('Name must be 100 characters or less')
      return
    }

    if (description.length > 500) {
      setError('Description must be 500 characters or less')
      return
    }

    setError(null)
    setIsSubmitting(true)

    try {
      await onSubmit({
        name: name.trim(),
        description: description.trim() || null,
      })
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save habit')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
          {error}
        </div>
      )}

      <div>
        <label
          htmlFor="habit-name"
          className="block text-sm font-medium text-gray-700 mb-1"
        >
          Habit Name <span className="text-red-500">*</span>
        </label>
        <input
          id="habit-name"
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="e.g., Morning Meditation"
          maxLength={100}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          autoFocus
        />
        <p className="text-xs text-gray-400 mt-1">{name.length}/100</p>
      </div>

      <div>
        <label
          htmlFor="habit-description"
          className="block text-sm font-medium text-gray-700 mb-1"
        >
          Description <span className="text-gray-400">(optional)</span>
        </label>
        <textarea
          id="habit-description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Add details about this habit..."
          maxLength={500}
          rows={3}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 resize-none"
        />
        <p className="text-xs text-gray-400 mt-1">{description.length}/500</p>
      </div>

      <div className="flex justify-end gap-3 pt-4">
        <Button
          type="button"
          variant="secondary"
          onClick={onCancel}
          disabled={isSubmitting}
        >
          Cancel
        </Button>
        <Button
          type="submit"
          variant="primary"
          disabled={isSubmitting || !name.trim()}
        >
          {isSubmitting ? 'Saving...' : isEditing ? 'Save Changes' : 'Create Habit'}
        </Button>
      </div>
    </form>
  )
}

export default HabitForm
