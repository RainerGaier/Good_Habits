import Button from './Button'

interface EmptyStateProps {
  onCreateClick: () => void
}

function EmptyState({ onCreateClick }: EmptyStateProps) {
  return (
    <div className="text-center py-12">
      <div className="text-6xl mb-4">{'\u{1F4DD}'}</div>
      <h3 className="text-xl font-semibold text-gray-900 mb-2">No habits yet</h3>
      <p className="text-gray-500 mb-6 max-w-sm mx-auto">
        Start building positive daily routines by creating your first habit.
      </p>
      <Button onClick={onCreateClick} variant="primary" size="lg">
        Create Your First Habit
      </Button>
    </div>
  )
}

export default EmptyState
