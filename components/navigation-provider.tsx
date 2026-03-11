'use client'

import { createContext, useContext, useState, useCallback, type ReactNode } from 'react'
import type { PageView } from '@/lib/types'

interface NavigationState {
  page: PageView
  agingZone: string | null
  agingBucket: string | null
  vendorName: string | null
  vendorZone: string | null
  handoverBucket: string | null
  searchVendor: string | null
  sidebarOpen: boolean
}

interface NavigationContextType extends NavigationState {
  goHome: () => void
  goTo: (page: PageView, params?: Partial<NavigationState>) => void
  toggleSidebar: () => void
  setSidebarOpen: (open: boolean) => void
}

const NavigationContext = createContext<NavigationContextType | null>(null)

export function NavigationProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<NavigationState>({
    page: 'home',
    agingZone: null,
    agingBucket: null,
    vendorName: null,
    vendorZone: null,
    handoverBucket: null,
    searchVendor: null,
    sidebarOpen: true,
  })

  const goHome = useCallback(() => {
    setState(prev => ({ ...prev, page: 'home' }))
  }, [])

  const goTo = useCallback((page: PageView, params?: Partial<NavigationState>) => {
    setState(prev => ({ ...prev, ...params, page }))
  }, [])

  const toggleSidebar = useCallback(() => {
    setState(prev => ({ ...prev, sidebarOpen: !prev.sidebarOpen }))
  }, [])

  const setSidebarOpen = useCallback((open: boolean) => {
    setState(prev => ({ ...prev, sidebarOpen: open }))
  }, [])

  return (
    <NavigationContext.Provider value={{ ...state, goHome, goTo, toggleSidebar, setSidebarOpen }}>
      {children}
    </NavigationContext.Provider>
  )
}

export function useNavigation() {
  const ctx = useContext(NavigationContext)
  if (!ctx) throw new Error('useNavigation must be used within NavigationProvider')
  return ctx
}
