import { ReactNode } from "react"
import { NuqsAdapter } from "nuqs/adapters/react-router"
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

import { SidebarProvider } from "@/shared/sidebar"

const queryClient = new QueryClient()

export function Providers({ children }: { children: ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      <NuqsAdapter>
          {children}
      </NuqsAdapter>
    </QueryClientProvider>
  )
}