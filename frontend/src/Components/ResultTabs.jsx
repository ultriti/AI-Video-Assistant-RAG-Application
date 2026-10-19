import { ChevronRight, FileText, ListChecks, MessageSquareText, Pin, CircleHelp } from 'lucide-react'

const ResultTabs = ({ result }) => {
  return (
    <div className="space-y-4">
      <section className="rounded-xl border border-slate-800 bg-[#101118] p-5 shadow-lg shadow-black/20 sm:p-6">
        <p className="flex items-center gap-2 text-[10px] font-bold tracking-[0.18em] text-violet-300">
          <Pin size={13} /> SESSION TITLE
        </p>
        <h2 className="mt-2 text-lg font-semibold text-slate-100 sm:text-xl">{result.title || 'Meeting Analysis'}</h2>
        {result.source && <p className="mt-1 truncate text-xs text-slate-500">{result.source}</p>}
      </section>

      <div className="grid items-start gap-4 lg:grid-cols-[minmax(0,1.4fr)_minmax(280px,0.9fr)]">
        <ResultCard title="Summary" icon={FileText} content={result.summary} className="min-h-64" />
        <details className="group rounded-xl border border-slate-800 bg-[#101118]">
          <summary className="flex cursor-pointer list-none items-center gap-2 px-4 py-3.5 text-sm font-semibold text-slate-200">
            <ChevronRight size={15} className="text-violet-300 transition group-open:rotate-90" />
            <FileText size={15} className="text-slate-400" />
            Full Transcript
          </summary>
          <div className="max-h-[28rem] overflow-y-auto border-t border-slate-800 px-4 py-4 text-sm leading-6 whitespace-pre-wrap text-slate-300">
            {result.transcript || 'No transcript found.'}
          </div>
        </details>
      </div>

      <div className="grid gap-4 xl:grid-cols-3">
        <ResultCard title="Action Items" icon={ListChecks} content={result.action_items} accent="emerald" />
        <ResultCard title="Key Decisions" icon={MessageSquareText} content={result.key_decisions} accent="cyan" />
        <ResultCard title="Open Questions" icon={CircleHelp} content={result.open_questions} accent="violet" />
      </div>
    </div>
  )
}

const ResultCard = ({ title, icon: Icon, content, accent = 'violet', className = '' }) => {
  const accents = {
    violet: 'before:bg-violet-500',
    emerald: 'before:bg-emerald-400',
    cyan: 'before:bg-cyan-400',
  }

  return (
    <section className={`relative overflow-hidden rounded-xl border border-slate-800 bg-[#101118] p-4 shadow-lg shadow-black/20 before:absolute before:inset-y-0 before:left-0 before:w-0.5 ${accents[accent]} ${className}`}>
      <h3 className="flex items-center gap-2 text-[10px] font-bold uppercase tracking-[0.18em] text-slate-400">
        <Icon size={14} className={accent === 'emerald' ? 'text-emerald-300' : accent === 'cyan' ? 'text-cyan-300' : 'text-violet-300'} />
        {title}
      </h3>
      <div className="mt-3 max-h-[27rem] overflow-y-auto text-sm leading-6 whitespace-pre-wrap text-slate-300">
        {content || `No ${title.toLowerCase()} found.`}
      </div>
    </section>
  )
}

export default ResultTabs