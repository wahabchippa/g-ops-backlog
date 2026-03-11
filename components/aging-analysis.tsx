'use client'

import { BUCKET_ORDER } from '@/lib/types'
import { useNavigation } from '@/components/navigation-provider'
import type { PageView } from '@/lib/types'

interface AgingTableProps {
  title: string
  buckets: Record<string, number>
  total: number
  onBucketClick: (bucket: string) => void
}

function AgingColumn({ title, buckets, total, onBucketClick }: AgingTableProps) {
  return (
    <div className="rounded-xl border border-border bg-card">
      <div className="border-b border-border px-4 py-3">
        <h3 className="text-sm font-semibold text-foreground">{title}</h3>
      </div>
      <div className="divide-y divide-border">
        {BUCKET_ORDER.map(bucket => {
          const count = buckets[bucket] || 0
          return (
            <button
              key={bucket}
              onClick={() => count > 0 && onBucketClick(bucket)}
              disabled={count === 0}
              className="flex w-full items-center justify-between px-4 py-2 text-sm transition-colors hover:bg-accent disabled:cursor-default disabled:opacity-40"
            >
              <span className="text-muted-foreground">{bucket}</span>
              <span className="font-mono text-xs font-semibold tabular-nums text-foreground">
                {count}
              </span>
            </button>
          )
        })}
      </div>
      <div className="border-t border-border px-4 py-3">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Total</span>
          <span className="font-mono text-sm font-bold tabular-nums text-foreground">{total.toLocaleString()}</span>
        </div>
      </div>
    </div>
  )
}

interface AgingAnalysisProps {
  pkBuckets: Record<string, number>
  qcBuckets: Record<string, number>
  handoverBuckets: Record<string, number>
  pkTotal: number
  qcTotal: number
  handoverTotal: number
}

export function AgingAnalysis({ pkBuckets, qcBuckets, handoverBuckets, pkTotal, qcTotal, handoverTotal }: AgingAnalysisProps) {
  const nav = useNavigation()

  return (
    <div>
      <h2 className="mb-4 text-lg font-semibold text-foreground">Aging Analysis &mdash; Normal Orders</h2>
      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        <AgingColumn
          title="PK Zone"
          buckets={pkBuckets}
          total={pkTotal}
          onBucketClick={(b) => nav.goTo('aging_detail', { agingZone: 'PK Zone', agingBucket: b })}
        />
        <AgingColumn
          title="QC Center"
          buckets={qcBuckets}
          total={qcTotal}
          onBucketClick={(b) => nav.goTo('aging_detail', { agingZone: 'PK QC Center', agingBucket: b })}
        />
        <AgingColumn
          title="Handover"
          buckets={handoverBuckets}
          total={handoverTotal}
          onBucketClick={(b) => nav.goTo('handover_aging_detail', { handoverBucket: b })}
        />
      </div>
    </div>
  )
}
