'use client'

import { useState } from 'react'
import { Search } from 'lucide-react'
import type { OrderRow } from '@/lib/types'
import { useNavigation } from '@/components/navigation-provider'

interface SearchBoxProps {
  allData: OrderRow[]
}

export function SearchBox({ allData }: SearchBoxProps) {
  const [query, setQuery] = useState('')
  const nav = useNavigation()

  const searchTerm = query.trim().toLowerCase()
  const hasSearch = searchTerm.length >= 3

  const orderMatches = hasSearch
    ? allData.filter(r => r.order_number.toLowerCase().includes(searchTerm))
    : []

  const vendorMatches = hasSearch
    ? allData.filter(r => r.vendor.toLowerCase().includes(searchTerm))
    : []

  const uniqueVendors = hasSearch && orderMatches.length === 0
    ? [...new Set(vendorMatches.map(r => r.vendor))].slice(0, 10)
    : []

  return (
    <div className="rounded-xl border border-border bg-card p-4">
      <div className="relative">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        <input
          type="text"
          placeholder="Search by order number or vendor name..."
          value={query}
          onChange={e => setQuery(e.target.value)}
          className="w-full rounded-lg border border-border bg-input py-2.5 pl-10 pr-4 text-sm text-foreground placeholder:text-muted-foreground focus:border-ring focus:outline-none focus:ring-1 focus:ring-ring"
        />
      </div>

      {hasSearch && orderMatches.length > 0 && (
        <div className="mt-4 space-y-2">
          <p className="text-sm font-semibold text-success">
            Found {orderMatches.length} order(s)
          </p>
          {orderMatches.slice(0, 5).map((order, i) => (
            <div key={i} className="rounded-lg border border-border bg-secondary/50 p-4">
              <div className="grid grid-cols-1 gap-x-8 gap-y-2 sm:grid-cols-2">
                <InfoRow label="Order" value={order.order_number} />
                <InfoRow label="Vendor" value={order.vendor} />
                <InfoRow label="Customer" value={order.customer_name} />
                <InfoRow label="Item" value={order.item_name.slice(0, 50)} />
                <InfoRow label="Amount" value={`$${order.total_order_line_amount}`} />
                <InfoRow label="Aging" value={`${order.aging_days}d (${order.aging_bucket})`} />
              </div>
            </div>
          ))}
          {orderMatches.length > 5 && (
            <p className="text-xs text-muted-foreground">
              Showing 5 of {orderMatches.length}. Refine search for more results.
            </p>
          )}
        </div>
      )}

      {hasSearch && uniqueVendors.length > 0 && (
        <div className="mt-4 space-y-2">
          <p className="text-sm font-semibold text-[#a78bfa]">
            Found {uniqueVendors.length} vendor(s)
          </p>
          {uniqueVendors.map(vendor => {
            const cnt = vendorMatches.filter(r => r.vendor === vendor).length
            return (
              <button
                key={vendor}
                onClick={() => nav.goTo('search_vendor_orders', { searchVendor: vendor })}
                className="flex w-full items-center justify-between rounded-lg border border-border bg-secondary/50 px-4 py-3 text-left transition-colors hover:bg-accent"
              >
                <div>
                  <p className="text-sm font-semibold text-foreground">{vendor}</p>
                  <p className="text-xs text-muted-foreground">{cnt} orders in backlog</p>
                </div>
                <span className="text-xs text-muted-foreground">View</span>
              </button>
            )
          })}
        </div>
      )}

      {hasSearch && orderMatches.length === 0 && uniqueVendors.length === 0 && (
        <p className="mt-3 text-sm text-muted-foreground">
          {'No results found for "'}{query}{'"'}
        </p>
      )}
    </div>
  )
}

function InfoRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-baseline gap-2">
      <span className="text-xs font-medium text-muted-foreground">{label}:</span>
      <span className="text-sm text-foreground">{value}</span>
    </div>
  )
}
