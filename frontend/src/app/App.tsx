import { Outlet } from "react-router-dom";
import { SidebarProvider, SidebarTrigger } from "@/shared/ui/sidebar"
import { AppSidebar } from "@/features/sidebar"
import { Toaster } from "sonner";

export function App() {
  return (
    <div className="min-h-screen flex flex-col">
        <SidebarProvider>
          <AppSidebar />
          <div className="flex min-h-screen flex-1 flex-col">
            <header className="flex h-12 items-center border-b px-3">
              <SidebarTrigger />
              <div className="ml-2 font-medium">Панель управления</div>
            </header>
            <Outlet />
            <Toaster richColors closeButton position="top-right" />
            <main className="flex-1 p-4"></main>
          </div>
        </SidebarProvider>
    </div>
  );
}
