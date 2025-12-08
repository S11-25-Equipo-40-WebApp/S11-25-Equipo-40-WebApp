'use client'

import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/Sidebar"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Search, Trash2, ThumbsUp } from "lucide-react"
import { useState, useEffect, ChangeEvent } from "react"
import Image from "next/image"
import Link from "next/link"

interface Testimonial {
  id: string
  user: string
  email: string
  product: string
  rating: number
  status: string
  excerpt: string
  avatar?: string
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:3001/api"

export default function TestimonialsPage() {
  const [testimonials, setTestimonials] = useState<Testimonial[]>([])
  const [filteredTestimonials, setFilteredTestimonials] = useState<Testimonial[]>([])
  const [currentPage, setCurrentPage] = useState<number>(1)
  const [searchTerm, setSearchTerm] = useState<string>("")
  const [selectedStatus, setSelectedStatus] = useState<string>("all")
  const [selectedProduct, setSelectedProduct] = useState<string>("all")
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set())

  const itemsPerPage = 3

  useEffect(() => {
    fetchTestimonials()
  }, [])

  const fetchTestimonials = async () => {
    try {
      setLoading(true)
      const response = await fetch(`${API_URL}/testimonials`)
      if (!response.ok) throw new Error("Error fetching testimonials")

      const data: Testimonial[] = await response.json()
      setTestimonials(data || [])
      setFilteredTestimonials(data || [])
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message)
      } else {
        setError("Error inesperado")
      }
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    let filtered = testimonials

    if (searchTerm) {
      filtered = filtered.filter(t =>
        t.user.toLowerCase().includes(searchTerm.toLowerCase()) ||
        t.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
        t.product.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    if (selectedStatus !== "all") {
      filtered = filtered.filter(t => t.status === selectedStatus)
    }

    if (selectedProduct !== "all") {
      filtered = filtered.filter(t => t.product === selectedProduct)
    }

    setFilteredTestimonials(filtered)
    setCurrentPage(1)
  }, [searchTerm, selectedStatus, selectedProduct, testimonials])

  const renderStars = (rating: number) => (
    <div className="flex gap-1">
      {[...Array(5)].map((_, i) => (
        <span key={i} className={i < rating ? "text-yellow-400" : "text-gray-600"}>★</span>
      ))}
    </div>
  )

