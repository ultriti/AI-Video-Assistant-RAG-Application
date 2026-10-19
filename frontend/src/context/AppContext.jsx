import React, { createContext, useContext, useEffect, useState } from 'react'

const AppContext = createContext(null)

export const AppProvider = ({ children }) => {
  const [current, setCurrent] = useState(null)
  const [history, setHistory] = useState(() =>
    JSON.parse(localStorage.getItem('history') || '[]')
  )

  useEffect(() => {
    localStorage.setItem('history', JSON.stringify(history))
  }, [history])

  const addResult = (result, source) => {
    const item = { ...result, source, id: Date.now(), createdAt: new Date().toISOString() }
    setHistory((prev) => [item, ...prev])
    setCurrent(item)
  }

  const deleteResult = (id) => {
    setHistory((prev) => prev.filter((h) => h.id !== id))
    if (current?.id === id) setCurrent(null)
  }

  const resetCurrent = () => setCurrent(null)

  return (
    <AppContext.Provider
      value={{ current, setCurrent, history, addResult, deleteResult, resetCurrent }}
    >
      {children}
    </AppContext.Provider>
  )
}

export const useApp = () => useContext(AppContext)