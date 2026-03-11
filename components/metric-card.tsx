'use client'

import { cn } from '@/lib/utils'

interface MetricCardProps {
  label: string
  value: string | number
  variant?: 'default' | 'success' | 'warning'
  onClick?: () => void
}

export function MetricCard({ label, value, variant = 'default', onClick }: MetricCardProps) {
  const formatted = typeof value === 'number' ? value.toLocaleString() : value

  return (
    <button
      onClick={onClick}
      disabled={!onClick}
      className={cn(
        'group flex flex-col items-center justify-center rounded-xl border px-4 py-6 text-center transition-all',
        onClick && 'cursor-pointer hover:-translate-y-0.5 hover:shadow-lg',
        variant === 'default' && 'border-border bg-card',
        variant === 'success' && 'border-success/20 bg-success/5',
        variant === 'warning' && 'border-warning/20 bg-warning/5'
      )}
    >
      <p className="text-xs font-semibold uppercase tracking-widest text-muted-foreground">
        {label}
      </p>
      <p
        className={cn(
          'mt-2 text-3xl font-extrabold tabular-nums',
          variant === 'default' && 'text-foreground',
          variant === 'success' && 'text-success',
          variant === 'warning' && 'text-warning'
        )}
      >
        {formatted}
      </p>
    </button>
  )
}
