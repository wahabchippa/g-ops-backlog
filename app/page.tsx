import { NavigationProvider } from '@/components/navigation-provider'
import { DashboardShell } from '@/components/dashboard-shell'

export default function Page() {
  return (
    <NavigationProvider>
      <DashboardShell />
    </NavigationProvider>
  )
}
