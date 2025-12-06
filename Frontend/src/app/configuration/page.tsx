'use client'

import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/Sidebar"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useEffect, useState } from "react"

export default function ConfiguracionPage() {


  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  

  useEffect(() => {
  const loadConfig = async () => {
    try {
      setLoading(true)

      await new Promise(resolve => setTimeout(resolve, 600))

    } catch (err) {
      setError("Error cargando API Keys")
    } finally {
      setLoading(false) 
    }
  }

  loadConfig()
}, [])



 if (loading) return <div className="flex min-h-screen w-full bg-[#0f172a] text-white text-center items-center justify-center">Cargando...</div>



  return (
    <SidebarProvider>
      <div className="flex w-full min-h-screen bg-[#0f172a] text-white">
        <AppSidebar />

        <SidebarInset className="bg-[#0f172a]">
          <div className="p-8 max-w-4xl">

        
            <div className="mb-6">
              <h1 className="text-3xl font-bold">Configuración</h1>
              <p className="text-sm text-gray-400 mt-1">
                Administra tu cuenta y preferencias del sistema
              </p>
            </div>

            <Tabs defaultValue="perfil" className="w-full">
              <TabsList className="bg-gray-900 border border-gray-700 mb-6">
                <TabsTrigger value="perfil">Perfil</TabsTrigger>
                <TabsTrigger value="seguridad">Seguridad</TabsTrigger>
                <TabsTrigger value="roles">Roles</TabsTrigger>
              </TabsList>

           
              <TabsContent value="perfil">
                <div className="bg-gray-900 border border-gray-700 rounded-lg p-6 space-y-4">
                  <h2 className="text-xl font-semibold">Perfil de la Cuenta</h2>

                  <div>
                    <Label className="text-gray-300 p-1">Nombre del Proyecto</Label>
                    <Input
                      placeholder="Testify"
                      className="bg-[#0f172a] border-gray-700 text-white"
                    />
                  </div>

                  <div>
                    <Label className="text-gray-300 p-1">Email de contacto</Label>
                    <Input
                      type="email"
                      placeholder="contacto@testify.com"
                      className="bg-[#0f172a] border-gray-700 text-white"
                    />
                  </div>

                  <Button className="bg-blue-600 hover:bg-blue-700">
                    Guardar cambios
                  </Button>
                </div>
              </TabsContent>

             
              <TabsContent value="seguridad">
                <div className="bg-gray-900 border border-gray-700 rounded-lg p-6 space-y-4">
                  <h2 className="text-xl font-semibold">Seguridad</h2>

                  <div>
                    <Label className="text-gray-300">Contraseña actual</Label>
                    <Input
                      type="password"
                      className="bg-[#0f172a] border-gray-700 text-white"
                    />
                  </div>

                  <div>
                    <Label className="text-gray-300">Nueva contraseña</Label>
                    <Input
                      type="password"
                      className="bg-[#0f172a] border-gray-700 text-white"
                    />
                  </div>

                  <div>
                    <Label className="text-gray-300">Confirmar contraseña</Label>
                    <Input
                      type="password"
                      className="bg-[#0f172a] border-gray-700 text-white"
                    />
                  </div>

                  <Button className="bg-blue-600 hover:bg-blue-700">
                    Actualizar contraseña
                  </Button>
                </div>
              </TabsContent>

              <TabsContent value="roles">
                <div className="bg-gray-900 border border-gray-700 rounded-lg p-6 space-y-4">
                  <h2 className="text-xl font-semibold">Roles & Permisos</h2>

                  <p className="text-sm text-gray-400">
                    Define qué puede hacer cada tipo de usuario
                  </p>

                  <div className="grid grid-cols-2 gap-4">
                    <div className="border border-gray-700 rounded-lg p-4">
                      <h3 className="font-semibold mb-2">Administrador</h3>
                      <ul className="text-sm text-gray-400 space-y-1">
                        <li>✔ Gestionar usuarios</li>
                        <li>✔ Crear API Keys</li>
                        <li>✔ Ver testimonios</li>
                      </ul>
                    </div>

                    <div className="border border-gray-700 rounded-lg p-4">
                      <h3 className="font-semibold mb-2">Usuario</h3>
                      <ul className="text-sm text-gray-400 space-y-1">
                        <li>✔ Ver testimonios</li>
                        <li>✖ Gestionar API Keys</li>
                        <li>✖ Administrar usuarios</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </TabsContent>

            </Tabs>
          </div>
        </SidebarInset>
      </div>
    </SidebarProvider>
  )
}
