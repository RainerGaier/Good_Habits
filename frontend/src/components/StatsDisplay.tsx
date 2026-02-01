import type { CompletionRate } from '@/types/habit'

interface StatsDisplayProps {
  stats: CompletionRate
}

function StatsDisplay({ stats }: StatsDisplayProps) {
  const getColorClass = (rate: number): string => {
    if (rate >= 80) return 'text-green-600'
    if (rate >= 50) return 'text-yellow-600'
    return 'text-red-500'
  }

  const formatRate = (rate: number): string => {
    return `${Math.round(rate)}%`
  }

  return (
    <div className="flex items-center gap-4 text-sm">
      <div className="flex flex-col items-center">
        <span className={`font-semibold ${getColorClass(stats.week)}`}>
          {formatRate(stats.week)}
        </span>
        <span className="text-xs text-gray-400">week</span>
      </div>

      <div className="flex flex-col items-center">
        <span className={`font-semibold ${getColorClass(stats.month)}`}>
          {formatRate(stats.month)}
        </span>
        <span className="text-xs text-gray-400">month</span>
      </div>

      <div className="flex flex-col items-center">
        <span className={`font-semibold ${getColorClass(stats.all_time)}`}>
          {formatRate(stats.all_time)}
        </span>
        <span className="text-xs text-gray-400">all time</span>
      </div>
    </div>
  )
}

export default StatsDisplay
