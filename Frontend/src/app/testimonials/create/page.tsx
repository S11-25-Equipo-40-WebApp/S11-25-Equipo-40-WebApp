'use client'

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { Star } from "lucide-react"
import Navbar from "@/components/Navbar"

const API_URL = process.env.NEXT_PUBLIC_API_URL!
const API_KEY = process.env.NEXT_PUBLIC_API_KEY!

const PRODUCTS = [
  { id: "prd-react", name: "Curso React Básico" },
  { id: "prd-js", name: "Curso JavaScript" },
  { id: "prd-next", name: "Bootcamp Next.js" },
  { id: "prd-ui", name: "UI Design Masterclass" },
  { id: "prd-ai", name: "Introducción a IA" },
]

const getRandomProduct = () =>
  PRODUCTS[Math.floor(Math.random() * PRODUCTS.length)]

export default function NewTestimonialPage() {
  const [rating, setRating] = useState(0)
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)

  const [images, setImages] = useState<File[]>([])

  const [form, setForm] = useState({
    name: "",
    title: "",
    testimonial: "",
    videoUrl: "",
  })

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleImages = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files) return
    setImages(Array.from(e.target.files))
  }

  const handleSubmit = async () => {
    if (!form.name || !form.testimonial || rating === 0) {
      alert("Completa los campos obligatorios")
      return
    }

    try {
      setLoading(true)

      const product = getRandomProduct()

      let imageUrls: string[] = []

      if (images.length > 0) {
        const formData = new FormData()
        images.forEach(img => formData.append("files", img))

        const uploadRes = await fetch(
          `${API_URL}/testimonials/upload-images`,
          {
            method: "POST",
            headers: {
              "X-API-Key": API_KEY,
            },
            body: formData,
          }
        )

        if (!uploadRes.ok) {
          throw new Error("Error subiendo imágenes")
        }

        imageUrls = await uploadRes.json()
      }

      const res = await fetch(`${API_URL}/testimonials`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-API-Key": API_KEY,
        },
        body: JSON.stringify({
          product,
          content: {
            title: form.title,
            content: form.testimonial,
            rating,
            author_name: form.name,
          },
          media: {
            youtube_url: form.videoUrl || null,
            image_url: imageUrls,
          },
          category_name: "web",
          tags: ["public", "testimonial"],
        }),
      })

      if (!res.ok) {
        const error = await res.json()
        console.error(error)
        throw new Error("Error creando testimonio")
      }

      setSuccess(true)
      setForm({
        name: "",
        title: "",
        testimonial: "",
        videoUrl: "",
      })
      setRating(0)
      setImages([])
    } catch (err) {
      console.error(err)
      alert("No se pudo enviar el testimonio")
    } finally {
      setLoading(false)
    }
  }

  if (success) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#0f172a] text-white">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-2">¡Gracias! ⭐</h2>
          <p className="text-gray-400">
            Tu testimonio fue enviado y está pendiente de aprobación
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-[#0f172a] text-white">
      <Navbar />

      <div className="flex justify-center py-16 px-4">
        <div className="w-full max-w-3xl">

          <div className="text-center mb-10">
            <h1 className="text-3xl font-bold mb-2">
              Comparte tu experiencia
            </h1>
            <p className="text-gray-400 text-sm">
              Tu opinión es muy importante para nosotros
            </p>
          </div>

          <div className="bg-gray-900 p-6 rounded-xl border border-gray-700 mb-6">
            <h2 className="text-lg font-semibold mb-4">
              Información Básica
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label>Tu nombre *</Label>
                <Input
                  name="name"
                  value={form.name}
                  onChange={handleChange}
                  className="bg-gray-800 border-gray-700 mt-1"
                />
              </div>

              <div>
                <Label>Título</Label>
                <Input
                  name="title"
                  value={form.title}
                  onChange={handleChange}
                  className="bg-gray-800 border-gray-700 mt-1"
                />
              </div>
            </div>
          </div>

          <div className="bg-gray-900 p-6 rounded-xl border border-gray-700 mb-6">
            <h2 className="text-lg font-semibold mb-4">
              Tu experiencia
            </h2>

            <Label>Calificación *</Label>
            <div className="flex gap-2 mt-2 mb-4">
              {[1,2,3,4,5].map(star => (
                <Star
                  key={star}
                  onClick={() => setRating(star)}
                  className={`cursor-pointer ${
                    rating >= star ? "text-yellow-400" : "text-gray-600"
                  }`}
                  fill={rating >= star ? "#facc15" : "none"}
                />
              ))}
            </div>

            <Label>Testimonio *</Label>
            <Textarea
              name="testimonial"
              rows={5}
              value={form.testimonial}
              onChange={handleChange}
              className="bg-gray-800 border-gray-700 mt-1"
            />
          </div>

       
          <div className="bg-gray-900 p-6 rounded-xl border border-gray-700 mb-6">
            <h2 className="text-lg font-semibold mb-4">
              Multimedia (opcional)
            </h2>

            <Label>Imágenes</Label>
            <Input
              type="file"
              multiple
              accept="image/*"
              onChange={handleImages}
              className="bg-gray-800 border-gray-700 mt-1"
            />

            <Label className="mt-4">Video (YouTube)</Label>
            <Input
              name="videoUrl"
              value={form.videoUrl}
              onChange={handleChange}
              className="bg-gray-800 border-gray-700 mt-1"
            />
          </div>

          <Button
            className="w-full bg-blue-600 hover:bg-blue-700"
            disabled={loading}
            onClick={handleSubmit}
          >
            {loading ? "Enviando..." : "Enviar Testimonio"}
          </Button>
        </div>
      </div>
    </div>
  )
}
