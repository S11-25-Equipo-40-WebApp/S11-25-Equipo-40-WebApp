"use client";

import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/Sidebar";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Search, Trash2, Pencil } from "lucide-react";
import { ReactNode, useEffect, useState, useCallback } from "react";
import Image from "next/image";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";


const API_URL = "https://testify-dwtn.onrender.com/api";

interface User {
  registerDate: ReactNode;
  id: string;
  name: string;
  surname: string;
  email: string;
  role: string;
  is_active: boolean;
  created_at: string;
  avatar?: string;
}

export default function UsuariosPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [filteredUsers, setFilteredUsers] = useState<User[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedRole, setSelectedRole] = useState("all");
  const [selectedStatus, setSelectedStatus] = useState("all");
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 4;

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  
  const [openDeleteModal, setOpenDeleteModal] = useState(false);
  const [deleteId, setDeleteId] = useState<string | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [openCreateModal, setOpenCreateModal] = useState(false);
  const [editId, setEditId] = useState<string | null>(null);
  
  const getAuthHeaders = () => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null
    return {
      "Content-Type": "application/json",
      ...(token ? { "Authorization": `Bearer ${token}` } : {})
    }
  }
  
  const [form, setForm] = useState({
    name: "",
    surname: "",
    email: "",
    password: "",
    role: "moderator",
  });

  const fetchUsers = useCallback(async () => {
    try {
      setLoading(true);

      const res = await fetch(`${API_URL}/users`, {
        headers: getAuthHeaders(),
      });
      if (!res.ok) throw new Error("Error obteniendo usuarios");

      const data = await res.json();
      
      // Los usuarios están en data.results
      const usersList = Array.isArray(data) ? data : data.results || [];

      const mapped = usersList.map((u: User) => ({
        ...u,
        name: u.name || u.email.split('@')[0],
        surname: u.surname || "",
        status: u.is_active ? "Activo" : "Inactivo",
        registerDate: new Date(u.created_at).toLocaleDateString("es-MX"),
        avatar:
          u.avatar ||
          "https://cdn-icons-png.flaticon.com/512/3177/3177440.png", 
      }));

      setUsers(mapped);
      setFilteredUsers(mapped);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error desconocido");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchUsers();
  }, [fetchUsers]);

  useEffect(() => {
    let filtered = users;

    if (searchTerm) {
      filtered = filtered.filter(
        (u) =>
          u.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          u.email.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (selectedRole !== "all") {
      filtered = filtered.filter((u) => u.role === selectedRole);
    }

    if (selectedStatus !== "all") {
      filtered = filtered.filter(
        (u) =>
          (selectedStatus === "Activo" && u.is_active) ||
          (selectedStatus === "Inactivo" && !u.is_active)
      );
    }

    setFilteredUsers(filtered);
    setCurrentPage(1);
  }, [searchTerm, selectedRole, selectedStatus, users]);

  
  const paginated = filteredUsers.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  const totalPages = Math.ceil(filteredUsers.length / itemsPerPage);

  const handleSelectAll = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.checked) {
      setSelectedIds(new Set(paginated.map((u) => u.id)));
    } else {
      setSelectedIds(new Set());
    }
  };

  const handleSelectItem = (id: string) => {
    const updated = new Set(selectedIds);
    if (updated.has(id)) {
      updated.delete(id);
    } else {
      updated.add(id);
    }
    setSelectedIds(updated);
  };

  const createUser = async () => {
    try {
      const method = isEditing && editId ? "PATCH" : "POST";
      const url = isEditing && editId ? `${API_URL}/users/${editId}` : `${API_URL}/users`;

      const res = await fetch(url, {
        method,
        headers: getAuthHeaders(),
        body: JSON.stringify(form),
      });

      if (!res.ok) {
        alert(isEditing ? "Error actualizando usuario" : "Error creando usuario");
        return;
      }

      setOpenCreateModal(false);
      setIsEditing(false);
      setEditId(null);
      setForm({ name: "", surname: "", email: "", password: "", role: "moderator" });

      fetchUsers();
    } catch (err) {
      console.error(err);
      alert("Error en la petición");
    }
  };

  
  const deleteUser = async () => {
    if (!deleteId) return;

    const res = await fetch(`${API_URL}/users/delete/${deleteId}`, {
      method: "PATCH",
      headers: getAuthHeaders(),
      body: JSON.stringify({ is_active: false }),
    });

    if (!res.ok) {
      alert("Error eliminando usuario");
      return;
    }

    setOpenDeleteModal(false);
    setDeleteId(null);
    fetchUsers();
  };

  if (loading) {
    return (
      <div className="flex min-h-screen w-full bg-[#0f172a] text-white items-center justify-center">
        Cargando...
      </div>
    );
  }

  return (
    <SidebarProvider>
      <div className="flex w-full min-h-screen bg-[#0f172a] text-white">
        <AppSidebar />

        <SidebarInset className="bg-[#0f172a]">
          <div className="p-8">
            {/* HEADER */}
            <div className="flex justify-between items-center mb-6">
              <h1 className="text-3xl font-bold">Gestión de Usuarios</h1>
              <Button
                className="bg-blue-600 hover:bg-blue-700"
                onClick={() => setOpenCreateModal(true)}
              >
                + Añadir Nuevo Usuario
              </Button>
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
                onChange={(e) => setSelectedRole(e.target.value)}
              >
                <option value="all">Rol: Todos</option>
                <option value="owner">Administrador</option>
                <option value="moderator">Usuario</option>
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
                <div>
                  <input type="checkbox" onChange={handleSelectAll} />
                </div>
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
                      src={u.avatar || "/default-avatar.png"}
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
                    <span
                      className={`px-3 py-1 rounded text-sm ${
                        u.role === "owner"
                          ? "bg-blue-600"
                          : "bg-gray-700"
                      }`}
                    >
                      {u.role}
                    </span>
                  </div>

                  <div className="col-span-3 text-gray-300">
                    {u.registerDate}
                  </div>

                  <div className="col-span-2">
                    <span
                      className={`px-3 py-1 rounded text-sm ${
                        u.is_active ? "bg-green-600" : "bg-yellow-600"
                      }`}
                    >
                      {u.is_active ? "Activo" : "Inactivo"}
                    </span>
                  </div>

                  <div className="col-span-1 flex gap-3 justify-end">
                    <Pencil
                      className="cursor-pointer hover:text-blue-400"
                      onClick={() => {
                        setIsEditing(true);
                        setEditId(u.id);
                        setForm({
                          name: u.name,
                          surname: u.surname,
                          email: u.email,
                          password: "",
                          role: u.role,
                        });
                        setOpenCreateModal(true);
                      }}
                    />
                    <Trash2
                      className="cursor-pointer hover:text-red-400"
                      onClick={() => {
                        setDeleteId(u.id);
                        setOpenDeleteModal(true);
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>

            <div className="flex justify-between items-center mt-6 text-sm text-gray-400">
              <span>
                Mostrando {(currentPage - 1) * itemsPerPage + 1} -
                {Math.min(currentPage * itemsPerPage, filteredUsers.length)} de{" "}
                {filteredUsers.length}
              </span>

              <div className="flex gap-2">
                <Button
                  variant="outline"
                  className="bg-gray-900 border-gray-700"
                  onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
                  disabled={currentPage === 1}
                >
                  Anterior
                </Button>

                {[...Array(totalPages)].map((_, i) => (
                  <Button
                    key={i}
                    variant={currentPage === i + 1 ? "default" : "outline"}
                    className={
                      currentPage === i + 1
                        ? "bg-blue-600"
                        : "bg-gray-900 border-gray-700"
                    }
                    onClick={() => setCurrentPage(i + 1)}
                  >
                    {i + 1}
                  </Button>
                ))}

                <Button
                  variant="outline"
                  className="bg-gray-900 border-gray-700"
                  onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
                  disabled={currentPage === totalPages}
                >
                  Siguiente
                </Button>
              </div>
            </div>
          </div>
        </SidebarInset>
      </div>

   
      <Dialog open={openDeleteModal} onOpenChange={setOpenDeleteModal}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Confirmar Eliminación</DialogTitle>
          </DialogHeader>
          <p>¿Seguro que deseas desactivar este usuario?</p>

          <DialogFooter>
            <Button variant="outline" onClick={() => setOpenDeleteModal(false)}>
              Cancelar
            </Button>
            <Button variant="destructive" onClick={deleteUser}>
              Eliminar
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

        <Dialog open={openCreateModal} onOpenChange={setOpenCreateModal}>
        <DialogContent className="bg-[#0f172a] text-white border border-slate-700 shadow-xl rounded-xl">
          <DialogHeader>
            <DialogTitle className="text-xl font-semibold text-white">
              {isEditing ? "Editar Usuario" : "Crear Usuario"}
            </DialogTitle>
          </DialogHeader>

          <div className="grid gap-4 mt-4">
            <Input
              className="bg-slate-800 border-slate-700 text-white placeholder-slate-400"
              type="text"
              placeholder="Nombre"
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
            />

            <Input
              className="bg-slate-800 border-slate-700 text-white placeholder-slate-400"
              type="text"
              placeholder="Apellido"
              value={form.surname}
              onChange={(e) => setForm({ ...form, surname: e.target.value })}
            />

            <Input
              className="bg-slate-800 border-slate-700 text-white placeholder-slate-400"
              type="email"
              placeholder="Correo"
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
            />

            <Input
              className="bg-slate-800 border-slate-700 text-white placeholder-slate-400"
              type="password"
              placeholder="Contraseña"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
            />

            <select
              className="bg-slate-800 border border-slate-700 text-white rounded p-2"
              value={form.role}
              onChange={(e) => setForm({ ...form, role: e.target.value })}
            >
              <option value="moderator">Usuario</option>
              <option value="owner">Administrador</option>
            </select>
          </div>

          <DialogFooter className="mt-4">
            <Button
              className="border-slate-500 text-white hover:bg-slate-700"
              onClick={() => {
                setOpenCreateModal(false);
                setIsEditing(false);
                setEditId(null);
                setForm({ name: "", surname: "", email: "", password: "", role: "moderator" });
              }}
            >
              Cancelar
            </Button>

            <Button
              className="bg-indigo-600 hover:bg-indigo-700 text-white"
              onClick={createUser}
            >
              {isEditing ? "Actualizar" : "Crear"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

    </SidebarProvider>
  );
}
