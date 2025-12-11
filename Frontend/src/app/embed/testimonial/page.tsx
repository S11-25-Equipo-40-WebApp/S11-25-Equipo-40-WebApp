'use client'

import { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { Star } from "lucide-react"

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:3001/api"

const PRODUCTS = [
  { id: "prd-react", name: "Curso React Básico" },
  { id: "prd-js", name: "Curso JavaScript" },
  { id: "prd-next", name: "Bootcamp Next.js" },
  { id: "prd-ui", name: "UI Design Masterclass" },
  { id: "prd-ai", name: "Introducción a IA" },
]

const getRandomProduct = () =>
  PRODUCTS[Math.floor(Math.random() * PRODUCTS.length)]

export default function EmbedTestimonialPage() {
  const [rating, setRating] = useState(0)
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [category, setCategory] = useState("")
  const [tag, setTag] = useState("")

  // nuevos estados para listas y selección múltiple de tags
  const [categoriesList, setCategoriesList] = useState<string[]>([])
  const [tagsList, setTagsList] = useState<string[]>([])
  const [selectedTags, setSelectedTags] = useState<string[]>([])

  // estados para permitir escribir categoría personalizada y añadir tags manualmente
  const [customCategory, setCustomCategory] = useState<string>("")
  const [isCustomCategory, setIsCustomCategory] = useState<boolean>(false)
  const [tagInput, setTagInput] = useState<string>("")

  // loading flags para evitar interacción hasta traer datos
  const [categoriesLoading, setCategoriesLoading] = useState<boolean>(true)
  const [tagsLoading, setTagsLoading] = useState<boolean>(true)

  const [images, setImages] = useState<File[]>([])

  const [form, setForm] = useState({
    name: "",
    title: "",
    testimonial: "",
    videoUrl: "",
  })

  // Cargar categorías y tags (endpoints específicos para embed) al montar el componente
  useEffect(() => {
    const load = async () => {
      setCategoriesLoading(true)
      setTagsLoading(true)
      try {
        const [cRes, tRes] = await Promise.all([
          fetch(`${API_URL}/categories`),
          fetch(`${API_URL}/tags`)
        ])

        if (cRes.ok) {
          const cData = await cRes.json()
          setCategoriesList(Array.isArray(cData) ? cData.map((i: any) => i?.name ?? i) : [])
        } else {
          setCategoriesList([])
        }

        if (tRes.ok) {
          const tData = await tRes.json()
          setTagsList(Array.isArray(tData) ? tData.map((i: any) => i?.name ?? i) : [])
        } else {
          setTagsList([])
        }
      } catch (err) {
        console.error("Error cargando categorías/tags:", err)
        setCategoriesList([])
        setTagsList([])
      } finally {
        setCategoriesLoading(false)
        setTagsLoading(false)
      }
    }

    load()
  }, [])

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
      setError("Completa los campos obligatorios")
      return
    }

    setError(null)
    setLoading(true)

    try {
      const product = getRandomProduct()
      let imageUrls: string[] = []

      if (images.length > 0) {
        const formData = new FormData()
        images.forEach(img => formData.append("files", img))

        const uploadRes = await fetch(`${API_URL}/testimonials/upload-images`, {
          method: "POST",
          body: formData,
        })

        if (!uploadRes.ok) {
          throw new Error("Error subiéndose las imágenes")
        }

        imageUrls = await uploadRes.json()
      }

      /* ---------------- aki se estan creando los testimonios ---------------- */
      const res = await fetch(`${API_URL}/testimonials`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
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
          category_name: category || customCategory || "embebido",
          tags: selectedTags.length ? selectedTags : ["embed", "testimonial"],
        }),
      })

      if (!res.ok) {
        throw new Error("Error del backend al crear testimonio")
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
      setError("Ocurrió un error al enviar tu testimonio")
    } finally {
      setLoading(false)
    }
  }

  if (success) {
    return (
      <div className="min-h-screen bg-[#0f172a] flex items-center justify-center text-white">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-2">¡Gracias! ⭐</h2>
          <p className="text-gray-400">
            Tu testimonio fue enviado correctamente
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-[#0f172a] flex items-center justify-center text-white">
      <div className="w-full max-w-lg bg-gray-900 border border-gray-700 rounded-xl p-6">
        <h1 className="text-xl font-bold text-center mb-2">
          Comparte tu experiencia
        </h1>
        <p className="text-sm text-gray-400 text-center mb-6">
          Nos encantaría conocer tu opinión
        </p>

        {error && (
          <p className="mb-4 text-sm text-red-400 text-center">{error}</p>
        )}

        <div className="mb-4">
          <Label>Tu nombre *</Label>
          <Input
            name="name"
            value={form.name}
            onChange={handleChange}
            className="bg-gray-800 border-gray-700 mt-1"
          />
        </div>

        <div className="mb-4">
          <Label>Título</Label>
          <Input
            name="title"
            value={form.title}
            onChange={handleChange}
            className="bg-gray-800 border-gray-700 mt-1"
          />
        </div>

        <div className="mb-4">
          <Label>Calificación *</Label>
          <div className="flex gap-2 mt-2">
            {[1, 2, 3, 4, 5].map(star => (
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
          <Label>Categorías *</Label>
          <div className="mt-1 flex gap-2 items-center">
            <select
              value={isCustomCategory ? "__other__" : category}
              onChange={(e) => {
                const v = e.target.value
                if (v === "__other__") {
                  setIsCustomCategory(true)
                  setCategory("")
                } else {
                  setIsCustomCategory(false)
                  setCategory(v)
                  setCustomCategory("")
                }
              }}
              disabled={categoriesLoading}
              className="flex-1 bg-gray-800 border-gray-700 p-2 rounded disabled:opacity-60"
            >
              <option value="">
                {categoriesLoading ? "Cargando categorías..." : "Selecciona una categoría"}
              </option>
              {categoriesList.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
              <option value="__other__">Otra...</option>
            </select>
            {isCustomCategory && (
              <input
                type="text"
                placeholder="Escribe la categoría"
                value={customCategory}
                onChange={(e) => setCustomCategory(e.target.value)}
                className="bg-gray-800 border border-gray-700 p-2 rounded flex-1"
              />
            )}
          </div>
        </div>

        <div className="mb-4">
          <Label>Tags</Label>
          <div className="mt-2">
            <div className="flex gap-2 mb-2">
              <input
                type="text"
                placeholder={tagsLoading ? "Cargando tags..." : "Añadir tag y presiona Enter"}
                value={tagInput}
                onChange={(e) => setTagInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    e.preventDefault()
                    const v = tagInput.trim()
                    if (v && !selectedTags.includes(v)) {
                      setSelectedTags((s) => [...s, v])
                    }
                    setTagInput("")
                  }
                }}
                disabled={tagsLoading}
                className="flex-1 bg-gray-800 border border-gray-700 p-2 rounded disabled:opacity-60"
              />
              <button
                type="button"
                onClick={() => {
                  const v = tagInput.trim()
                  if (v && !selectedTags.includes(v)) {
                    setSelectedTags((s) => [...s, v])
                  }
                  setTagInput("")
                }}
                disabled={tagsLoading}
                className="bg-blue-600 px-3 py-2 rounded disabled:opacity-60"
              >
                Añadir
              </button>
            </div>

            {/* click para añadir */}
            <div className="flex flex-wrap gap-2 mb-3">
              {tagsLoading ? (
                <span className="text-sm text-gray-400">Cargando sugerencias...</span>
              ) : (
                tagsList
                  .filter((t) => !selectedTags.includes(t))
                  .slice(0, 10)
                  .map((t) => (
                    <button
                      key={t}
                      type="button"
                      onClick={() => setSelectedTags((s) => (s.includes(t) ? s : [...s, t]))}
                      className="text-sm px-2 py-1 rounded bg-gray-800 hover:bg-gray-700"
                    >
                      {t}
                    </button>
                  ))
              )}
            </div>

            {/* Tags seleccionados */}
            <div className="flex flex-wrap gap-2">
              {selectedTags.map((t) => (
                <span
                  key={t}
                  className="flex items-center gap-2 bg-blue-600 text-white px-2 py-1 rounded text-sm"
                >
                  {t}
                  <button
                    type="button"
                    onClick={() => setSelectedTags((s) => s.filter((x) => x !== t))}
                    className="ml-1 text-xs px-1"
                    aria-label={`Eliminar ${t}`}
                  >
                    ×
                  </button>
                </span>
              ))}
            </div>
          </div>
        </div>

        <div className="mb-4">
          <Label>Tu testimonio *</Label>
          <Textarea
            name="testimonial"
            rows={4}
            value={form.testimonial}
            onChange={handleChange}
            className="bg-gray-800 border-gray-700 mt-1"
          />
        </div>

        <div className="mb-4">
          <Label>Imágenes (opcional)</Label>
          <Input
            type="file"
            multiple
            accept="image/*"
            onChange={handleImages}
            className="bg-gray-800 border-gray-700 mt-1"
          />
        </div>

        <div className="mb-6">
          <Label>Video (opcional)</Label>
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

        <p className="text-xs text-gray-500 text-center mt-4">
          Este formulario puede ser insertado en cualquier sitio web!!
        </p>
      </div>
    </div>
  )
}
