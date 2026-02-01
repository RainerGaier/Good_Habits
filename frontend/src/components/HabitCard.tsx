import type { HabitWithStats } from '@/types/habit'
import CompletionCheckbox from './CompletionCheckbox'
import StreakBadge from './StreakBadge'
import StatsDisplay from './StatsDisplay'

interface HabitCardProps {
  habit: HabitWithStats
  onToggle: () => void
  onEdit: () => void
  onDelete: () => void
  isLoading?: boolean
}

function HabitCard({
  habit,
  onToggle,
  onEdit,
  onDelete,
  isLoading = false,
}: HabitCardProps) {
  return (
    <div
      className={`
      bg-white rounded-lg shadow-md p-4
      transition-all duration-200 hover:shadow-lg
      ${habit.completed_today ? 'border-l-4 border-green-500' : ''}
    `}
    >
      <div className="flex items-start gap-4">
        {/* Completion Toggle */}
        <div className="flex-shrink-0 pt-1">
          <CompletionCheckbox
            completed={habit.completed_today}
            onToggle={onToggle}
            disabled={isLoading}
          />
        </div>

        {/* Main Content */}
        <div className="flex-grow min-w-0">
          <div className="flex items-start justify-between gap-2">
            <div className="min-w-0">
              <h3
                className={`font-semibold text-lg truncate ${
                  habit.completed_today
                    ? 'text-gray-500 line-through'
                    : 'text-gray-900'
                }`}
              >
                {habit.name}
              </h3>
              {habit.description && (
                <p className="text-sm text-gray-500 mt-0.5 line-clamp-2">
                  {habit.description}
                </p>
              )}
            </div>

            {/* Actions Menu */}
            <div className="flex-shrink-0 flex items-center gap-1">
              <button
                onClick={onEdit}
                className="p-1.5 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded transition-colors"
                aria-label="Edit habit"
              >
                <svg
                  className="w-4 h-4"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"
                  />
                </svg>
              </button>
              <button
                onClick={onDelete}
                className="p-1.5 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded transition-colors"
                aria-label="Delete habit"
              >
                <svg
                  className="w-4 h-4"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                  />
                </svg>
              </button>
            </div>
          </div>

          {/* Stats Row */}
          <div className="flex items-center justify-between mt-3 pt-3 border-t border-gray-100">
            <StreakBadge
              currentStreak={habit.current_streak}
              bestStreak={habit.best_streak}
            />
            <StatsDisplay stats={habit.completion_rate} />
          </div>
        </div>
      </div>
    </div>
  )
}

export default HabitCard
