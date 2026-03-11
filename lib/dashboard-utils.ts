import type { OrderRow } from './types'
import { BUCKET_ORDER } from './types'

export function groupByBucket(orders?: OrderRow[] | null): Record<string, number> {
  const counts: Record<string, number> = {}
  for (const b of BUCKET_ORDER) counts[b] = 0
  if (!orders || !Array.isArray(orders)) return counts
  for (const order of orders) {
    if (order.aging_bucket && counts[order.aging_bucket] !== undefined) {
      counts[order.aging_bucket]++
    }
  }
  return counts
}

export function groupByVendor(orders?: OrderRow[] | null): { vendor: string; count: number }[] {
  if (!orders || !Array.isArray(orders)) return []
  const map = new Map<string, number>()
  for (const order of orders) {
    const v = order.vendor || 'Unknown'
    map.set(v, (map.get(v) || 0) + 1)
  }
  return Array.from(map.entries())
    .map(([vendor, count]) => ({ vendor, count }))
    .sort((a, b) => b.count - a.count)
}

export function formatNumber(n: number): string {
  return n.toLocaleString('en-US')
}
