import * as React from "react"
import { cn } from "@/lib/utils"

interface AvatarProps {
  src?: string
  alt?: string
  fallback?: string
  size?: "xs" | "sm" | "md" | "lg" | "xl" | "2xl"
  status?: "online" | "offline" | "busy" | "away"
  className?: string
}

export const Avatar = React.forwardRef<HTMLDivElement, AvatarProps>(
  (
    {
      src,
      alt = "Avatar",
      fallback,
      size = "md",
      status,
      className,
    },
    ref
  ) => {
    const sizeClasses = {
      xs: "w-6 h-6 text-xs",
      sm: "w-8 h-8 h-8 text-sm",
      md: "w-10 h-10 text-base",
      lg: "w-12 h-12 text-lg",
      xl: "w-16 h-16 text-xl",
      "2xl": "w-20 h-20 text-2xl",
    }

    const statusClasses = {
      online: "bg-green-500",
      offline: "bg-gray-500",
      busy: "bg-red-500",
      away: "bg-yellow-500",
    }

    const baseClasses =
      "rounded-full bg-[#1A2230] border-2 border-[#1A2230] flex items-center justify-center text-white font-semibold overflow-hidden relative"

    const finalSize = sizeClasses[size]
    const finalClassName = cn(baseClasses, finalSize, className)

    if (src) {
      return (
        <div ref={ref} className="relative inline-block">
          <img src={src} alt={alt} className={finalClassName} />
          {status && (
            <div
              className={cn(
                "absolute bottom-0 right-0 w-3 h-3 rounded-full border-2 border-[#0B0F14]",
                statusClasses[status]
              )}
            />
          )}
        </div>
      )
    }

    return (
      <div ref={ref} className="relative inline-block">
        <div className={finalClassName}>{fallback || "?"}</div>
        {status && (
          <div
            className={cn(
              "absolute bottom-0 right-0 w-3 h-3 rounded-full border-2 border-[#0B0F14]",
              statusClasses[status]
            )}
          />
        )}
      </div>
    )
  }
)

Avatar.displayName = "Avatar"