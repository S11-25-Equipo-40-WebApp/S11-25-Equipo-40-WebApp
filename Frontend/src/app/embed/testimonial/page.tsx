'use client'

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { Star } from "lucide-react"

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:3001/api"

export default function EmbedTestimonialPage() {
  const [rating, setRating] = useState(0)
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)

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

  const handleSubmit = async () => {
    if (!form.name || !form.testimonial || rating === 0) {
      alert("Por favor completa los campos obligatorios")
      return
    }

    try {
      setLoading(true)

      await fetch(`${API_URL}/testimonials`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user: form.name,
          title: form.title,
          content: form.testimonial,
          rating,
          videoUrl: form.videoUrl,
          source: "embed",
        }),
      })

      setSuccess(true)
      setForm({
        name: "",
        title: "",
        testimonial: "",
        videoUrl: "",
      })
      setRating(0)
    } catch (err) {
      console.error(err)
      alert("Error enviando testimonio")
    } finally {
      setLoading(false)
    }
  }

  if (success) {
    return (
      <div className="text-center p-10 text-white">
        <h2 className="text-2xl font-bold mb-2">¡Gracias! ⭐</h2>
        <p className="text-gray-400">
          Tu testimonio fue enviado correctamente
        </p>
      </div>
    )
  }

  return (
     <div className="min-h-screen bg-[#0f172a] text-white flex items-center justify-center">
       <div className="max-w-lg w-full bg-gray-900 border border-gray-700 rounded-xl p-6">
        <h1 className="text-xl font-bold text-center mb-2">
          Comparte tu experiencia
        </h1>
        <p className="text-sm text-gray-400 text-center mb-6">
          Nos encantaría conocer tu opinión
        </p>

        
        <div className="mb-4">
          <Label>Tu nombre *</Label>
          <Input
            name="name"
            value={form.name}
            onChange={handleChange}
            placeholder="Escribe tu nombre"
            className="bg-gray-800 border-gray-700 mt-1"
          />
        </div>

    
        <div className="mb-4">
          <Label>Título</Label>
          <Input
            name="title"
            value={form.title}
            onChange={handleChange}
            placeholder="Ej: Excelente servicio"
            className="bg-gray-800 border-gray-700 mt-1"
          />
        </div>

        
        <div className="mb-4">
          <Label>Calificación *</Label>
          <div className="flex gap-2 mt-2">
            {[1, 2, 3, 4, 5].map((star) => (
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
        </div>

       
        <div className="mb-4">
          <Label>Tu testimonio *</Label>
          <Textarea
            name="testimonial"
            rows={4}
            value={form.testimonial}
            onChange={handleChange}
            placeholder="Cuéntanos tu experiencia..."
            className="bg-gray-800 border-gray-700 mt-1"
          />
        </div>

    
        <div className="mb-6">
          <Label>Video (opcional)</Label>
          <Input
            name="videoUrl"
            value={form.videoUrl}
            onChange={handleChange}
            placeholder="https://youtube.com/..."
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

        <p className="text-xs text-gray-500 text-center mt-4">
          Este formulario puede ser insertado en cualquier sitio web
        </p>
      </div>
    </div>
  )
}