  const handleSelectAll = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.checked) {
      setSelectedIds(new Set(paginatedTestimonials.map(t => t.id)))
    } else {
      setSelectedIds(new Set())
    }
  }

  const handleSelectItem = (id: string) => {
    const newSelected = new Set(selectedIds)
    newSelected.has(id) ? newSelected.delete(id) : newSelected.add(id)
    setSelectedIds(newSelected)
  }

  const handleApprove = async () => {
    await fetch(`${API_URL}/testimonials/approve`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ids: Array.from(selectedIds) }),
    })
    setSelectedIds(new Set())
    fetchTestimonials()
  }

  const handleDelete = async () => {
    if (!confirm("¿Estás seguro de eliminar los testimonios seleccionados?")) return

    await fetch(`${API_URL}/testimonials`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ids: Array.from(selectedIds) }),
    })
    setSelectedIds(new Set())
    fetchTestimonials()
  }

  const totalPages = Math.ceil(filteredTestimonials.length / itemsPerPage)
  const startIdx = (currentPage - 1) * itemsPerPage
  const paginatedTestimonials = filteredTestimonials.slice(startIdx, startIdx + itemsPerPage)

  const products = [...new Set(testimonials.map(t => t.product))]
  const statuses = [...new Set(testimonials.map(t => t.status))]

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[#0f172a] text-white">
        Cargando...
      </div>
    )
  }



  return (
    <SidebarProvider>
      <div className="flex min-h-screen w-full bg-[#0f172a] text-white">
        <AppSidebar />

        <SidebarInset className="bg-[#0f172a]">
          <div className="p-8">
            <div className="flex justify-between items-center mb-6">
            <h1 className="text-3xl font-bold">Gestión de Testimonios</h1>
              <Link href="/testimonials/create">
                <Button className="bg-blue-600 hover:bg-blue-700">+ Nuevo Testimonio</Button>
              </Link>
            </div>

            <div className="flex gap-4 mb-6">
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-3 w-4 h-4 text-gray-400" />
                <Input 
                  placeholder="Buscar por palabra clave, usuario o producto..." 
                  className="pl-10 bg-gray-900 border-gray-700 text-white"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>
              <select 
                className="bg-gray-900 border border-gray-700 rounded px-3 py-2 text-sm text-white"
                value={selectedStatus}
                onChange={(e) => setSelectedStatus(e.target.value)}
              >
                <option value="all">Estado</option>
                {statuses.map(status => (
                  <option key={status} value={status}>{status}</option>
                ))}
              </select>
              <select 
                className="bg-gray-900 border border-gray-700 rounded px-3 py-2 text-sm text-white"
                value={selectedProduct}
                onChange={(e) => setSelectedProduct(e.target.value)}
              >
                <option value="all">Producto</option>
                {products.map(product => (
                  <option key={product} value={product}>{product}</option>
                ))}
              </select>
            </div>

            <div className="flex gap-2 mb-6">
              <Button 
                className="bg-blue-600 hover:bg-blue-700 flex items-center gap-2"
                onClick={handleApprove}
                disabled={selectedIds.size === 0}
              >
                <ThumbsUp className="w-4 h-4" /> Aprobar Seleccionados
              </Button>
              <Button 
                className="bg-red-900 hover:bg-red-800 flex items-center gap-2"
                onClick={handleDelete}
                disabled={selectedIds.size === 0}
              >
                <Trash2 className="w-4 h-4" /> Eliminar Seleccionados
              </Button>
            </div>

            <div className="border border-gray-700 rounded-lg overflow-hidden">
              <div className="bg-gray-900 border-b border-gray-700 px-6 py-4 grid grid-cols-16 gap-4">
                <div className="col-span-1" title="Seleccionar Todos"><input type="checkbox" onChange={handleSelectAll} /></div>
                <div className="col-span-3 text-sm font-semibold">USUARIO</div>
                <div className="col-span-3 text-sm font-semibold">PRODUCTO</div>
                <div className="col-span-3 text-sm font-semibold">CALIFICACIÓN</div>
                <div className="col-span-3 text-sm font-semibold">EXTRACTO</div>
              </div>

              {paginatedTestimonials.length > 0 ? (
                paginatedTestimonials.map((item) => (
                  <div key={item.id} className="border-b border-gray-700 hover:bg-gray-900/50 px-6 py-4 grid grid-cols-12 gap-4 items-center">
                    <div className="col-span-1">
                      <input 
                        type="checkbox" 
                        checked={selectedIds.has(item.id)}
                        onChange={() => handleSelectItem(item.id)}
                      />
                    </div>
                    <div className="col-span-3 flex items-center gap-3">
                      {item.avatar && (
                        <Image 
                          src={item.avatar} 
                          alt={item.user}
                          width={40}
                          height={40}
                          className="rounded-full"
                        />
                      )}
                      <div>
                        <p className="font-semibold text-white">{item.user}</p>
                        <p className="text-gray-400 text-sm">{item.email}</p>
                      </div>
                    </div>
                    <div className="col-span-2 text-sm text-gray-300">{item.product}</div>
                    <div className="col-span-2">{renderStars(item.rating)}</div>
                    <div className="col-span-4 text-sm text-gray-300">{item.excerpt}</div>
                  </div>
                ))
              ) : (
                <div className="px-6 py-8 text-center text-gray-400">No hay testimonios</div>
              )}
            </div>

            <div className="flex justify-between items-center mt-6 text-sm text-gray-400">
              <span>Mostrando {startIdx + 1}-{Math.min(startIdx + itemsPerPage, filteredTestimonials.length)} de {filteredTestimonials.length}</span>
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
                    key={i + 1}
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