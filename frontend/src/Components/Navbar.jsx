import { Menu } from 'lucide-react'
import { Link } from 'react-router-dom'

const Navbar = ({ onMenuClick }) => {
  return (
    <header className="fixed inset-x-0 top-0 z-30 flex h-12 items-center justify-end border-b border-slate-800/80 bg-[#0b0c12] px-5 md:left-64">
      <button
        onClick={onMenuClick}
        className="absolute left-3 rounded-md p-2 text-slate-400 hover:bg-slate-800 md:hidden"
        aria-label="Open menu"
      >
        <Menu size={20} />
      </button>

      <Link to="/history" className="text-xs font-semibold tracking-wide text-slate-400 transition hover:text-violet-300">
        HISTORY
      </Link>
    </header>
  )
}

export default Navbar