import { useState } from 'react'
import { Outlet, useLocation } from 'react-router-dom'
import Navbar from './Navbar'
import Sidebar from './Sidebar'
import { useApp } from '../context/AppContext'

const API_URL = 'http://localhost:8000'

const Layout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const { current, addResult } = useApp()
  const location = useLocation()

  const handleAnalyze = async (source, language) => {
    setLoading(true)
    setError('')
    try {
      const res = await fetch(`${API_URL}/api/process`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ source, language }),
      })
      if (!res.ok) throw new Error('Request failed')
      addResult(await res.json(), source)
    } catch {
      setError('Could not process the video. Check that the backend is running.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-[#08090e]">
      <Navbar onMenuClick={() => setSidebarOpen(true)} />
      <Sidebar
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        onAnalyze={handleAnalyze}
        loading={loading}
        error={error}
        hasResult={Boolean(current)}
      />

      <main className="min-h-screen pt-12 md:pl-64">
        <div className={`mx-auto px-5 py-8 sm:px-8 lg:px-10 ${location.pathname === '/history' ? 'max-w-5xl' : 'max-w-[1500px]'}`}>
          <Outlet context={{ loading }} />
        </div>
      </main>
    </div>
  )
}

export default Layout