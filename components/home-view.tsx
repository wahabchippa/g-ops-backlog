'use client'

import type { DashboardData } from '@/lib/types'
import { useNavigation } from '@/components/navigation-provider'
import { groupByBucket } from '@/lib/dashboard-utils'
import { MetricCard } from '@/components/metric-card'
import { SearchBox } from '@/components/search-box'
import { AgingAnalysis } from '@/components/aging-analysis'
import { VendorList } from '@/components/vendor-list'
import { Zap } from 'lucide-react'

interface HomeViewProps {
  data: DashboardData
}

export function HomeView({ data }: HomeViewProps) {
  const nav = useNavigation()

  const pkBuckets = groupByBucket(data.pk_normal)
  const qcBuckets = groupByBucket(data.qc_normal)
  const handoverBuckets = groupByBucket(data.handover)

  const updatedAt = data.updated_at
    ? new Date(data.updated_at).toLocaleString('en-US', {
        day: 'numeric',
        month: 'short',
        year: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
      })
    : ''

  return (
    <div>
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-success text-success-foreground">
            <Zap className="h-5 w-5" />
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight text-foreground">
            G-Ops Backlog Dashboard
          </h1>
        </div>
        <p className="mt-2 text-sm text-muted-foreground">
          Real-time Operations Monitoring &middot; Last updated: {updatedAt}
        </p>
      </div>

      {/* Search */}
      <div className="mb-8">
        <SearchBox allData={data.all_data} />
      </div>

      {/* KPIs */}
      <div className="mb-8 grid grid-cols-2 gap-4 lg:grid-cols-4">
        <MetricCard label="Total Approved" value={data.approved.length} />
        <MetricCard label="PK Zone" value={data.pk_zone.length} />
        <MetricCard label="QC Center" value={data.qc_center.length} />
        <MetricCard label="Handover" value={data.handover.length} variant="warning" />
      </div>

      {/* Category Cards */}
      <div className="mb-8 grid grid-cols-1 gap-4 md:grid-cols-3">
        {/* Handover */}
        <div className="rounded-xl border border-warning/20 bg-warning/5 p-6">
          <h3 className="mb-1 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            Handover
          </h3>
          <p className="text-sm text-muted-foreground">To Logistics Partner</p>
          <p className="mt-3 text-4xl font-extrabold tabular-nums text-warning">
            {data.handover.length.toLocaleString()}
          </p>
          <button
            onClick={() => nav.goTo('handover')}
            className="mt-4 w-full rounded-lg border border-border bg-secondary px-4 py-2 text-sm font-medium text-foreground transition-colors hover:bg-accent"
          >
            View Details
          </button>
        </div>

        {/* PK Zone */}
        <div className="rounded-xl border border-success/20 bg-success/5 p-6">
          <h3 className="mb-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            PK Zone
          </h3>
          <div className="grid grid-cols-2 gap-3">
            <div className="text-center">
              <p className="text-xs text-muted-foreground">Normal</p>
              <p className="text-2xl font-extrabold tabular-nums text-success">
                {data.pk_normal.length.toLocaleString()}
              </p>
              <button
                onClick={() => nav.goTo('pk_normal')}
                className="mt-2 w-full rounded-md border border-border bg-secondary px-2 py-1.5 text-xs font-medium text-foreground transition-colors hover:bg-accent"
              >
                View
              </button>
            </div>
            <div className="text-center">
              <p className="text-xs text-muted-foreground">AI Orders</p>
              <p className="text-2xl font-extrabold tabular-nums text-success">
                {data.pk_ai.length.toLocaleString()}
              </p>
              <button
                onClick={() => nav.goTo('pk_ai')}
                className="mt-2 w-full rounded-md border border-border bg-secondary px-2 py-1.5 text-xs font-medium text-foreground transition-colors hover:bg-accent"
              >
                View
              </button>
            </div>
          </div>
        </div>

        {/* QC Center */}
        <div className="rounded-xl border border-success/20 bg-success/5 p-6">
          <h3 className="mb-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            QC Center
          </h3>
          <div className="grid grid-cols-2 gap-3">
            <div className="text-center">
              <p className="text-xs text-muted-foreground">Normal</p>
              <p className="text-2xl font-extrabold tabular-nums text-success">
                {data.qc_normal.length.toLocaleString()}
              </p>
              <button
                onClick={() => nav.goTo('qc_normal')}
                className="mt-2 w-full rounded-md border border-border bg-secondary px-2 py-1.5 text-xs font-medium text-foreground transition-colors hover:bg-accent"
              >
                View
              </button>
            </div>
            <div className="text-center">
              <p className="text-xs text-muted-foreground">AI Orders</p>
              <p className="text-2xl font-extrabold tabular-nums text-success">
                {data.qc_ai.length.toLocaleString()}
              </p>
              <button
                onClick={() => nav.goTo('qc_ai')}
                className="mt-2 w-full rounded-md border border-border bg-secondary px-2 py-1.5 text-xs font-medium text-foreground transition-colors hover:bg-accent"
              >
                View
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Aging */}
      <div className="mb-8">
        <AgingAnalysis
          pkBuckets={pkBuckets}
          qcBuckets={qcBuckets}
          handoverBuckets={handoverBuckets}
          pkTotal={data.pk_normal.length}
          qcTotal={data.qc_normal.length}
          handoverTotal={data.handover.length}
        />
      </div>

      {/* Vendor List */}
      <VendorList orders={data.pk_normal} zone="PK Zone" />
    </div>
  )
}
