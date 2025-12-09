'use client'

import { useState } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Checkbox } from "@/components/ui/checkbox"

const RequirementItem = ({ met, text }: { met: boolean; text: string }) => (
  <div className="flex items-center gap-2 text-sm">
    <div className={`w-4 h-4 rounded-full flex items-center justify-center ${met ? 'bg-green-500' : 'bg-gray-600'}`}>
      {met && <span className="text-white text-xs">✓</span>}
    </div>
    <span className={met ? 'text-green-400' : 'text-gray-400'}>
      {text}
    </span>
  </div>
)

export default function HomePage() {
  // Estados para login
  const [loginEmail, setLoginEmail] = useState("")
  const [loginPassword, setLoginPassword] = useState("")

  // Estados para registro
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")

  // Feedback
  const [error, setError] = useState("")
  const [success, setSuccess] = useState("")

  // Validación de contraseña
  const validatePassword = (pwd: string)=> {
    return {
      hasLower: /[a-z]/.test(pwd),
      hasUpper: /[A-Z]/.test(pwd),
      hasNumber: /\d/.test(pwd),
      hasSpecial: /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(pwd),
      isLongEnough: pwd.length >= 8
    }
  }

  const passwordRequirements = validatePassword(password)
  const isPasswordValid = Object.values(passwordRequirements).every(v => v)

  const handleRegister = async () => {
    setError("")
    setSuccess("")

    if (!isPasswordValid) {
      setError("La contraseña no cumple con todos los requisitos")
      return
    }

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

      if (res.ok) {
        setSuccess("Registro exitoso. Inicia sesión para continuar.")
        setEmail("")
        setPassword("")
        setConfirmPassword("")
      } else {
        setError("Error en el registro. Intenta nuevamente.")
      }
    } catch (_err) {
      setError("Error de conexión. Intenta nuevamente."+ _err)
    }
  }

  const handleLogin = async () => {
    setError("")
    setSuccess("")
    
    if (!loginEmail || !loginPassword) {
      setError("Por favor, completa todos los campos.")
      return
    }

    try {
      const formData = new FormData()
      formData.append("username", loginEmail.trim())
      formData.append("password", loginPassword)

      const res = await fetch("https://testify-dwtn.onrender.com/api/auth/login", {
        method: "POST",
        body: formData
      })

      const data = await res.json()

      if (res.ok) {
        setSuccess("Login exitoso")
        localStorage.setItem("token", data.access_token)
        setTimeout(() => {
          window.location.href = "/home"
        }, 1000)
      } else {
        setError(data.detail?.[0]?.msg || data.detail || "Error en el inicio de sesión")
      }
    } catch (err) {
      setError("Error de conexión: " + (err instanceof Error ? err.message : "Desconocido"))
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

                <Button className="bg-blue-600 hover:bg-blue-700 transition w-full mt-2" onClick={handleLogin}>
                  Ingresar
                </Button>
              </TabsContent>

              {/* REGISTER */}
              <TabsContent value="register" className="space-y-4">
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
                  
                  {/* muestra al usuario los requerimmentos de la contraseña */}
                  {password && (
                    <div className="mt-3 p-3 bg-gray-700 rounded-lg space-y-2">
                      <RequirementItem met={passwordRequirements.hasLower} text="Letra minúscula (a-z)" />
                      <RequirementItem met={passwordRequirements.hasUpper} text="Letra mayúscula (A-Z)" />
                      <RequirementItem met={passwordRequirements.hasNumber} text="Número (0-9)" />
                      <RequirementItem met={passwordRequirements.hasSpecial} text="Carácter especial (!@#$%^&*)" />
                      <RequirementItem met={passwordRequirements.isLongEnough} text="Mínimo 8 caracteres" />
                    </div>
                  )}
                </div>

                <div>
                  <Label htmlFor="confirmPassword" className="text-gray-300 p-1">Confirmar contraseña</Label>
                  <Input id="confirmPassword" type="password" placeholder="Confirmar contraseña"
                    className="text-gray-300"
                    value={confirmPassword}
                    onChange={e => setConfirmPassword(e.target.value)} />
                  
                  {confirmPassword && password !== confirmPassword && (
                    <p className="text-red-400 text-sm mt-1">Las contraseñas no coinciden</p>
                  )}
                  {confirmPassword && password === confirmPassword && (
                    <p className="text-green-400 text-sm mt-1">✓ Las contraseñas coinciden</p>
                  )}
                </div>

                <Button
                  className="bg-blue-600 hover:bg-blue-700 transition w-full mt-2 disabled:opacity-50 disabled:cursor-not-allowed"
                  onClick={handleRegister}
                  disabled={!isPasswordValid || password !== confirmPassword}
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