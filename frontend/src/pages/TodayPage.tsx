import { useState } from 'react'
import { useHabits } from '@/hooks/useHabits'
import type { HabitWithStats } from '@/types/habit'
import HabitCard from '@/components/HabitCard'
import HabitForm from '@/components/HabitForm'
import Modal from '@/components/Modal'
import Button from '@/components/Button'
import EmptyState from '@/components/EmptyState'

function TodayPage() {
  const {
    habits,
    loading,
    error,
    createHabit,
    updateHabit,
    deleteHabit,
    toggleCompletion,
  } = useHabits()

  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false)
  const [editingHabit, setEditingHabit] = useState<HabitWithStats | null>(null)
  const [deletingHabit, setDeletingHabit] = useState<HabitWithStats | null>(null)
  const [actionLoading, setActionLoading] = useState<string | null>(null)

  const today = new Date()
  const formattedDate = today.toLocaleDateString('en-US', {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
  })

  const completedCount = habits.filter((h) => h.completed_today).length
  const totalCount = habits.length

  const handleCreateSubmit = async (data: {
    name: string
    description: string | null
  }) => {
    await createHabit(data)
    setIsCreateModalOpen(false)
  }

  const handleEditSubmit = async (data: {
    name: string
    description: string | null
  }) => {
    if (editingHabit) {
      await updateHabit(editingHabit.id, data)
      setEditingHabit(null)
    }
  }

  const handleDelete = async () => {
    if (deletingHabit) {
      await deleteHabit(deletingHabit.id)
      setDeletingHabit(null)
    }
  }

  const handleToggle = async (habit: HabitWithStats) => {
    setActionLoading(habit.id)
    try {
      await toggleCompletion(habit)
    } finally {
      setActionLoading(null)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading habits...</p>
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
          <Button onClick={() => window.location.reload()}>Try Again</Button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-2xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Today</h1>
              <p className="text-sm text-gray-500 mt-1">{formattedDate}</p>
            </div>
            {totalCount > 0 && (
              <div className="text-right">
                <p className="text-2xl font-bold text-indigo-600">
                  {completedCount}/{totalCount}
                </p>
                <p className="text-sm text-gray-500">completed</p>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-2xl mx-auto px-4 py-6">
        {habits.length === 0 ? (
          <EmptyState onCreateClick={() => setIsCreateModalOpen(true)} />
        ) : (
          <>
            {/* Add Habit Button */}
            <div className="mb-6">
              <Button
                onClick={() => setIsCreateModalOpen(true)}
                variant="primary"
                className="w-full"
              >
                + Add New Habit
              </Button>
            </div>

            {/* Habits List */}
            <div className="space-y-4">
              {habits.map((habit) => (
                <HabitCard
                  key={habit.id}
                  habit={habit}
                  onToggle={() => handleToggle(habit)}
                  onEdit={() => setEditingHabit(habit)}
                  onDelete={() => setDeletingHabit(habit)}
                  isLoading={actionLoading === habit.id}
                />
              ))}
            </div>
          </>
        )}
      </main>

      {/* Create Modal */}
      <Modal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        title="Create New Habit"
      >
        <HabitForm
          onSubmit={handleCreateSubmit}
          onCancel={() => setIsCreateModalOpen(false)}
        />
      </Modal>

      {/* Edit Modal */}
      <Modal
        isOpen={Boolean(editingHabit)}
        onClose={() => setEditingHabit(null)}
        title="Edit Habit"
      >
        <HabitForm
          habit={editingHabit}
          onSubmit={handleEditSubmit}
          onCancel={() => setEditingHabit(null)}
        />
      </Modal>

      {/* Delete Confirmation Modal */}
      <Modal
        isOpen={Boolean(deletingHabit)}
        onClose={() => setDeletingHabit(null)}
        title="Delete Habit"
      >
        <div className="space-y-4">
          <p className="text-gray-600">
            Are you sure you want to delete "
            <span className="font-semibold">{deletingHabit?.name}</span>"? This
            will also delete all completion history and cannot be undone.
          </p>
          <div className="flex justify-end gap-3">
            <Button variant="secondary" onClick={() => setDeletingHabit(null)}>
              Cancel
            </Button>
            <Button variant="danger" onClick={handleDelete}>
              Delete Habit
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  )
}

export default TodayPage
