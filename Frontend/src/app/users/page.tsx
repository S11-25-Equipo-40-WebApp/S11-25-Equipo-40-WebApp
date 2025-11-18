'use client'

import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/Sidebar"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Search, Trash2, Pencil } from "lucide-react"
import { useEffect, useState } from "react"
import Image from "next/image"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:3001/api"

export default function UsuariosPage() {

  const [users, setUsers] = useState([])
  const [filteredUsers, setFilteredUsers] = useState([])
  const [searchTerm, setSearchTerm] = useState("")
  const [selectedRole, setSelectedRole] = useState("all")
  const [selectedStatus, setSelectedStatus] = useState("all")
  const [selectedIds, setSelectedIds] = useState(new Set())
  const [currentPage, setCurrentPage] = useState(1)
  const itemsPerPage = 4

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)


  useEffect(() => {
    fetchUsers()
  }, [])

  const fetchUsers = async () => {
    try {
      setLoading(true)
      const res = await fetch(`${API_URL}/users`)
      if (!res.ok) throw new Error("Error obteniendo usuarios")
      const data = await res.json()

      setUsers(data)
      setFilteredUsers(data)
    } catch (err) {
      //@ts-ignore
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }



  useEffect(() => {
    let filtered = users
    
    if (searchTerm) {
      filtered = filtered.filter(u =>
         //@ts-ignore
        u.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
         //@ts-ignore
        u.email.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    if (selectedRole !== "all") {
      filtered = filtered.filter(u => u.role === selectedRole)
    }

    if (selectedStatus !== "all") {
      filtered = filtered.filter(u => u.status === selectedStatus)
    }

    setFilteredUsers(filtered)
    setCurrentPage(1)
  }, [searchTerm, selectedRole, selectedStatus, users])



  const paginated = filteredUsers.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  )
  //@ts-ignore
  const handleSelectAll = (e) => {
    if (e.target.checked) {
      const ids = new Set(paginated.map(u => u.id))
      setSelectedIds(ids)
    } else {
      setSelectedIds(new Set())
    }
  }

   //@ts-ignore
  const handleSelectItem = (id) => {
    const updated = new Set(selectedIds)
    updated.has(id) ? updated.delete(id) : updated.add(id)
    setSelectedIds(updated)
  }

  const totalPages = Math.ceil(filteredUsers.length / itemsPerPage)

   if (loading) return <div className="flex min-h-screen w-full bg-[#0f172a] text-white text-center items-center justify-center">Cargando...</div>


  return (
    <SidebarProvider>
      <div className="flex w-full min-h-screen bg-[#0f172a] text-white">
        <AppSidebar />

        <SidebarInset className="bg-[#0f172a]">
          <div className="p-8">

            <div className="flex justify-between items-center mb-6">
              <h1 className="text-3xl font-bold">Gestión de Usuarios</h1>
              <Button className="bg-blue-600 hover:bg-blue-700">+ Añadir Nuevo Usuario</Button>
            </div>

        
            <div className="flex gap-4 mb-6">
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-3 w-4 h-4 text-gray-400" />
                <Input
                  placeholder="Buscar por nombre o email..."
                  className="pl-10 bg-gray-900 border-gray-700 text-white"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>

              <select
                className="bg-gray-900 border border-gray-700 rounded px-3 py-2 text-sm"
                value={selectedRole}
                onChange={(e) => setSelectedRole(e.target.value)}>

                <option value="all">Rol: Todos</option>
                <option value="Administrador">Administrador</option>
                <option value="Usuario">Usuario</option>
              </select>

            
              <select
                className="bg-gray-900 border border-gray-700 rounded px-3 py-2 text-sm"
                value={selectedStatus}
                onChange={(e) => setSelectedStatus(e.target.value)}
              >
                <option value="all">Estado: Todos</option>
                <option value="Activo">Activo</option>
                <option value="Inactivo">Inactivo</option>
              </select>
            </div>


        
            <div className="border border-gray-700 rounded-lg overflow-hidden">

    
              <div className="bg-gray-900 border-b border-gray-700 px-6 py-4 grid grid-cols-12 gap-4">
                <div><input type="checkbox" onChange={handleSelectAll} /></div>
                <div className="col-span-3 font-semibold">Nombre de Usuario</div>
                <div className="col-span-2 font-semibold">Rol</div>
                <div className="col-span-3 font-semibold">Fecha Registro</div>
                <div className="col-span-2 font-semibold">Estado</div>
                <div className="col-span-1 font-semibold">Acciones</div>
              </div>

          
              {paginated.map((u) => (
                <div
                  key={u.id}
                  className="grid grid-cols-12 gap-4 px-6 py-4 border-b border-gray-700 hover:bg-gray-900/50 items-center"
                >
                  <div>
                    <input
                      type="checkbox"
                      checked={selectedIds.has(u.id)}
                      onChange={() => handleSelectItem(u.id)}
                    />
                  </div>

                  
                  <div className="col-span-3 flex gap-3 items-center">
                    <Image
                      src={u.avatar}
                      width={40}
                      height={40}
                      alt={u.name}
                      className="rounded-full"
                    />
                    <div>
                      <p className="font-semibold">{u.name}</p>
                      <p className="text-sm text-gray-400">{u.email}</p>
                    </div>
                  </div>

                  <div className="col-span-2">
                    <span className={`px-3 py-1 rounded text-sm ${
                      u.role === "Administrador" ? "bg-blue-600" : "bg-gray-700"
                    }`}>
                      {u.role}
                    </span>
                  </div>

             
                  <div className="col-span-3 text-gray-300">{u.registerDate}</div>

                
                  <div className="col-span-2">
                    <span className={`px-3 py-1 rounded text-sm ${
                      u.status === "Activo" ? "bg-green-600" : "bg-yellow-600"
                    }`}>
                      {u.status}
                    </span>
                  </div>

                  <div className="col-span-1 flex gap-3 justify-end">
                    <Pencil className="cursor-pointer hover:text-blue-400" />
                    <Trash2 className="cursor-pointer hover:text-red-400" />
                  </div>

                </div>
              ))}
            </div>


            {/*esta es la paginacion */}
            <div className="flex justify-between items-center mt-6 text-sm text-gray-400">
              <span>
                Mostrando {(currentPage - 1) * itemsPerPage + 1} -
                {Math.min(currentPage * itemsPerPage, filteredUsers.length)}
                {" "}de {filteredUsers.length}
              </span>

              <div className="flex gap-2">
                <Button
                  variant="outline"
                  className="bg-gray-900 border-gray-700"
                  onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                  disabled={currentPage === 1}
                >
                  Anterior
                </Button>

                {[...Array(totalPages)].map((_, i) => (
                  <Button
                    key={i}
                    variant={currentPage === i + 1 ? "default" : "outline"}
                    className={currentPage === i + 1 ? "bg-blue-600" : "bg-gray-900 border-gray-700"}
                    onClick={() => setCurrentPage(i + 1)}
                  >
                    {i + 1}
                  </Button>
                ))}

                <Button
                  variant="outline"
                  className="bg-gray-900 border-gray-700"
                  onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                  disabled={currentPage === totalPages}
                >
                  Siguiente
                </Button>
              </div>
            </div>

          </div>
        </SidebarInset>
      </div>
    </SidebarProvider>
  )
}
