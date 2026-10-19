import { useEffect, useRef, useState } from 'react'
import { Send } from 'lucide-react'

const API_URL = 'http://localhost:8000'

const ChatBox = ({ sessionId }) => {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = async (e) => {
    e.preventDefault()
    const question = input.trim()
    if (!question || loading) return

    setMessages((m) => [...m, { role: 'user', text: question }])
    setInput('')
    setLoading(true)

    try {
      const res = await fetch(`${API_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId, question }),
      })
      const data = await res.json()
      setMessages((m) => [...m, { role: 'assistant', text: data.answer }])
    } catch {
      setMessages((m) => [...m, { role: 'assistant', text: 'Something went wrong. Try again.' }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="rounded-xl border border-slate-800 bg-[#101118] shadow-lg shadow-black/20">
      <div className="border-b border-slate-800 px-5 py-3">
        <h3 className="text-sm font-semibold text-slate-100">Chat with this video</h3>
      </div>

      <div className="h-64 overflow-y-auto p-4 sm:h-72 sm:p-5">
        {messages.length === 0 && (
          <div className="flex h-full items-center justify-center">
            <p className="text-center text-sm text-slate-500">Ask anything about your meeting transcript</p>
          </div>
        )}
        {messages.length > 0 && (
          <div className="flex min-h-full flex-col justify-end gap-4">
            {messages.map((m, i) => {
              const isUser = m.role === 'user'

              return (
                <div
                  key={i}
                  className={`flex w-full ${isUser ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`flex max-w-[85%] flex-col gap-1 ${isUser ? 'items-end' : 'items-start'}`}>
                    <span className="px-1 text-[10px] font-semibold uppercase tracking-wider text-slate-500">
                      {isUser ? 'You' : 'AI'}
                    </span>
                    <div
                      className={`rounded-2xl px-4 py-2.5 text-sm leading-relaxed whitespace-pre-wrap ${
                        isUser
                          ? 'rounded-br-md bg-indigo-500 text-white'
                          : 'rounded-bl-md border border-slate-700 bg-slate-800 text-slate-200'
                      }`}
                    >
                      {m.text}
                    </div>
                  </div>
                </div>
              )
            })}
            {loading && (
              <div className="flex w-full justify-start">
                <div className="rounded-2xl rounded-bl-md border border-slate-700 bg-slate-800 px-4 py-2.5 text-sm text-slate-400">
                  AI is thinking...
                </div>
              </div>
            )}
            <div ref={bottomRef} />
          </div>
        )}
      </div>

      <form onSubmit={handleSend} className="flex gap-2 border-t border-slate-800 p-3">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your question..."
          className="flex-1 rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-100 outline-none placeholder:text-slate-500 focus:border-indigo-400"
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="rounded-lg bg-indigo-500 p-2.5 text-white hover:bg-indigo-400 disabled:opacity-50"
        >
          <Send size={16} />
        </button>
      </form>
    </div>
  )
}

export default ChatBox