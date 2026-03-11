import useSWR from 'swr'
import type { DashboardData } from '@/lib/types'

const fetcher = (url: string) => fetch(url).then(res => res.json())

export function useDashboardData() {
  const { data, error, isLoading, mutate } = useSWR<DashboardData>(
    '/api/data',
    fetcher,
    {
      revalidateOnFocus: false,
      dedupingInterval: 600000,
    }
  )

  return { data, error, isLoading, mutate }
}
