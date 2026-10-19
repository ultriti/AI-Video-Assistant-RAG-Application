import React from 'react'
import { useNavigate } from 'react-router-dom'
import { Trash2, FileVideo } from 'lucide-react'
import { useApp } from '../../context/AppContext'

const HistoryPage = () => {
  const navigate = useNavigate()
  const { history, setCurrent, deleteResult } = useApp()

  const handleOpen = (item) => {
    setCurrent(item)
    navigate('/')
  }

  return (
    <div>
      <h1 className="text-xl font-semibold text-slate-100">History</h1>
      <p className="mt-1 text-sm text-slate-400">Your previously analyzed videos.</p>

      {history.length === 0 ? (
        <div className="mt-8 rounded-xl border border-dashed border-slate-700 bg-slate-900 p-10 text-center text-sm text-slate-500">
          No analyses yet.
        </div>
      ) : (
        <ul className="mt-6 space-y-3">
          {history.map((item) => (
            <li
              key={item.id}
              className="flex items-center justify-between gap-4 rounded-xl border border-slate-800 bg-slate-900 p-4 shadow-sm shadow-black/20"
            >
              <button
                onClick={() => handleOpen(item)}
                className="flex min-w-0 flex-1 items-center gap-3 text-left"
              >
                <div className="rounded-lg bg-indigo-500/15 p-2 text-indigo-300">
                  <FileVideo size={18} />
                </div>
                <div className="min-w-0">
                  <p className="truncate text-sm font-medium text-slate-100">{item.title}</p>
                  <p className="truncate text-xs text-slate-400">
                    {new Date(item.createdAt).toLocaleString()} · {item.source}
                  </p>
                </div>
              </button>

              <button
                onClick={() => deleteResult(item.id)}
                className="rounded-md p-2 text-slate-500 hover:bg-red-950 hover:text-red-300"
                aria-label="Delete"
              >
                <Trash2 size={16} />
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

export default HistoryPage