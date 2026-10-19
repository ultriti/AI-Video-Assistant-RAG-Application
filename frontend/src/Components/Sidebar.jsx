import { Link } from 'react-router-dom'
import { AudioLines, Brain, Captions, FileText, ListChecks, Sparkles, X } from 'lucide-react'
import SourceForm from './SourceForm'

const stages = [
  { label: 'Audio Processing', icon: AudioLines },
  { label: 'Transcription', icon: Captions },
  { label: 'Title Generation', icon: Sparkles },
  { label: 'Summarisation', icon: FileText },
  { label: 'Extraction', icon: ListChecks },
  { label: 'RAG Engine', icon: Brain },
]

const Sidebar = ({ open, onClose, onAnalyze, loading, error, hasResult }) => {
  return (
    <>
      {open && (
        <button aria-label="Close menu" className="fixed inset-0 z-30 bg-black/70 md:hidden" onClick={onClose} />
      )}

      <aside
        className={`fixed inset-y-0 left-0 z-40 flex w-64 flex-col border-r border-slate-800 bg-[#0d0e15] px-4 transition-transform md:translate-x-0 ${
          open ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <button
          onClick={onClose}
          className="absolute top-3 right-3 rounded-md p-1.5 text-slate-400 hover:bg-slate-800 md:hidden"
          aria-label="Close menu"
        >
          <X size={18} />
        </button>

        <Link to="/" onClick={onClose} className="border-b border-slate-800/90 py-5">
          <span className="block bg-gradient-to-r from-violet-300 via-fuchsia-300 to-indigo-400 bg-clip-text text-[26px] font-black leading-[0.95] tracking-tight text-transparent">
            AI<br />Video
          </span>
          <span className="mt-2 block text-[9px] font-bold tracking-[0.28em] text-slate-400">MEETING INTELLIGENCE</span>
        </Link>

        <div className="pt-5">
          <p className="mb-3 inline-flex rounded bg-violet-500/15 px-2 py-1 text-[9px] font-bold tracking-[0.18em] text-violet-300">INPUT</p>
          <SourceForm onSubmit={onAnalyze} loading={loading} error={error} compact />
        </div>

        <div className="mt-6 border-t border-slate-800/90 pt-5">
          <p className="mb-3 inline-flex rounded bg-emerald-500/15 px-2 py-1 text-[9px] font-bold tracking-[0.16em] text-emerald-300">PIPELINE STATUS</p>
          <ul className="space-y-2">
            {stages.map(({ label, icon: Icon }) => (
              <li key={label} className="flex items-center gap-2.5 rounded-lg border border-slate-800/80 bg-[#171821] px-3 py-2.5 text-[11px] text-slate-300">
                <span className={`h-1.5 w-1.5 shrink-0 rounded-full ${loading ? 'animate-pulse bg-amber-400' : hasResult ? 'bg-emerald-400' : 'bg-slate-600'}`} />
                <Icon size={13} className="text-slate-400" />
                {label}
              </li>
            ))}
          </ul>
        </div>

        <Link to="/history" onClick={onClose} className="mt-auto border-t border-slate-800 py-4 text-xs font-medium text-slate-400 hover:text-violet-300">
          View analysis history
        </Link>
      </aside>
    </>
  )
}

export default Sidebar