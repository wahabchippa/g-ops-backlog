'use client'

import { useNavigation } from '@/components/navigation-provider'
import { useDashboardData } from '@/hooks/use-dashboard-data'
import { groupByBucket } from '@/lib/dashboard-utils'
import { BUCKET_ORDER } from '@/lib/types'
import {
  Home,
  Package,
  MapPin,
  Building2,
  Bot,
  FileText,
  Clock,
  Truck,
  X,
  ChevronDown,
  ChevronRight,
} from 'lucide-react'
import { useState } from 'react'

function AgingDropdown({
  label,
  icon: Icon,
  buckets,
  onSelect,
}: {
  label: string
  icon: typeof Clock
  buckets: Record<string, number>
  onSelect: (bucket: string) => void
}) {
  const [open, setOpen] = useState(false)
  const total = Object.values(buckets).reduce((s, n) => s + n, 0)

  if (total === 0) return null

  return (
    <div>
      <button
        onClick={() => setOpen(!open)}
        className="flex w-full items-center gap-2 rounded-md px-3 py-2 text-sm text-muted-foreground transition-colors hover:bg-accent hover:text-foreground"
      >
        <Icon className="h-4 w-4 shrink-0" />
        <span className="flex-1 truncate text-left">{label}</span>
        <span className="text-xs text-muted-foreground">{total}</span>
        {open ? <ChevronDown className="h-3.5 w-3.5" /> : <ChevronRight className="h-3.5 w-3.5" />}
      </button>
      {open && (
        <div className="ml-6 mt-1 space-y-0.5">
          {BUCKET_ORDER.map(b => {
            const count = buckets[b] || 0
            if (count === 0) return null
            return (
              <button
                key={b}
                onClick={() => onSelect(b)}
                className="flex w-full items-center justify-between rounded px-3 py-1.5 text-xs text-muted-foreground transition-colors hover:bg-accent hover:text-foreground"
              >
                <span>{b}</span>
                <span className="font-mono text-xs tabular-nums">{count}</span>
              </button>
            )
          })}
        </div>
      )}
    </div>
  )
}

