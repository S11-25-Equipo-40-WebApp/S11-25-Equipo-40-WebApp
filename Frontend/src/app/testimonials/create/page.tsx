'use client'

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { Star } from "lucide-react"
import Navbar from "@/components/Navbar"

export default function NewTestimonialPage() {

  const [rating, setRating] = useState(0)

  return (
    
    <div className="min-h-screen bg-[#0f172a] text-white">
      <Navbar />

      <div className="flex justify-center py-16 px-4">
      <div className="w-full max-w-3xl">

        <div className="text-center mb-10">
          <h1 className="text-3xl font-bold mb-2">
            Comparte tu opinión sobre <span className="text-blue-500">Testimonials</span>
          </h1>
          <p className="text-gray-400 text-sm">
            Tu opinión es muy importante para nosotros.
            Completa el formulario para compartir tu experiencia.
          </p>
        </div>



        {/* informacion basica */}
        <div className="bg-gray-900 p-6 rounded-xl border border-gray-700 mb-6">
          <h2 className="text-lg font-semibold mb-4">Información Básica</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label className=" mb-4">Tu nombre</Label>
              <Input 
                placeholder="Escribe tu nombre completo" 
                className="bg-gray-800 border-gray-700"
              />
            </div>

            <div>
              <Label className=" mb-4">Título de tu testimonio</Label>
              <Input 
                placeholder="Ej: ¡Un producto increíble!" 
                className="bg-gray-800 border-gray-700"
              />
            </div>
          </div>
        </div>



        {/* experiencia */}
        <div className="bg-gray-900 p-6 rounded-xl border border-gray-700 mb-6">
          <h2 className="text-lg font-semibold mb-4">Tu experiencia</h2>

          {/*estrellitas iji */}
          <div className="mb-6">
            <Label>Tu calificación</Label>

            <div className="flex gap-2 mt-2">
              {[1,2,3,4,5].map((star) => (
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

          <div>
            <Label className=" mb-4">Tu testimonio</Label>
            <Textarea 
              rows={5}
              placeholder="Describe tu experiencia en detalle..."
              className="bg-gray-800 border-gray-700"
            />
          </div>
        </div>




        {/* contnido mu,timedia */}
        <div className="bg-gray-900 p-6 rounded-xl border border-gray-700 mb-6">
          <h2 className="text-lg font-semibold mb-4">
            Contenido Multimedia <span className="text-gray-400 text-sm">(Opcional)</span>
          </h2>

          <p >Subir imagenes</p>
          <div className="border border-dashed border-gray-600 p-6 rounded-lg text-center mb-4 hover:border-gray-400 transition mt-2">
            <p className="text-gray-400 text-sm">
              Haz clic o arrastra una imagen aquí
            </p>
            <p className="text-xs text-gray-500 mt-1">
              PNG, JPG o GIF (MAX 5MB)
            </p>
          </div>

          {/* Vidio-enlace */}
          <div>
            <Label className=" mb-4">Enlace del video</Label>
            <Input 
              placeholder="https://youtube.com/..." 
              className="bg-gray-800 border-gray-700"
            />
          </div>
        </div>

        {/*botoncito */}
        <div className="text-center">
          <Button className="bg-blue-600 hover:bg-blue-700 px-10 py-5 text-lg rounded-full">
            Enviar Testimonio
          </Button>

          <p className="text-xs text-gray-500 mt-4">
            Al enviar tu testimonio aceptas nuestros Términos de Servicio y Política de Privacidad.
          </p>
        </div>
       </div>
      </div>
    </div>
  )
}
