interface CompletionCheckboxProps {
  completed: boolean
  onToggle: () => void
  disabled?: boolean
}

function CompletionCheckbox({
  completed,
  onToggle,
  disabled = false,
}: CompletionCheckboxProps) {
  return (
    <button
      onClick={onToggle}
      disabled={disabled}
      className={`
        w-10 h-10 rounded-full border-2 flex items-center justify-center
        transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2
        ${
          completed
            ? 'bg-green-500 border-green-500 text-white hover:bg-green-600'
            : 'bg-white border-gray-300 text-gray-300 hover:border-green-400 hover:text-green-400'
        }
        ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
        focus:ring-green-500
      `}
      aria-label={completed ? 'Mark as incomplete' : 'Mark as complete'}
    >
      <svg
        className="w-6 h-6"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        strokeWidth={3}
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          d="M5 13l4 4L19 7"
        />
      </svg>
    </button>
  )
}

export default CompletionCheckbox