export function DashboardSidebar() {
  const nav = useNavigation()
  const { data, isLoading } = useDashboardData()

  if (!data || isLoading) return null

  const pkNormalBuckets = groupByBucket(data.pk_normal ?? [])
  const qcNormalBuckets = groupByBucket(data.qc_normal ?? [])
  const handoverBuckets = groupByBucket(data.handover ?? [])

  const navItems = [
    { label: 'Dashboard', icon: Home, page: 'home' as const },
  ]

  return (
    <aside className="flex h-screen w-64 shrink-0 flex-col border-r border-sidebar-border bg-sidebar overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-sidebar-border px-4 py-4">
        <div className="flex items-center gap-2.5">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-success text-success-foreground">
            <Truck className="h-4 w-4" />
          </div>
          <span className="text-sm font-semibold text-sidebar-foreground">G-Ops</span>
        </div>
        <button
          onClick={() => nav.setSidebarOpen(false)}
          className="rounded-md p-1.5 text-muted-foreground transition-colors hover:bg-accent hover:text-foreground lg:hidden"
        >
          <X className="h-4 w-4" />
        </button>
      </div>

      {/* Nav */}
      <nav className="flex-1 overflow-y-auto px-3 py-4">
        <div className="space-y-1">
          {navItems.map(item => (
            <button
              key={item.page}
              onClick={() => nav.goTo(item.page)}
              className={`flex w-full items-center gap-2 rounded-md px-3 py-2 text-sm transition-colors ${
                nav.page === item.page
                  ? 'bg-accent text-foreground font-medium'
                  : 'text-muted-foreground hover:bg-accent hover:text-foreground'
              }`}
            >
              <item.icon className="h-4 w-4 shrink-0" />
              <span>{item.label}</span>
            </button>
          ))}
        </div>

        {/* Handover Section */}
        <div className="mt-6">
          <p className="mb-2 px-3 text-xs font-semibold uppercase tracking-wider text-warning">
            Handover
          </p>
          <button
            onClick={() => nav.goTo('handover')}
            className={`flex w-full items-center gap-2 rounded-md px-3 py-2 text-sm transition-colors ${
              nav.page === 'handover'
                ? 'bg-accent text-foreground font-medium'
                : 'text-muted-foreground hover:bg-accent hover:text-foreground'
            }`}
          >
            <Package className="h-4 w-4 shrink-0" />
            <span className="flex-1 text-left">All Handover</span>
            <span className="text-xs font-mono tabular-nums text-muted-foreground">
              {(data?.handover?.length ?? 0).toLocaleString()}
            </span>
          </button>
        </div>

        {/* PK Zone Section */}
        <div className="mt-6">
          <p className="mb-2 px-3 text-xs font-semibold uppercase tracking-wider text-success">
            PK Zone
          </p>
          <div className="space-y-0.5">
            <button
              onClick={() => nav.goTo('pk_normal')}
              className={`flex w-full items-center gap-2 rounded-md px-3 py-2 text-sm transition-colors ${
                nav.page === 'pk_normal'
                  ? 'bg-accent text-foreground font-medium'
                  : 'text-muted-foreground hover:bg-accent hover:text-foreground'
              }`}
            >
              <FileText className="h-4 w-4 shrink-0" />
              <span className="flex-1 text-left">Normal</span>
              <span className="text-xs font-mono tabular-nums text-muted-foreground">
                {(data?.pk_normal?.length ?? 0).toLocaleString()}
              </span>
            </button>
            <button
              onClick={() => nav.goTo('pk_ai')}
              className={`flex w-full items-center gap-2 rounded-md px-3 py-2 text-sm transition-colors ${
                nav.page === 'pk_ai'
                  ? 'bg-accent text-foreground font-medium'
                  : 'text-muted-foreground hover:bg-accent hover:text-foreground'
              }`}
            >
              <Bot className="h-4 w-4 shrink-0" />
              <span className="flex-1 text-left">AI Orders</span>
              <span className="text-xs font-mono tabular-nums text-muted-foreground">
                {(data?.pk_ai?.length ?? 0).toLocaleString()}
              </span>
            </button>
          </div>
        </div>

        {/* QC Center Section */}
        <div className="mt-6">
          <p className="mb-2 px-3 text-xs font-semibold uppercase tracking-wider text-success">
            QC Center
          </p>
          <div className="space-y-0.5">
            <button
              onClick={() => nav.goTo('qc_normal')}
              className={`flex w-full items-center gap-2 rounded-md px-3 py-2 text-sm transition-colors ${
                nav.page === 'qc_normal'
                  ? 'bg-accent text-foreground font-medium'
                  : 'text-muted-foreground hover:bg-accent hover:text-foreground'
              }`}
            >
              <Building2 className="h-4 w-4 shrink-0" />
              <span className="flex-1 text-left">Normal</span>
              <span className="text-xs font-mono tabular-nums text-muted-foreground">
                {(data?.qc_normal?.length ?? 0).toLocaleString()}
              </span>
            </button>
            <button
              onClick={() => nav.goTo('qc_ai')}
              className={`flex w-full items-center gap-2 rounded-md px-3 py-2 text-sm transition-colors ${
                nav.page === 'qc_ai'
                  ? 'bg-accent text-foreground font-medium'
                  : 'text-muted-foreground hover:bg-accent hover:text-foreground'
              }`}
            >
              <Bot className="h-4 w-4 shrink-0" />
              <span className="flex-1 text-left">AI Orders</span>
              <span className="text-xs font-mono tabular-nums text-muted-foreground">
                {(data?.qc_ai?.length ?? 0).toLocaleString()}
              </span>
            </button>
          </div>
        </div>

        {/* Aging Section */}
        <div className="mt-6">
          <p className="mb-2 px-3 text-xs font-semibold uppercase tracking-wider text-[#3b82f6]">
            Aging Analysis
          </p>
          <div className="space-y-0.5">
            <AgingDropdown
              label="PK Zone"
              icon={MapPin}
              buckets={pkNormalBuckets}
              onSelect={(bucket) =>
                nav.goTo('aging_detail', { agingZone: 'PK Zone', agingBucket: bucket })
              }
            />
            <AgingDropdown
              label="QC Center"
              icon={Building2}
              buckets={qcNormalBuckets}
              onSelect={(bucket) =>
                nav.goTo('aging_detail', { agingZone: 'PK QC Center', agingBucket: bucket })
              }
            />
            <AgingDropdown
              label="Handover"
              icon={Truck}
              buckets={handoverBuckets}
              onSelect={(bucket) =>
                nav.goTo('handover_aging_detail', { handoverBucket: bucket })
              }
            />
          </div>
        </div>
      </nav>
    </aside>
  )
}
