interface StreakBadgeProps {
  currentStreak: number
  bestStreak: number
}

function StreakBadge({ currentStreak, bestStreak }: StreakBadgeProps) {
  const isHotStreak = currentStreak >= 7
  const isOnFire = currentStreak >= 30

  return (
    <div className="flex items-center gap-3">
      {/* Current Streak */}
      <div className="flex items-center gap-1">
        <span className={`text-lg ${isOnFire ? 'animate-pulse' : ''}`}>
          {isHotStreak ? '\u{1F525}' : '\u{26A1}'}
        </span>
        <span
          className={`font-bold ${currentStreak > 0 ? 'text-orange-600' : 'text-gray-400'}`}
        >
          {currentStreak}
        </span>
        <span className="text-sm text-gray-500">
          day{currentStreak !== 1 ? 's' : ''}
        </span>
      </div>

      {/* Best Streak */}
      {bestStreak > 0 && (
        <div className="flex items-center gap-1 text-sm text-gray-400">
          <span>{'\u{1F3C6}'}</span>
          <span>{bestStreak}</span>
        </div>
      )}
    </div>
  )
}

export default StreakBadge
