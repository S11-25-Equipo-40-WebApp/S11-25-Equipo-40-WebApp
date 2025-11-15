'use client'

import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/Sidebar"

export default function UsuariosPage() {
  return (
    <SidebarProvider>
      <div className="flex min-h-screen w-full bg-[#0f172a] text-white">
        <AppSidebar />

        <SidebarInset className="bg-[#0f172a]">
          <div className="p-8">
            <h1 className="text-3xl font-bold mb-6">Gestión de Usuarios</h1>
          </div>
        </SidebarInset>
      </div>
    </SidebarProvider>
  )
}
