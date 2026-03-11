'use client'

import { useState, useMemo } from 'react'
import {
  ArrowLeft, Download, Search, MoreVertical,
  ArrowDown, ArrowUp, EyeOff, Pin, Maximize, Eye
} from 'lucide-react'
import { useNavigation } from '@/components/navigation-provider'
import { DISPLAY_COLS } from '@/lib/types'
import type { OrderRow } from '@/lib/types'

interface DetailViewProps {
  title: string
  orders: OrderRow[]
}

const COLUMN_LABELS: Record<string, string> = {
  order_number: 'Order',
  fleek_id: 'Fleek ID',
  customer_name: 'Customer',
  customer_country: 'Country',
  vendor: 'Vendor',
  item_name: 'Item',
  total_order_line_amount: 'Amount',
  product_brand: 'Brand',
  logistics_partner_name: 'Logistics',
  aging_days: 'Days',
  aging_bucket: 'Bucket',
}

export function DetailView({ title, orders }: DetailViewProps) {
  const nav = useNavigation()
  const [search, setSearch] = useState('')
  const [country, setCountry] = useState('All Countries')

  // --- Advanced Table States ---
  const [openMenu, setOpenMenu] = useState<string | null>(null)
  const [sortConfig, setSortConfig] = useState<{ key: string; dir: 'asc' | 'desc' } | null>(null)
  const [hiddenCols, setHiddenCols] = useState<Set<string>>(new Set())
  const [pinnedCols, setPinnedCols] = useState<Record<string, 'left' | 'right'>>({})
  const [autoSizedCols, setAutoSizedCols] = useState<Set<string>>(new Set())

  const countries = useMemo(
    () => ['All Countries', ...Array.from(new Set(orders.map(r => r.customer_country).filter(Boolean))).sort()],
    [orders]
  )

  // 1. Filter the Data
  const filtered = useMemo(() => {
    let result = orders
    const s = search.toLowerCase()
    if (s) {
      result = result.filter(
        r =>
          r.order_number.toLowerCase().includes(s) ||
          r.customer_name.toLowerCase().includes(s) ||
          r.vendor.toLowerCase().includes(s)
      )
    }
    if (country !== 'All Countries') {
      result = result.filter(r => r.customer_country === country)
    }
    return result
  }, [orders, search, country])

  // 2. Sort the Data (TypeScript Fix Applied Here)
  const sortedAndFiltered = useMemo(() => {
    let res = [...filtered]
    if (sortConfig) {
      res.sort((a, b) => {
        const valA = String(a[sortConfig.key as keyof OrderRow] || '').toLowerCase()
        const valB = String(b[sortConfig.key as keyof OrderRow] || '').toLowerCase()
        if (valA < valB) return sortConfig.dir === 'asc' ? -1 : 1
        if (valA > valB) return sortConfig.dir === 'asc' ? 1 : -1
        return 0
      })
    }
    return res
  }, [filtered, sortConfig])

  // 3. Visible & Pinned Columns
  const activeCols = useMemo(() => {
    const visible = DISPLAY_COLS.filter(c => !hiddenCols.has(c))
    const left = visible.filter(c => pinnedCols[c] === 'left')
    const center = visible.filter(c => !pinnedCols[c])
    return [...left, ...center]
  }, [hiddenCols, pinnedCols])

  const downloadCSV = () => {
    const header = activeCols.map(c => COLUMN_LABELS[c] || c).join(',')
    const rows = sortedAndFiltered.map(r => activeCols.map(c => `"${String(r[c as keyof OrderRow] || '').replace(/"/g, '""')}"`).join(','))
    const csv = [header, ...rows].join('\n')
    const blob = new Blob([csv], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'orders_export.csv'
    a.click()
    URL.revokeObjectURL(url)
  }

  // --- Actions ---
  const handleSort = (col: string, dir: 'asc' | 'desc') => { setSortConfig({ key: col, dir }); setOpenMenu(null); }
  const handleHide = (col: string) => { setHiddenCols(p => { const n = new Set(p); n.add(col); return n; }); setOpenMenu(null); }
  const handleAutoSize = (col: string) => { setAutoSizedCols(p => { const n = new Set(p); if (n.has(col)) n.delete(col); else n.add(col); return n; }); setOpenMenu(null); }
  const handlePin = (col: string, pos: 'left' | null) => { setPinnedCols(p => { const n = { ...p }; if (pos) n[col] = pos; else delete n[col]; return n; }); setOpenMenu(null); }

  return (
    <div className="relative">
      {openMenu && <div className="fixed inset-0 z-40" onClick={() => setOpenMenu(null)} />}

      <div className="mb-6">
        <button
          onClick={() => nav.goHome()}
          className="mb-3 flex items-center gap-1.5 text-sm text-muted-foreground transition-colors hover:text-foreground"
        >
          <ArrowLeft className="h-4 w-4" />
          <span>Back to Dashboard</span>
        </button>
        <h1 className="text-2xl font-bold text-foreground">{title}</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          {sortedAndFiltered.length.toLocaleString()} orders found
        </p>
      </div>

      <div className="mb-4 flex flex-col gap-3 sm:flex-row sm:items-center">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search order, customer or vendor..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="w-full rounded-lg border border-border bg-input py-2 pl-10 pr-4 text-sm text-foreground placeholder:text-muted-foreground focus:border-ring focus:outline-none focus:ring-1 focus:ring-ring"
          />
        </div>
        <select
          value={country}
          onChange={e => setCountry(e.target.value)}
          className="rounded-lg border border-border bg-input px-3 py-2 text-sm text-foreground focus:border-ring focus:outline-none"
        >
          {countries.map(c => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>

        {hiddenCols.size > 0 && (
          <button
            onClick={() => setHiddenCols(new Set())}
            className="flex items-center gap-2 rounded-lg bg-secondary px-4 py-2 text-sm font-medium text-secondary-foreground transition-colors hover:bg-secondary/80"
          >
            <Eye className="h-4 w-4" />
            Show Hidden ({hiddenCols.size})
          </button>
        )}

        <button
          onClick={downloadCSV}
          className="flex items-center gap-2 rounded-lg bg-success px-4 py-2 text-sm font-semibold text-success-foreground transition-colors hover:bg-success/90"
        >
          <Download className="h-4 w-4" />
          Export CSV
        </button>
      </div>

      <div className="overflow-x-auto rounded-xl border border-border bg-card shadow-sm">
        <table className="w-full min-w-[900px] border-collapse">
          <thead>
            <tr className="border-b border-border bg-muted/20">
              {activeCols.map(col => {
                const isPinned = pinnedCols[col] === 'left'
                return (
                  <th
                    key={col}
                    className={`relative px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-muted-foreground transition-colors hover:bg-muted/50 ${isPinned ? 'sticky left-0 z-30 bg-card shadow-[2px_0_5px_-2px_rgba(0,0,0,0.3)]' : 'bg-transparent'
                      }`}
                  >
                    <div className="flex items-center justify-between gap-2">
                      <span className="flex items-center gap-1">
                        {COLUMN_LABELS[col] || col}
                        {sortConfig?.key === col && (
                          sortConfig.dir === 'asc' ? <ArrowDown size={12} className="text-primary" /> : <ArrowUp size={12} className="text-primary" />
                        )}
                      </span>
                      <button
                        onClick={() => setOpenMenu(openMenu === col ? null : col)}
                        className="rounded hover:bg-accent p-1 text-muted-foreground hover:text-foreground"
                      >
                        <MoreVertical size={14} />
                      </button>
                    </div>

                    {openMenu === col && (
                      <div className="absolute left-4 top-full mt-1 w-48 rounded-lg border border-border bg-popover py-1.5 shadow-xl z-50">
                        <button onClick={() => handleSort(col, 'asc')} className="flex w-full items-center gap-2 px-3 py-2 text-sm text-foreground hover:bg-accent">
                          <ArrowDown size={14} /> Sort A to Z
                        </button>
                        <button onClick={() => handleSort(col, 'desc')} className="flex w-full items-center gap-2 px-3 py-2 text-sm text-foreground hover:bg-accent">
                          <ArrowUp size={14} /> Sort Z to A
                        </button>
                        <div className="my-1 h-px bg-border" />
                        <button onClick={() => handleAutoSize(col)} className="flex w-full items-center gap-2 px-3 py-2 text-sm text-foreground hover:bg-accent">
                          <Maximize size={14} /> {autoSizedCols.has(col) ? 'Reset Size' : 'Auto-size'}
                        </button>
                        {isPinned ? (
                          <button onClick={() => handlePin(col, null)} className="flex w-full items-center gap-2 px-3 py-2 text-sm text-foreground hover:bg-accent">
                            <Pin size={14} className="rotate-45 opacity-50" /> Unpin Column
                          </button>
                        ) : (
                          <button onClick={() => handlePin(col, 'left')} className="flex w-full items-center gap-2 px-3 py-2 text-sm text-foreground hover:bg-accent">
                            <Pin size={14} /> Pin to Left
                          </button>
                        )}
                        <div className="my-1 h-px bg-border" />
                        <button onClick={() => handleHide(col)} className="flex w-full items-center gap-2 px-3 py-2 text-sm text-destructive hover:bg-destructive/10">
                          <EyeOff size={14} /> Hide Column
                        </button>
                      </div>
                    )}
                  </th>
                )
              })}
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {sortedAndFiltered.slice(0, 100).map((row, i) => (
              <tr key={i} className="group transition-colors hover:bg-accent/30">
                {activeCols.map(col => {
                  const isPinned = pinnedCols[col] === 'left'
                  const isAutoSize = autoSizedCols.has(col)
                  return (
                    <td
                      key={col}
                      className={`px-4 py-3 text-sm text-foreground ${isPinned ? 'sticky left-0 z-20 bg-card shadow-[2px_0_5px_-2px_rgba(0,0,0,0.3)] group-hover:bg-accent/30' : 'bg-transparent'
                        } ${!isAutoSize ? 'max-w-[200px] truncate whitespace-nowrap' : 'whitespace-nowrap'}`}
                    >
                      {col === 'aging_days' ? (
                        <span className="font-mono tabular-nums">{String(row[col as keyof OrderRow] || '')}</span>
                      ) : (
                        String(row[col as keyof OrderRow] || '')
                      )}
                    </td>
                  )
                })}
              </tr>
            ))}
          </tbody>
        </table>

        {sortedAndFiltered.length === 0 && (
          <div className="py-12 text-center text-sm text-muted-foreground">No orders found matching your filters.</div>
        )}
        {sortedAndFiltered.length > 100 && (
          <div className="border-t border-border px-4 py-3 text-center text-xs text-muted-foreground">
            Showing 100 of {sortedAndFiltered.length.toLocaleString()} orders
          </div>
        )}
      </div>
    </div>
  )
}