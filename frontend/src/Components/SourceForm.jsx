import { useState } from 'react'
import { Link2, Loader2, Zap } from 'lucide-react'

const SourceForm = ({ onSubmit, loading, error, compact = false }) => {
  const [source, setSource] = useState('')
  const [language, setLanguage] = useState('english')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!source.trim()) return
    onSubmit(source.trim(), language)
  }

  return (
    <form
      onSubmit={handleSubmit}
      className={compact ? 'space-y-3' : 'rounded-xl border border-slate-800 bg-slate-900 p-6 shadow-lg shadow-black/20'}
    >
      {!compact && (
        <>
          <h2 className="text-lg font-semibold text-slate-100">Analyze a video or meeting</h2>
          <p className="mt-1 text-sm text-slate-400">
            Paste a YouTube link or a local file path to get a summary, action items and a chat.
          </p>
        </>
      )}

      <label className="block text-[11px] font-medium text-slate-300" htmlFor="video-source">YouTube URL or File Path</label>
      <div className="flex items-center gap-2 rounded-lg border border-slate-700 bg-[#181922] px-2.5 focus-within:border-violet-500 focus-within:ring-2 focus-within:ring-violet-500/15">
        <Link2 size={16} className="text-slate-500" />
        <input
          id="video-source"
          value={source}
          onChange={(e) => setSource(e.target.value)}
          placeholder="https://youtube.com/watch?v=... or C:\videos\meeting.mp4"
          className="w-full min-w-0 bg-transparent py-2.5 text-xs text-slate-100 outline-none placeholder:text-slate-500"
        />
      </div>

      <div>
        <label className="mb-1.5 block text-[11px] font-medium text-slate-300" htmlFor="analysis-language">Language</label>
        <select
          id="analysis-language"
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          className="w-full rounded-lg border border-slate-700 bg-[#181922] px-2.5 py-2 text-xs text-slate-200 outline-none focus:border-violet-500"
        >
          <option value="english">English</option>
          <option value="hinglish">Hinglish</option>
        </select>
      </div>

      <div className="flex flex-col gap-2">
        <button
          type="submit"
          disabled={loading || !source.trim()}
          className="inline-flex w-full items-center justify-center gap-2 rounded-lg border border-violet-400/15 bg-gradient-to-r from-violet-600/80 to-indigo-600/80 px-4 py-2.5 text-[11px] font-bold uppercase tracking-wider text-white transition hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading ? <Loader2 size={14} className="animate-spin" /> : <Zap size={13} />}
          {loading ? 'Processing...' : 'Analyze'}
        </button>
        {error && <p role="alert" className="text-[11px] leading-relaxed text-red-300">{error}</p>}
      </div>
    </form>
  )
}

export default SourceForm