'use client'

import { useDashboardData } from '@/hooks/use-dashboard-data'
import { useNavigation } from '@/components/navigation-provider'
import { DashboardSidebar } from '@/components/dashboard-sidebar'
import { HomeView } from '@/components/home-view'
import { DetailView } from '@/components/detail-view'
import { Loader2, Menu, RefreshCw, AlertTriangle } from 'lucide-react'

export function DashboardShell() {
  const { data, error, isLoading, mutate } = useDashboardData()
  const nav = useNavigation()

  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center bg-background">
        <div className="flex flex-col items-center gap-4">
          <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
          <p className="text-sm text-muted-foreground">Loading dashboard data...</p>
        </div>
      </div>
    )
  }

  if (error || !data) {
    return (
      <div className="flex h-screen items-center justify-center bg-background">
        <div className="flex flex-col items-center gap-4 text-center">
          <AlertTriangle className="h-8 w-8 text-destructive" />
          <p className="text-sm text-muted-foreground">Failed to load data. Please try again.</p>
          <button
            onClick={() => mutate()}
            className="flex items-center gap-2 rounded-lg bg-secondary px-4 py-2 text-sm font-medium text-foreground transition-colors hover:bg-accent"
          >
            <RefreshCw className="h-4 w-4" />
            Retry
          </button>
        </div>
      </div>
    )
  }

  const getDetailViewProps = () => {
    switch (nav.page) {
      case 'handover':
        return { title: 'Handover Orders', orders: data.handover }
      case 'pk_normal':
        return { title: 'PK Zone \u2014 Normal Orders', orders: data.pk_normal }
      case 'pk_ai':
        return { title: 'PK Zone \u2014 AI Orders', orders: data.pk_ai }
      case 'qc_normal':
        return { title: 'QC Center \u2014 Normal Orders', orders: data.qc_normal }
      case 'qc_ai':
        return { title: 'QC Center \u2014 AI Orders', orders: data.qc_ai }
      case 'aging_detail': {
        const zone = nav.agingZone || 'PK Zone'
        const bucket = nav.agingBucket || '0 days'
        const source = zone === 'PK Zone' ? data.pk_normal : data.qc_normal
        return {
          title: `${zone} \u2014 ${bucket}`,
          orders: source.filter(r => r.aging_bucket === bucket),
        }
      }
      case 'vendor_detail': {
        const vendor = nav.vendorName || ''
        const zone = nav.vendorZone || 'PK Zone'
        const source = zone === 'PK Zone' ? data.pk_normal : data.qc_normal
        return {
          title: vendor,
          orders: source.filter(r => r.vendor === vendor),
        }
      }
      case 'handover_aging_detail': {
        const bucket = nav.handoverBucket || '0 days'
        return {
          title: `Handover \u2014 ${bucket}`,
          orders: data.handover.filter(r => r.aging_bucket === bucket),
        }
      }
      case 'search_vendor_orders': {
        const vendor = nav.searchVendor || ''
        return {
          title: vendor,
          orders: data.all_data.filter(r => r.vendor === vendor),
        }
      }
      default:
        return null
    }
  }

  const detailProps = nav.page !== 'home' ? getDetailViewProps() : null

  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar - desktop */}
      <div className={`hidden lg:block ${nav.sidebarOpen ? '' : 'lg:hidden'}`}>
        {data && <DashboardSidebar />}
      </div>

      {/* Sidebar - mobile overlay */}
      {nav.sidebarOpen && (
        <div className="fixed inset-0 z-50 lg:hidden">
          <div
            className="absolute inset-0 bg-background/80 backdrop-blur-sm"
            onClick={() => nav.setSidebarOpen(false)}
          />
          <div className="relative z-10 h-full w-64">
            {data && <DashboardSidebar />}
          </div>
        </div>
      )}

      {/* Main content */}
      <main className="flex-1 overflow-y-auto">
        {/* Mobile header */}
        <div className="sticky top-0 z-40 flex items-center border-b border-border bg-background/95 px-4 py-3 backdrop-blur lg:hidden">
          <button
            onClick={() => nav.setSidebarOpen(true)}
            className="rounded-md p-2 text-muted-foreground transition-colors hover:bg-accent hover:text-foreground"
          >
            <Menu className="h-5 w-5" />
          </button>
          <span className="ml-3 text-sm font-semibold text-foreground">G-Ops Dashboard</span>
        </div>

        {/* Toggle sidebar on desktop when closed */}
        {!nav.sidebarOpen && (
          <div className="hidden lg:block">
            <button
              onClick={() => nav.setSidebarOpen(true)}
              className="fixed left-4 top-4 z-40 rounded-md border border-border bg-card p-2 text-muted-foreground shadow-sm transition-colors hover:bg-accent hover:text-foreground"
            >
              <Menu className="h-5 w-5" />
            </button>
          </div>
        )}

        <div className="mx-auto max-w-7xl px-4 py-6 lg:px-8 lg:py-8">
          {nav.page === 'home' ? (
            <HomeView data={data} />
          ) : detailProps ? (
            <DetailView {...detailProps} />
          ) : null}
        </div>
      </main>
    </div>
  )
}
