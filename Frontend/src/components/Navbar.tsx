import Link from "next/link";
import { UserCircle } from "lucide-react";

const Navbar = () => {
  return (
    <header className="w-full bg-[#0f172a] border-b border-gray-700 px-8 py-4 flex items-center justify-between">
      
    
      <div className="flex items-center gap-2 text-white font-bold text-lg">
          <div className="w-8 h-8 bg-blue-500 rounded-md flex items-center justify-center font-bold text-white">
            T
          </div>
        <span>Testimonials</span>
      </div>

      {/* Links */}
      <nav className="hidden md:flex items-center gap-8 text-gray-300">
        <Link href="/" className="hover:text-white transition">
          Inicio
        </Link>

        <Link href="/testimonials" className="hover:text-white transition">
          Ver Testimonios
        </Link>

        <Link href="/profile" className="hover:text-white transition">
          Mi Perfil
        </Link>
      </nav>

      {/* usuario */}
      <div className="flex items-center gap-3">
        <div className="bg-[#1e293b] p-2 rounded-full cursor-pointer hover:bg-[#334155] transition">
          <UserCircle size={28} className="text-white" />
        </div>
      </div>

    </header>
  );
};

export default Navbar;
