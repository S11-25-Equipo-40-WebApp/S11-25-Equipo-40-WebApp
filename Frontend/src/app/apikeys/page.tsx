'use client'

import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/Sidebar"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { useEffect, useState, useCallback } from "react"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog"
import { Search, Trash2, Pencil, Copy, Eye, EyeOff } from "lucide-react"
import { useAuth } from "@/hooks/useAuth"

type ApiKey = {
  id: string
  name: string
  prefix: string
  revoked: boolean
  created_at: string
  raw_key?: string
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "https://testify-dwtn.onrender.com/api"

export default function ApiKeysPage() {
  const { getAuthHeaders } = useAuth()
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const [apiKeys, setApiKeys] = useState<ApiKey[]>([])
  const [searchTerm, setSearchTerm] = useState("")
  const [openCreate, setOpenCreate] = useState(false)
  const [openEdit, setOpenEdit] = useState(false)
  const [currentKey, setCurrentKey] = useState<ApiKey | null>(null)
  const [keyName, setKeyName] = useState("")

  const loadApiKeys = useCallback(async () => {
  try {
    setLoading(true)
    
    const res = await fetch(`${API_BASE}/api-keys`, {
      headers: getAuthHeaders()
    })

    const respText = await res.text()

    if (!res.ok) {
      throw new Error(`Error ${res.status}: ${respText}`)
    }

    const data: ApiKey[] = JSON.parse(respText)
    setApiKeys(data)
    setError(null)

  } catch (err) {
    console.error(err)
    setError("Error cargando API Keys: " + (err instanceof Error ? err.message : "Desconocido"))
  } finally {
    setLoading(false)
  }
}, [getAuthHeaders])


  useEffect(() => {
    loadApiKeys()
  }, [loadApiKeys])





  const handleCreate = async () => {
  if (!keyName.trim()) {
    setError("El nombre es requerido")
    return
  }

  try {
    setError(null)
    const res = await fetch(`${API_BASE}/api-keys`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify({ name: keyName })
    })

    const respText = await res.text()
    if (!res.ok) {
      throw new Error(`Error ${res.status}: ${respText}`)
    }

    const newKey = JSON.parse(respText)
    setApiKeys([newKey, ...apiKeys])
    setKeyName("")
    setOpenCreate(false)

  } catch (err) {
    setError("Error: " + (err instanceof Error ? err.message : "Desconocido"))
  }
}


  const handleEdit = async () => {
    if (!currentKey) return

    setApiKeys(apiKeys.map(k =>
      k.id === currentKey.id ? { ...k, name: keyName } : k
    ))

    setCurrentKey(null)
    setKeyName("")
    setOpenEdit(false)
  }





  const revokeKey = async (id: string) => {
  try {
    const res = await fetch(`${API_BASE}/api-keys/revoke/${id}`, {
      method: "POST"
    })

    if (!res.ok) throw new Error("Error revocando API Key")

    setApiKeys(apiKeys.map(k =>
      k.id === id ? { ...k, revoked: true } : k
    ))

  } catch (err) {
    alert("No se pudo revocar la key")
  }
}


  const copyKey = (key: string) => {
    navigator.clipboard.writeText(key)
  }

  const filteredKeys = apiKeys.filter(k =>
    k.name.toLowerCase().includes(searchTerm.toLowerCase())
  )

  if (loading) {
    return (
      <div className="flex min-h-screen w-full bg-[#0f172a] text-white text-center items-center justify-center">
        Cargando...
      </div>
    )
  }

  return (
    <SidebarProvider>
      <div className="flex w-full min-h-screen bg-[#0f172a] text-white">
        <AppSidebar />

        <SidebarInset className="bg-[#0f172a]">
          <div className="p-8">

         
            <div className="flex justify-between items-center mb-6">
              <div>
                <h1 className="text-3xl font-bold">API Keys</h1>
                <p className="text-sm text-gray-400 mt-1">
                  Administra claves para consumir la API
                </p>
              </div>

              <Button
                onClick={() => setOpenCreate(true)}
                className="bg-blue-600 hover:bg-blue-700"
              >
                + Create API Key
              </Button>
            </div>

            
            <div className="flex mb-6 max-w-md relative">
              <Search className="absolute left-3 top-3 w-4 h-4 text-gray-400" />
              <Input
                placeholder="Buscar API Key..."
                className="pl-10 bg-gray-900 border-gray-700 text-white"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>

         
            <div className="border border-gray-700 rounded-lg overflow-hidden">
              <div className="bg-gray-900 border-b border-gray-700 px-6 py-4 grid grid-cols-12 gap-4">
                <div className="col-span-3 font-semibold">Nombre</div>
                <div className="col-span-4 font-semibold">Prefijo</div>
                <div className="col-span-2 font-semibold">Creada</div>
                <div className="col-span-2 font-semibold">Estado</div>
                <div className="col-span-1 text-right font-semibold">Acciones</div>
              </div>

              {filteredKeys.map(k => (
                <div
                  key={k.id}
                  className="grid grid-cols-12 gap-4 px-6 py-4 border-b border-gray-700 hover:bg-gray-900/50 items-center"
                >
                  <div className="col-span-3">{k.name}</div>
                  <div className="col-span-4 text-gray-400">{k.prefix}</div>
                  <div className="col-span-2">
                    {new Date(k.created_at).toLocaleDateString()}
                  </div>
                  <div className="col-span-2">
                    <span className={`px-3 py-1 rounded text-sm ${k.revoked ? "bg-red-600" : "bg-green-600"}`}>
                      {k.revoked ? "Revocado" : "Activo"}
                    </span>
                  </div>

                  <div className="col-span-1 flex gap-3 justify-end">
                    <Copy
                      className="cursor-pointer hover:text-blue-400"
                      onClick={() => copyKey(k.prefix)}
                    />
                    <Pencil
                      className="cursor-pointer hover:text-blue-400"
                      onClick={() => {
                        setCurrentKey(k)
                        setKeyName(k.name)
                        setOpenEdit(true)
                      }}
                    />
                    {!k.revoked && (
                      <Trash2
                        className="cursor-pointer hover:text-red-400"
                        onClick={() => revokeKey(k.id)}
                      />
                    )}
                  </div>
                </div>
              ))}

              {filteredKeys.length === 0 && (
                <div className="p-6 text-center text-gray-400">
                  No hay API Keys creadas
                </div>
              )}
            </div>
          </div>
        </SidebarInset>
      </div>

      <Dialog open={openCreate} onOpenChange={setOpenCreate}>
        <DialogContent className="bg-[#020617] border border-gray-800 text-white">
          <DialogHeader>
            <DialogTitle>Crear API Key</DialogTitle>
          </DialogHeader>

          <Input
            placeholder="Nombre de la API Key"
            value={keyName}
            onChange={(e) => setKeyName(e.target.value)}
            className="bg-gray-900 border-gray-700"
          />

          <DialogFooter>
            <Button variant="ghost" onClick={() => setOpenCreate(false)}>
              Cancelar
            </Button>
            <Button
              className="bg-blue-600"
              disabled={!keyName}
              onClick={handleCreate}
            >
              Crear
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>


     <Dialog open={openEdit} onOpenChange={setOpenEdit}>
        <DialogContent className="bg-[#020617] border border-gray-800 text-white">
          <DialogHeader>
            <DialogTitle>Editar API Key</DialogTitle>
          </DialogHeader>

          <Input
            placeholder="Nuevo nombre"
            value={keyName}
            onChange={(e) => setKeyName(e.target.value)}
            className="bg-gray-900 border-gray-700"
          />

          <DialogFooter>
            <Button variant="ghost" onClick={() => setOpenEdit(false)}>
              Cancelar
            </Button>
            <Button
              className="bg-blue-600"
              disabled={!keyName}
              onClick={handleEdit}
            >
              Guardar
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </SidebarProvider>
  )
}
