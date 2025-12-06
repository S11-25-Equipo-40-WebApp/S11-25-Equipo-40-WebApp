'use client'

import { Card, CardContent } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Checkbox } from "@/components/ui/checkbox"

export default function HomePage() {
  return (
    <div className="flex min-h-screen">
     
      <div className="w-1/2 bg-gray-800 text-white flex flex-col justify-center items-center px-12">
        <div className="text-center max-w-md">
          <h2 className="text-2xl font-semibold mb-3">Testify</h2>
          <h1 className="text-4xl font-bold mb-4">
            Historias Reales.<br />Decisiones Inteligentes.
          </h1>
          <p className="text-gray-300">
            Únete a nuestra comunidad y descubre opiniones auténticas de productos para tomar siempre la mejor elección.
          </p>
        </div>
      </div>


      <div className="w-1/2 bg-[#0f172a] flex justify-center items-center">
        <Card className="w-[400px] bg-transparent border-none shadow-none">
          <CardContent>
            <h2 className="text-2xl font-bold text-white text-center mb-2">Bienvenido de Nuevo</h2>
            <p className="text-gray-400 text-center mb-6">Inicia sesión para continuar</p>

        <Tabs defaultValue="login" className="w-full">
           
            <TabsList className="grid grid-cols-2 bg-gray-800 rounded-lg mb-4">
              <TabsTrigger value="login">Iniciar Sesión</TabsTrigger>
              <TabsTrigger value="register">Registrarse</TabsTrigger>
            </TabsList>

          {/* esto es del login */}
          <TabsContent value="login" className="space-y-4">
            <div>
              <Label htmlFor="email" className="text-gray-300 p-1">Correo Electrónico</Label>
              <Input id="email" placeholder="tucorreo@ejemplo.com" type="email"  className="text-gray-300" />
            </div>

            <div>
              <Label htmlFor="password" className="text-gray-300 p-1">Contraseña</Label>
              <Input id="password" type="password" placeholder="Ingresa tu contraseña"  className="text-gray-300" />
            </div>

            <a href="#" className="block text-right text-sm text-blue-400 hover:underline">
              ¿Olvidaste tu contraseña?
            </a>

            <div className="flex items-center space-x-2">
              <Checkbox id="terms" />
              <Label htmlFor="terms" className="text-gray-300">
                Acepto los <a href="#" className="text-blue-400 hover:underline">Términos y Condiciones</a>
              </Label>
            </div>

            <Button className="bg-(--color-blue-btn) hover:bg-blue-700 transition w-full mt-2">Ingresar</Button>
          </TabsContent>

          {/* esto es del EGISTER */}
          <TabsContent value="register" className="space-y-4">
            <div>
              <Label htmlFor="nombre" className="text-gray-300 p-1">Nombre Completo</Label>
              <Input id="nombre" placeholder="Tu nombre" type="text" className="text-gray-300" />
            </div>

            <div>
              <Label htmlFor="emailReg" className="text-gray-300 p-1">Correo Electrónico</Label>
              <Input id="emailReg" placeholder="tucorreo@ejemplo.com" type="email"  className="text-gray-300" />
            </div>

            <div>
              <Label htmlFor="passwordReg" className="text-gray-300 p-1">Contraseña</Label>
              <Input id="passwordReg" type="password" placeholder="Crea una contraseña"  className="text-gray-300" />
            </div>

            <div>
              <Label htmlFor="passwordReg" className="text-gray-300 p-1">Confirmar contraseña</Label>
              <Input id="passwordReg" type="password" placeholder="Confirmar una contraseña"  className="text-gray-300" />
            </div>

            <Button className="bg-(--color-blue-btn) hover:bg-blue-700 transition w-full mt-2">Registrarse</Button>

          </TabsContent>
        </Tabs>

          </CardContent>
        </Card>
      </div>
    </div>
  )
}
