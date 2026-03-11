'use client'

import { useState } from 'react'
import { useNavigation } from '@/components/navigation-provider'
import { groupByVendor } from '@/lib/dashboard-utils'
import { VENDOR_ACTION_OPTIONS } from '@/lib/types'
import type { OrderRow } from '@/lib/types'

interface VendorListProps {
  orders: OrderRow[]
  zone: string
}

export function VendorList({ orders, zone }: VendorListProps) {
  const nav = useNavigation()
  const vendors = groupByVendor(orders)
  const [comments, setComments] = useState<Record<string, string>>({})

  return (
    <div>
      <h2 className="mb-4 text-lg font-semibold text-foreground">PK Zone Vendors</h2>
      <div className="overflow-hidden rounded-xl border border-border bg-card">
        {/* Header */}
        <div className="grid grid-cols-[1fr_80px_140px] gap-2 border-b border-border px-4 py-3">
          <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            Vendor Name
          </span>
          <span className="text-center text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            Qty
          </span>
          <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            Action
          </span>
        </div>

        {/* Rows */}
        <div className="divide-y divide-border">
          {vendors.map((v, i) => (
            <div key={i} className="grid grid-cols-[1fr_80px_140px] items-center gap-2 px-4 py-2.5">
              <span className="truncate text-sm text-foreground">{v.vendor}</span>
              <button
                onClick={() =>
                  nav.goTo('vendor_detail', {
                    vendorName: v.vendor,
                    vendorZone: zone,
                  })
                }
                className="text-center font-mono text-sm font-semibold tabular-nums text-foreground transition-colors hover:text-success"
              >
                {v.count}
              </button>
              <select
                value={comments[v.vendor] || '--'}
                onChange={e => setComments(prev => ({ ...prev, [v.vendor]: e.target.value }))}
                className="rounded-md border border-border bg-input px-2 py-1 text-xs text-foreground focus:border-ring focus:outline-none"
              >
                {VENDOR_ACTION_OPTIONS.map(opt => (
                  <option key={opt} value={opt}>
                    {opt}
                  </option>
                ))}
              </select>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="border-t border-border px-4 py-3">
          <p className="text-xs text-muted-foreground">
            {vendors.length} vendors &middot; {orders.length.toLocaleString()} total orders
          </p>
        </div>
      </div>
    </div>
  )
}
