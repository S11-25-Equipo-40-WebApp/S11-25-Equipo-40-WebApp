'use client'

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"

import { Home, Users, MessageSquare, Settings, LogOut } from "lucide-react"

export function AppSidebar() {
  return (
    <Sidebar className="bg-[#0B1120] text-gray-300 border-none w-64">
      <SidebarContent>
        <div className="p-6 flex items-center gap-2">
          <div className="w-8 h-8 bg-blue-500 rounded-md flex items-center justify-center font-bold text-white">
            T
          </div>
          <h1 className="text-xl font-semibold text-white">Testimonials</h1>
        </div>

        <SidebarGroup>
          <SidebarGroupLabel className="text-xs text-gray-500 uppercase mb-2 px-6">
            Menú
          </SidebarGroupLabel>

          <SidebarMenu>
            <SidebarMenuItem>
              <SidebarMenuButton asChild>
                <a href="/dashboard" className="flex items-center gap-3 px-6 py-2 hover:bg-[#1E293B] rounded-lg transition">
                  <Home className="w-5 h-5 text-blue-400" />
                  Dashboard
                </a>
              </SidebarMenuButton>
            </SidebarMenuItem>

            <SidebarMenuItem>
              <SidebarMenuButton asChild>
                <a href="/users" className="flex items-center gap-3 px-6 py-2 hover:bg-[#1E293B] rounded-lg transition">
                  <Users className="w-5 h-5 text-blue-400" />
                  Usuarios
                </a>
              </SidebarMenuButton>
            </SidebarMenuItem>

            <SidebarMenuItem>
              <SidebarMenuButton asChild>
                <a href="/testimonials" className="flex items-center gap-3 px-6 py-2 hover:bg-[#1E293B] rounded-lg transition">
                  <MessageSquare className="w-5 h-5 text-blue-400" />
                  Testimonios
                </a>
              </SidebarMenuButton>
            </SidebarMenuItem>

            <SidebarMenuItem>
              <SidebarMenuButton asChild>
                <a href="/configuracion" className="flex items-center gap-3 px-6 py-2 hover:bg-[#1E293B] rounded-lg transition">
                  <Settings className="w-5 h-5 text-blue-400" />
                  Configuración
                </a>
              </SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroup>
      </SidebarContent>

      <SidebarFooter className="px-6 py-4 border-t border-gray-800">
        <button className="flex items-center gap-3 text-sm text-gray-400 hover:text-white transition">
          <LogOut className="w-4 h-4 text-red-500" />
          Cerrar sesión
        </button>
      </SidebarFooter>
    </Sidebar>
  )
}
