'use client';

import { useState } from 'react';


export default function HomePage() {
  const [testimonials] = useState([
    {
      id: 1,
      product: 'Smartwatch Pro 4',
      rating: 5,
      text: '"¡Producto increíble. La batería dura días completos y la calidad es excelente. Lo recomendaría"',
      author: 'Sarah Johnson',
      role: 'Cliente verificado',
      image: '/testimonials/watch.jpg'
    },
    {
      id: 2,
      product: 'Audífonos Gamer 2',
      rating: 5,
      text: '"El sonido es excelente y se el micrófono está increíble. Duran mucho tiempo de juego. El color..."',
      author: 'Mike Davis',
      role: 'Cliente verificado',
      image: '/testimonials/headphones.jpg'
    },
    {
      id: 3,
      product: 'Deportes Runner Light',
      rating: 4,
      text: '"Perfectas para entrenamientos matutinos, excelentes. El color es más oscuro en persona. Muy..."',
      author: 'David Lee',
      role: 'Cliente verificado',
      image: '/testimonials/shoes.jpg'
    }
  ]);
const handleCreateTestimonial = () => {
    window.location.href = '/testimonials/create';
  
  }
  return (
    <main className="bg-gray-900 text-white min-h-screen">
      {/* Hero Section */}
      <section className="px-6 py-20 md:py-32 flex flex-col md:flex-row items-center justify-between gap-12">
        <div className="flex-1">
          <h1 className="text-4xl md:text-5xl font-bold mb-4 leading-tight">
            Opiniones reales de<br />clientes reales
          </h1>
          <p className="text-gray-400 mb-8 text-lg">
            Descubre lo que nuestros consumidores piensan de nuestros productos a través de sus auténticas experiencias.
          </p>
          <button className="btn-primary bg-blue-500 rounded m-2 px-4 py-2 cursor-pointer hover:bg-blue-600" onClick={handleCreateTestimonial}>Comparte tu experiencia</button>
        </div>
        <div className="flex-1">
          <div className="bg-gradient-to-br from-cyan-400 to-purple-600 rounded-lg h-64 md:h-80"></div>
        </div>
      </section>

      {/* Últimos testimonios */}
      <section className="px-6 py-16">
        <h2 className="text-3xl font-bold mb-12">Últimos testimonios</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {testimonials.map((testimonial) => (
            <div key={testimonial.id} className="bg-gray-800 rounded-lg p-6 hover:bg-gray-750 transition">
              <div className="mb-4">
                <img 
                  src={testimonial.image} 
                  alt={testimonial.product} 
                  className="w-full h-40 object-cover rounded"
                />
              </div>
              <p className="text-yellow-400 text-sm mb-3">★ {testimonial.rating}/5</p>
              <h3 className="font-semibold mb-2">{testimonial.product}</h3>
              <p className="text-gray-300 text-sm mb-4 italic">{testimonial.text}</p>
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-gray-600 rounded-full"></div>
                <div>
                  <p className="font-semibold text-sm">{testimonial.author}</p>
                  <p className="text-gray-400 text-xs">{testimonial.role}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
        <div className="text-center">
          <button >Cargar más testimonios</button>
        </div>
      </section>
    </main>
  );
}