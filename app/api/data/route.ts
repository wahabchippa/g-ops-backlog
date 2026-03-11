import { NextResponse } from 'next/server'
import type { OrderRow } from '@/lib/types'

export const dynamic = 'force-dynamic'
export const runtime = 'nodejs'

const SHEET_ID = '1GKIgyPTsxNctFL_oUJ9jqqvIjFBTsFi2mOj5VpHCv3o'

async function fetchSheet(sheetName: string): Promise<string> {
  const url = `https://docs.google.com/spreadsheets/d/${SHEET_ID}/gviz/tq?tqx=out:csv&sheet=${encodeURIComponent(sheetName)}`
  const res = await fetch(url, { cache: 'no-store' })
  if (!res.ok) throw new Error(`Sheet fetch failed: ${res.status}`)
  return res.text()
}

function csvToJson(csv: string): Record<string, string>[] {
  const lines = csv.split('\n')
  if (lines.length < 2) return []
  
  const headers = parseCSVLine(lines[0])
  const rows: Record<string, string>[] = []
  
  for (let i = 1; i < lines.length; i++) {
    const line = lines[i].trim()
    if (!line) continue
    const values = parseCSVLine(line)
    const row: Record<string, string> = {}
    headers.forEach((h, idx) => {
      row[h.trim().replace(/^"|"$/g, '')] = (values[idx] || '').replace(/^"|"$/g, '')
    })
    rows.push(row)
  }
  return rows
}

function parseCSVLine(line: string): string[] {
  const result: string[] = []
  let current = ''
  let inQuotes = false
  
  for (let i = 0; i < line.length; i++) {
    const char = line[i]
    if (char === '"') {
      if (inQuotes && line[i + 1] === '"') {
        current += '"'
        i++
      } else {
        inQuotes = !inQuotes
      }
    } else if (char === ',' && !inQuotes) {
      result.push(current)
      current = ''
    } else {
      current += char
    }
  }
  result.push(current)
  return result
}

function parseDate(dateStr: string): Date | null {
  if (!dateStr || dateStr.trim() === '') return null
  const s = dateStr.trim()
  
  const formats = [
    /^(\d{2})\/(\d{2})\/(\d{4}) (\d{2}):(\d{2}):(\d{2})$/,
    /^(\d{2})\/(\d{2})\/(\d{4})$/,
    /^(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})$/,
  ]
  
  const m1 = s.match(formats[0])
  if (m1) return new Date(+m1[3], +m1[2] - 1, +m1[1], +m1[4], +m1[5], +m1[6])
  
  const m2 = s.match(formats[1])
  if (m2) return new Date(+m2[3], +m2[2] - 1, +m2[1])
  
  const m3 = s.match(formats[2])
  if (m3) return new Date(+m3[1], +m3[2] - 1, +m3[3], +m3[4], +m3[5], +m3[6])
  
  const d = new Date(s)
  return isNaN(d.getTime()) ? null : d
}

function getAgingBucket(days: number): string {
  if (days === 0) return '0 days'
  if (days === 1) return '1 day'
  if (days === 2) return '2 days'
  if (days === 3) return '3 days'
  if (days === 4) return '4 days'
  if (days === 5) return '5 days'
  if (days >= 6 && days <= 7) return '6-7 days'
  if (days >= 8 && days <= 10) return '8-10 days'
  if (days >= 11 && days <= 15) return '11-15 days'
  if (days >= 16 && days <= 20) return '16-20 days'
  if (days >= 21 && days <= 25) return '21-25 days'
  if (days >= 26 && days <= 30) return '26-30 days'
  return '30+ days'
}

function getQcZone(isZone: string, vendorCountry: string): string {
  const iz = (isZone || '').trim().toUpperCase()
  const vc = (vendorCountry || '').trim().toUpperCase()
  
  if (vc === 'PK') return iz === 'TRUE' ? 'PK Zone' : 'PK QC Center'
  if (vc === 'IN') return iz === 'TRUE' ? 'IN Zone' : 'IN QC Center'
  return 'Other'
}

export async function GET() {
  try {
    const [mainCsv, aiCsv] = await Promise.all([
      fetchSheet('Extract 1'),
      fetchSheet('AI'),
    ])
    
    const mainRows = csvToJson(mainCsv)
    const aiRows = csvToJson(aiCsv)
    const aiFleekIds = new Set(aiRows.map(r => (r.fleek_id || '').trim()))

    const now = new Date()

    const processRow = (row: Record<string, string>, status: string, dateField: string): OrderRow => {
      const qcZone = getQcZone(row.is_zone_vendor || '', row.vendor_country || '')
      const orderType = aiFleekIds.has((row.fleek_id || '').trim()) ? 'AI Order' : 'Normal Order'
      
      const dateStr = row[dateField] || ''
      const parsed = parseDate(dateStr)
      const agingDays = parsed ? Math.floor((now.getTime() - parsed.getTime()) / (1000 * 60 * 60 * 24)) : 0

      return {
        order_number: row.order_number || '',
        fleek_id: row.fleek_id || '',
        customer_name: row.customer_name || '',
        customer_country: row.customer_country || '',
        vendor: row.vendor || '',
        item_name: row.item_name || '',
        total_order_line_amount: row.total_order_line_amount || '',
        product_brand: row.product_brand || '',
        logistics_partner_name: row.logistics_partner_name || '',
        latest_status: status,
        qc_approved_at: row.qc_approved_at || '',
        logistics_partner_handedover_at: row.logistics_partner_handedover_at || '',
        is_zone_vendor: row.is_zone_vendor || '',
        vendor_country: row.vendor_country || '',
        aging_days: agingDays,
        aging_bucket: getAgingBucket(agingDays),
        qc_or_zone: qcZone,
        order_type: orderType,
      }
    }

    const approved: OrderRow[] = []
    const handover: OrderRow[] = []

    for (const row of mainRows) {
      const status = (row.latest_status || '').trim()
      if (status === 'QC_APPROVED') {
        approved.push(processRow(row, status, 'qc_approved_at'))
      } else if (status === 'HANDED_OVER_TO_LOGISTICS_PARTNER') {
        const qcZone = getQcZone(row.is_zone_vendor || '', row.vendor_country || '')
        if (qcZone === 'PK Zone' || qcZone === 'PK QC Center') {
          handover.push(processRow(row, status, 'logistics_partner_handedover_at'))
        }
      }
    }

    const pk_zone = approved.filter(r => r.qc_or_zone === 'PK Zone')
    const qc_center = approved.filter(r => r.qc_or_zone === 'PK QC Center')
    const pk_normal = pk_zone.filter(r => r.order_type === 'Normal Order')
    const pk_ai = pk_zone.filter(r => r.order_type === 'AI Order')
    const qc_normal = qc_center.filter(r => r.order_type === 'Normal Order')
    const qc_ai = qc_center.filter(r => r.order_type === 'AI Order')

    return NextResponse.json({
      approved,
      handover,
      pk_zone,
      qc_center,
      pk_normal,
      pk_ai,
      qc_normal,
      qc_ai,
      all_data: [...approved, ...handover],
      updated_at: now.toISOString(),
    }, {
      headers: {
        'Cache-Control': 'no-store, no-cache, must-revalidate',
      },
    })
  } catch (err) {
    return NextResponse.json({ error: String(err) }, { status: 500 })
  }
}
