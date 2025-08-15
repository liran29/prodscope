import * as React from "react"
import { cn } from "../../lib/utils"

export interface ProgressProps extends React.HTMLAttributes<HTMLDivElement> {
  value?: number
  max?: number
  showLabel?: boolean
  label?: string
}

const Progress = React.forwardRef<HTMLDivElement, ProgressProps>(
  ({ className, value = 0, max = 100, showLabel = false, label, ...props }, ref) => {
    const percentage = Math.round((value / max) * 100)
    
    return (
      <div className="space-y-2">
        {(showLabel || label) && (
          <div className="flex justify-between text-sm">
            <span className="text-muted-foreground">{label}</span>
            <span className="text-muted-foreground">{percentage}%</span>
          </div>
        )}
        <div
          ref={ref}
          className={cn(
            "relative h-4 w-full overflow-hidden rounded-full bg-secondary",
            className
          )}
          {...props}
        >
          <div
            className="h-full w-full flex-1 bg-primary transition-all duration-500 ease-in-out"
            style={{ transform: `translateX(-${100 - percentage}%)` }}
          />
        </div>
      </div>
    )
  }
)
Progress.displayName = "Progress"

export { Progress }