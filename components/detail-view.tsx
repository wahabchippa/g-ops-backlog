'use client'

import { useState, useMemo } from 'react'
import { ArrowLeft, Download, Search } from 'lucide-react'
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

  const countries = useMemo(
    () => ['All Countries', ...Array.from(new Set(orders.map(r => r.customer_country).filter(Boolean))).sort()],
    [orders]
  )

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

  const downloadCSV = () => {
    const header = DISPLAY_COLS.join(',')
    const rows = filtered.map(r => DISPLAY_COLS.map(c => `"${String(r[c]).replace(/"/g, '""')}"`).join(','))
    const csv = [header, ...rows].join('\n')
    const blob = new Blob([csv], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'orders.csv'
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div>
      {/* Back + Title */}
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
          {orders.length.toLocaleString()} orders found
        </p>
      </div>

      {/* Filters */}
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
        <button
          onClick={downloadCSV}
          className="flex items-center gap-2 rounded-lg bg-success px-4 py-2 text-sm font-semibold text-success-foreground transition-colors hover:bg-success/90"
        >
          <Download className="h-4 w-4" />
          Export CSV
        </button>
      </div>

      {/* Table */}
      <div className="overflow-x-auto rounded-xl border border-border bg-card">
        <table className="w-full min-w-[900px]">
          <thead>
            <tr className="border-b border-border">
              {DISPLAY_COLS.map(col => (
                <th
                  key={col}
                  className="whitespace-nowrap px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-muted-foreground"
                >
                  {COLUMN_LABELS[col] || col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {filtered.slice(0, 100).map((row, i) => (
              <tr key={i} className="transition-colors hover:bg-accent/50">
                {DISPLAY_COLS.map(col => (
                  <td key={col} className="max-w-[200px] truncate whitespace-nowrap px-4 py-2.5 text-sm text-foreground">
                    {col === 'aging_days' ? (
                      <span className="font-mono tabular-nums">{String(row[col])}</span>
                    ) : (
                      String(row[col])
                    )}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
        {filtered.length === 0 && (
          <div className="py-12 text-center text-sm text-muted-foreground">No orders found</div>
        )}
        {filtered.length > 100 && (
          <div className="border-t border-border px-4 py-3 text-center text-xs text-muted-foreground">
            Showing 100 of {filtered.length.toLocaleString()} orders
          </div>
        )}
      </div>
    </div>
  )
}
