export interface OrderRow {
  order_number: string
  fleek_id: string
  customer_name: string
  customer_country: string
  vendor: string
  item_name: string
  total_order_line_amount: string
  product_brand: string
  logistics_partner_name: string
  latest_status: string
  qc_approved_at: string
  logistics_partner_handedover_at: string
  is_zone_vendor: string
  vendor_country: string
  aging_days: number
  aging_bucket: string
  qc_or_zone: string
  order_type: string
}

export interface DashboardData {
  approved: OrderRow[]
  handover: OrderRow[]
  pk_zone: OrderRow[]
  qc_center: OrderRow[]
  pk_normal: OrderRow[]
  pk_ai: OrderRow[]
  qc_normal: OrderRow[]
  qc_ai: OrderRow[]
  all_data: OrderRow[]
  updated_at: string
}

export const BUCKET_ORDER = [
  '0 days', '1 day', '2 days', '3 days', '4 days', '5 days',
  '6-7 days', '8-10 days', '11-15 days', '16-20 days',
  '21-25 days', '26-30 days', '30+ days',
]

export const DISPLAY_COLS: (keyof OrderRow)[] = [
  'order_number', 'fleek_id', 'customer_name', 'customer_country',
  'vendor', 'item_name', 'total_order_line_amount', 'product_brand',
  'logistics_partner_name', 'aging_days', 'aging_bucket',
]

export const VENDOR_ACTION_OPTIONS = [
  '--', 'today', 'update', 'Tuesday', 'Thursday', 'Saturday', 'NOT Response', 'MOVE to WH',
]

export type PageView =
  | 'home'
  | 'handover'
  | 'pk_normal'
  | 'pk_ai'
  | 'qc_normal'
  | 'qc_ai'
  | 'aging_detail'
  | 'vendor_detail'
  | 'handover_aging_detail'
  | 'search_vendor_orders'
