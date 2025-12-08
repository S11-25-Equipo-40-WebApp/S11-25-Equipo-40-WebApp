'use client'

import { useState } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Checkbox } from "@/components/ui/checkbox"

export default function HomePage() {
  // Estados para login
  const [loginEmail, setLoginEmail] = useState("")
  const [loginPassword, setLoginPassword] = useState("")

  // Estados para registro
  const [nombre, setNombre] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")

  // Feedback
  const [error, setError] = useState("")
  const [success, setSuccess] = useState("")

  const handleRegister = async () => {
    setError("")
    setSuccess("")

    if (password !== confirmPassword) {
      setError("Las contraseñas no coinciden")
      return
    }

    try {
      const res = await fetch("https://testify-dwtn.onrender.com/api/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      })

      if (!res.ok) {
        const data = await res.json()
        setError(data.message || "Error al registrar")
        return
      }

      const data = await res.json()
      setSuccess(`¡Registro exitoso! Bienvenido ${data.name || nombre}`)
    } catch (err) {
      setError("Error de conexión con el servidor")
    }
  }

  return (
    <div className="flex min-h-screen">
      {/* Lado izquierdo */}
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

      {/* Lado derecho */}
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

              {/* LOGIN */}
              <TabsContent value="login" className="space-y-4">
                <div>
                  <Label htmlFor="email" className="text-gray-300 p-1">Correo Electrónico</Label>
                  <Input id="email" type="email" placeholder="tucorreo@ejemplo.com"
                    className="text-gray-300"
                    value={loginEmail}
                    onChange={e => setLoginEmail(e.target.value)} />
                </div>

                <div>
                  <Label htmlFor="password" className="text-gray-300 p-1">Contraseña</Label>
                  <Input id="password" type="password" placeholder="Ingresa tu contraseña"
                    className="text-gray-300"
                    value={loginPassword}
                    onChange={e => setLoginPassword(e.target.value)} />
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

                <Button className="bg-(--color-blue-btn) hover:bg-blue-700 transition w-full mt-2">
                  Ingresar
                </Button>
              </TabsContent>

              {/* REGISTER */}
              <TabsContent value="register" className="space-y-4">
                <div>
                  <Label htmlFor="nombre" className="text-gray-300 p-1">Nombre Completo</Label>
                  <Input id="nombre" type="text" placeholder="Tu nombre"
                    className="text-gray-300"
                    value={nombre}
                    onChange={e => setNombre(e.target.value)} />
                </div>

                <div>
                  <Label htmlFor="emailReg" className="text-gray-300 p-1">Correo Electrónico</Label>
                  <Input id="emailReg" type="email" placeholder="tucorreo@ejemplo.com"
                    className="text-gray-300"
                    value={email}
                    onChange={e => setEmail(e.target.value)} />
                </div>

                <div>
                  <Label htmlFor="passwordReg" className="text-gray-300 p-1">Contraseña</Label>
                  <Input id="passwordReg" type="password" placeholder="Crea una contraseña"
                    className="text-gray-300"
                    value={password}
                    onChange={e => setPassword(e.target.value)} />
                </div>

                <div>
                  <Label htmlFor="confirmPassword" className="text-gray-300 p-1">Confirmar contraseña</Label>
                  <Input id="confirmPassword" type="password" placeholder="Confirmar contraseña"
                    className="text-gray-300"
                    value={confirmPassword}
                    onChange={e => setConfirmPassword(e.target.value)} />
                </div>

                <Button
                  className="bg-(--color-blue-btn) hover:bg-blue-700 transition w-full mt-2"
                  onClick={handleRegister}
                >
                  Registrarse
                </Button>

                {error && <p className="text-red-500 text-sm">{error}</p>}
                {success && <p className="text-green-500 text-sm">{success}</p>}
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}