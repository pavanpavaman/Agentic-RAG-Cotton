'use client'

import { useState, useRef, useEffect } from 'react'
import { Send, Loader2, Sparkles, AlertCircle, Trash2, Copy, Check, Download, Edit2, RotateCcw, ArrowDown, History, Plus, MessageSquare, Menu, X } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import { motion, AnimatePresence } from 'framer-motion'

interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
  id: string
}

interface ChatSession {
  id: string
  title: string
  messages: Message[]
  createdAt: Date
  updatedAt: Date
}

const EXAMPLE_QUESTIONS = [
  "What are the main pests affecting cotton crops?",
  "How to control pink bollworm in cotton?",
  "What is the recommended dosage for whitefly control?",
  "What preventive measures can reduce pest infestation?",
  "What are the symptoms of cotton leaf curl disease?",
  "How to identify early signs of pest infestation?",
]

export default function Home() {
  const [chatSessions, setChatSessions] = useState<ChatSession[]>([])
  const [currentChatId, setCurrentChatId] = useState<string | null>(null)
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [editContent, setEditContent] = useState('')
  const [showScrollButton, setShowScrollButton] = useState(false)
  const [showSidebar, setShowSidebar] = useState(true)
  const [showHistory, setShowHistory] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const chatContainerRef = useRef<HTMLDivElement>(null)

  const currentChat = chatSessions.find(chat => chat.id === currentChatId)
  const messages = currentChat?.messages || []

  // Load chat sessions from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem('cotton-chat-sessions')
    if (saved) {
      try {
        const parsed = JSON.parse(saved)
        const sessions = parsed.map((s: any) => ({
          ...s,
          createdAt: new Date(s.createdAt),
          updatedAt: new Date(s.updatedAt),
          messages: s.messages.map((m: any) => ({
            ...m,
            timestamp: new Date(m.timestamp)
          }))
        }))
        setChatSessions(sessions)
        if (sessions.length > 0) {
          setCurrentChatId(sessions[0].id)
        }
      } catch (e) {
        console.error('Failed to load chat sessions:', e)
        createNewChat()
      }
    } else {
      createNewChat()
    }
  }, [])

  // Save chat sessions to localStorage
  useEffect(() => {
    if (chatSessions.length > 0) {
      localStorage.setItem('cotton-chat-sessions', JSON.stringify(chatSessions))
    }
  }, [chatSessions])

  const createNewChat = () => {
    const newChat: ChatSession = {
      id: Date.now().toString(),
      title: 'New Chat',
      messages: [],
      createdAt: new Date(),
      updatedAt: new Date()
    }
    setChatSessions(prev => [newChat, ...prev])
    setCurrentChatId(newChat.id)
  }

  const deleteChat = (chatId: string) => {
    if (confirm('Delete this conversation?')) {
      setChatSessions(prev => {
        const updated = prev.filter(c => c.id !== chatId)
        if (chatId === currentChatId) {
          setCurrentChatId(updated.length > 0 ? updated[0].id : null)
        }
        if (updated.length === 0) {
          setTimeout(createNewChat, 100)
        }
        return updated
      })
    }
  }

  const updateChatTitle = (chatId: string, firstMessage: string) => {
    const title = firstMessage.slice(0, 30) + (firstMessage.length > 30 ? '...' : '')
    setChatSessions(prev => prev.map(chat => 
      chat.id === chatId ? { ...chat, title, updatedAt: new Date() } : chat
    ))
  }

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  // Handle scroll detection
  useEffect(() => {
    const container = chatContainerRef.current
    if (!container) return

    const handleScroll = () => {
      const { scrollTop, scrollHeight, clientHeight } = container
      const isNearBottom = scrollHeight - scrollTop - clientHeight < 100
      setShowScrollButton(!isNearBottom && messages.length > 0)
    }

    container.addEventListener('scroll', handleScroll)
    return () => container.removeEventListener('scroll', handleScroll)
  }, [messages.length])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    if (error) {
      const timer = setTimeout(() => {
        setError(null)
      }, 8000) // Auto-dismiss after 8 seconds
      return () => clearTimeout(timer)
    }
  }, [error])

  const sendMessage = async (text?: string) => {
    const messageText = text || input
    if (!messageText.trim() || isLoading || !currentChatId) return

    const userMessage: Message = {
      role: 'user',
      content: messageText,
      timestamp: new Date(),
      id: Date.now().toString()
    }

    // Update current chat with new message
    setChatSessions(prev => prev.map(chat => {
      if (chat.id === currentChatId) {
        const updatedMessages = [...chat.messages, userMessage]
        // Update title with first message
        if (chat.messages.length === 0) {
          updateChatTitle(chat.id, messageText)
        }
        return { ...chat, messages: updatedMessages, updatedAt: new Date() }
      }
      return chat
    }))

    setInput('')
    setIsLoading(true)
    setError(null)

    try {
      // Get conversation context (last 5 messages for context)
      const context = messages.slice(-5).map(m => ({
        role: m.role,
        content: m.content
      }))

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          message: messageText,
          context: context
        }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()

      const assistantMessage: Message = {
        role: 'assistant',
        content: data.answer,
        timestamp: new Date(),
        id: (Date.now() + 1).toString()
      }

      setChatSessions(prev => prev.map(chat => 
        chat.id === currentChatId 
          ? { ...chat, messages: [...chat.messages, assistantMessage], updatedAt: new Date() }
          : chat
      ))
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An unexpected error occurred'
      if (errorMessage.includes('404') || errorMessage.includes('not found')) {
        setError('⚠️ AI service temporarily unavailable. Please try again later.')
      } else if (errorMessage.includes('NetworkError') || errorMessage.includes('Failed to fetch')) {
        setError('🔌 Unable to connect to the server. Please check your connection.')
      } else {
        setError('❌ Something went wrong. Please try asking a different question.')
      }
      console.error('Error:', err)
    } finally {
      setIsLoading(false)
    }
  }

  const regenerateResponse = async (userMessageId: string) => {
    if (!currentChatId) return
    
    const messageIndex = messages.findIndex(m => m.id === userMessageId)
    if (messageIndex === -1) return

    const userMessage = messages[messageIndex]
    
    // Remove this message and all subsequent ones
    setChatSessions(prev => prev.map(chat => 
      chat.id === currentChatId 
        ? { ...chat, messages: chat.messages.slice(0, messageIndex + 1) }
        : chat
    ))
    
    setIsLoading(true)
    setError(null)

    try {
      const context = messages.slice(0, messageIndex).slice(-5).map(m => ({
        role: m.role,
        content: m.content
      }))

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          message: userMessage.content,
          context: context
        }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()

      const assistantMessage: Message = {
        role: 'assistant',
        content: data.answer,
        timestamp: new Date(),
        id: Date.now().toString()
      }

      setChatSessions(prev => prev.map(chat => 
        chat.id === currentChatId 
          ? { ...chat, messages: [...chat.messages, assistantMessage] }
          : chat
      ))
    } catch (err) {
      setError('❌ Failed to regenerate response. Please try again.')
      console.error('Error:', err)
    } finally {
      setIsLoading(false)
    }
  }

  const startEdit = (message: Message) => {
    setEditingId(message.id)
    setEditContent(message.content)
  }

  const saveEdit = async () => {
    if (!editingId || !editContent.trim() || !currentChatId) return

    const messageIndex = messages.findIndex(m => m.id === editingId)
    if (messageIndex === -1) return

    const message = messages[messageIndex]

    // Update the message in the chat session
    setChatSessions(prev => prev.map(chat => {
      if (chat.id === currentChatId) {
        const updatedMessages = [...chat.messages]
        updatedMessages[messageIndex] = {
          ...updatedMessages[messageIndex],
          content: editContent
        }
        // Remove all messages after this one
        return { ...chat, messages: updatedMessages.slice(0, messageIndex + 1) }
      }
      return chat
    }))

    setEditingId(null)
    setEditContent('')

    // If it's a user message, regenerate the response
    if (message.role === 'user') {
      await regenerateResponse(editingId)
    }
  }

  const cancelEdit = () => {
    setEditingId(null)
    setEditContent('')
  }

  const deleteMessage = (id: string) => {
    if (!currentChatId) return
    const index = messages.findIndex(m => m.id === id)
    if (index !== -1) {
      setChatSessions(prev => prev.map(chat => 
        chat.id === currentChatId 
          ? { ...chat, messages: chat.messages.slice(0, index) }
          : chat
      ))
    }
  }

  const exportChat = () => {
    if (!currentChat) return
    const chatText = `${currentChat.title}\n${'='.repeat(currentChat.title.length)}\n\n` +
      messages.map(m => 
        `${m.role.toUpperCase()} [${m.timestamp.toLocaleString()}]:\n${m.content}\n\n`
      ).join('---\n\n')
    
    const blob = new Blob([chatText], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${currentChat.title.replace(/[^a-z0-9]/gi, '_')}-${new Date().toISOString().slice(0, 10)}.txt`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const copyToClipboard = async (text: string, index: number) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopiedIndex(index)
      setTimeout(() => setCopiedIndex(null), 2000)
    } catch (err) {
      console.error('Failed to copy:', err)
    }
  }

  const clearChat = () => {
    if (!currentChatId) return
    if (confirm('Clear all messages in this chat?')) {
      setChatSessions(prev => prev.map(chat => 
        chat.id === currentChatId 
          ? { ...chat, messages: [], title: 'New Chat' }
          : chat
      ))
      setError(null)
    }
  }

  return (
    <div className="min-h-screen flex">
      {/* Sidebar */}
      <AnimatePresence>
        {showSidebar && (
          <motion.aside
            initial={{ x: -300 }}
            animate={{ x: 0 }}
            exit={{ x: -300 }}
            className="w-64 bg-gray-900 text-white flex flex-col border-r border-gray-700 fixed h-full z-40"
          >
            <div className="p-4 border-b border-gray-700">
              <button
                onClick={createNewChat}
                className="w-full flex items-center justify-center space-x-2 px-4 py-3 bg-gradient-to-r from-cotton-600 to-cotton-700 hover:from-cotton-700 hover:to-cotton-800 rounded-lg transition-all duration-200 font-semibold shadow-lg"
              >
                <Plus className="w-5 h-5" />
                <span>New Chat</span>
              </button>
            </div>

            <div className="flex-1 overflow-y-auto">
              <div className="p-2 space-y-1">
                {chatSessions.map((chat) => (
                  <div
                    key={chat.id}
                    className={`group flex items-center space-x-2 p-3 rounded-lg cursor-pointer transition-colors ${
                      chat.id === currentChatId
                        ? 'bg-gray-800 border border-gray-600'
                        : 'hover:bg-gray-800/50'
                    }`}
                    onClick={() => setCurrentChatId(chat.id)}
                  >
                    <MessageSquare className="w-4 h-4 flex-shrink-0" />
                    <span className="flex-1 text-sm truncate">{chat.title}</span>
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        deleteChat(chat.id)
                      }}
                      className="opacity-0 group-hover:opacity-100 p-1 hover:bg-red-600 rounded transition-all"
                      title="Delete chat"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                ))}
              </div>
            </div>

            <div className="p-4 border-t border-gray-700">
              <div className="text-xs text-gray-400 text-center">
                {chatSessions.length} conversation{chatSessions.length !== 1 ? 's' : ''}
              </div>
            </div>
          </motion.aside>
        )}
      </AnimatePresence>

      {/* Main Content */}
      <div className={`flex-1 flex flex-col transition-all duration-300 ${showSidebar ? 'ml-64' : 'ml-0'}`}>
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md border-b border-gray-200 sticky top-0 z-30 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <button
                onClick={() => setShowSidebar(!showSidebar)}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                title="Toggle sidebar"
              >
                <Menu className="w-5 h-5 text-gray-600" />
              </button>
              <div className="w-10 h-10 bg-gradient-to-br from-cotton-500 to-cotton-600 rounded-xl flex items-center justify-center shadow-lg">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900 font-display">
                  {currentChat?.title || 'Cotton Advisory'}
                </h1>
                <p className="text-xs text-gray-600">AI-Powered Pest & Disease Management</p>
              </div>
            </div>
            {messages.length > 0 && (
              <div className="flex items-center space-x-2">
                <button
                  onClick={exportChat}
                  className="flex items-center space-x-2 px-3 py-2 text-green-600 hover:bg-green-50 rounded-lg transition-colors duration-200"
                  title="Export chat"
                >
                  <Download className="w-4 h-4" />
                  <span className="hidden md:inline">Export</span>
                </button>
                <button
                  onClick={clearChat}
                  className="flex items-center space-x-2 px-3 py-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors duration-200"
                >
                  <Trash2 className="w-4 h-4" />
                  <span className="hidden sm:inline">Clear</span>
                </button>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-5xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {messages.length === 0 ? (
          /* Welcome Screen */
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex flex-col items-center justify-center h-full space-y-8 py-12"
          >
            <div className="text-center space-y-4">
              <div className="w-20 h-20 bg-gradient-to-br from-cotton-400 to-cotton-600 rounded-2xl flex items-center justify-center mx-auto shadow-2xl">
                <Sparkles className="w-10 h-10 text-white" />
              </div>
              <h2 className="text-4xl font-bold text-gray-900 font-display">
                Welcome to Cotton Advisory
              </h2>
              <p className="text-xl text-gray-600 max-w-2xl">
                Get expert guidance on cotton pest and disease management based on ICAR-CICR Advisory 2024
              </p>
            </div>

            {/* Info Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 w-full max-w-4xl">
              {[
                { icon: '🐛', title: 'Pest Control', desc: 'Bollworms, whitefly, mealybugs & more' },
                { icon: '🦠', title: 'Disease Management', desc: 'Leaf curl, blight, wilt & others' },
                { icon: '💊', title: 'Treatment Plans', desc: 'Dosages & application methods' }
              ].map((item, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.1 }}
                  className="bg-white p-6 rounded-xl shadow-lg border border-gray-100 hover:shadow-xl transition-shadow duration-200"
                >
                  <div className="text-4xl mb-3">{item.icon}</div>
                  <h3 className="font-semibold text-gray-900 mb-2">{item.title}</h3>
                  <p className="text-sm text-gray-600">{item.desc}</p>
                </motion.div>
              ))}
            </div>

            {/* Example Questions */}
            <div className="w-full max-w-4xl space-y-3">
              <h3 className="text-lg font-semibold text-gray-700 text-center">Try these questions:</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {EXAMPLE_QUESTIONS.slice(0, 4).map((question, i) => (
                  <motion.button
                    key={i}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.3 + i * 0.1 }}
                    onClick={() => sendMessage(question)}
                    className="text-left p-4 bg-white hover:bg-cotton-50 border border-gray-200 hover:border-cotton-300 rounded-xl transition-all duration-200 shadow-sm hover:shadow-md group"
                  >
                    <p className="text-sm text-gray-700 group-hover:text-cotton-700 font-medium">
                      {question}
                    </p>
                  </motion.button>
                ))}
              </div>
            </div>
          </motion.div>
        ) : (
          /* Chat Messages */
          <div ref={chatContainerRef} className="space-y-6 pb-32 overflow-y-auto max-h-[calc(100vh-300px)]">
            <AnimatePresence>
              {messages.map((message, index) => (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} group`}
                >
                  <div className={`chat-message ${message.role === 'user' ? 'user-message' : 'assistant-message'} relative`}>
                    {/* Message Actions */}
                    <div className="absolute -top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity flex items-center space-x-1">
                      {editingId !== message.id && (
                        <>
                          <button
                            onClick={() => startEdit(message)}
                            className="p-1.5 bg-white border border-gray-200 hover:bg-gray-50 rounded-md shadow-sm transition-colors"
                            title="Edit message"
                          >
                            <Edit2 className="w-3.5 h-3.5 text-gray-600" />
                          </button>
                          {message.role === 'user' && index < messages.length - 1 && (
                            <button
                              onClick={() => regenerateResponse(message.id)}
                              className="p-1.5 bg-white border border-gray-200 hover:bg-gray-50 rounded-md shadow-sm transition-colors"
                              title="Regenerate response"
                              disabled={isLoading}
                            >
                              <RotateCcw className="w-3.5 h-3.5 text-blue-600" />
                            </button>
                          )}
                          <button
                            onClick={() => deleteMessage(message.id)}
                            className="p-1.5 bg-white border border-gray-200 hover:bg-red-50 rounded-md shadow-sm transition-colors"
                            title="Delete message"
                          >
                            <Trash2 className="w-3.5 h-3.5 text-red-600" />
                          </button>
                        </>
                      )}
                    </div>

                    {message.role === 'assistant' && (
                      <div className="flex items-center justify-between mb-2 pb-2 border-b border-gray-100">
                        <div className="flex items-center space-x-2">
                          <Sparkles className="w-4 h-4 text-cotton-600" />
                          <span className="text-xs font-semibold text-gray-600">Cotton Advisory AI</span>
                        </div>
                        <button
                          onClick={() => copyToClipboard(message.content, index)}
                          className="p-1 hover:bg-gray-100 rounded transition-colors duration-200"
                          title="Copy to clipboard"
                        >
                          {copiedIndex === index ? (
                            <Check className="w-4 h-4 text-green-600" />
                          ) : (
                            <Copy className="w-4 h-4 text-gray-400" />
                          )}
                        </button>
                      </div>
                    )}

                    {editingId === message.id ? (
                      <div className="space-y-2">
                        <textarea
                          value={editContent}
                          onChange={(e) => setEditContent(e.target.value)}
                          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cotton-500 focus:border-transparent resize-none"
                          rows={3}
                          autoFocus
                        />
                        <div className="flex items-center space-x-2">
                          <button
                            onClick={saveEdit}
                            className="px-3 py-1.5 bg-cotton-600 text-white rounded-md hover:bg-cotton-700 text-sm transition-colors"
                          >
                            Save & Regenerate
                          </button>
                          <button
                            onClick={cancelEdit}
                            className="px-3 py-1.5 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 text-sm transition-colors"
                          >
                            Cancel
                          </button>
                        </div>
                      </div>
                    ) : (
                      <>
                        <div className={`prose prose-sm max-w-none ${message.role === 'user' ? 'text-white prose-invert' : 'text-gray-800'}`}>
                          <ReactMarkdown>{message.content}</ReactMarkdown>
                        </div>
                        <div className={`text-xs mt-2 ${message.role === 'user' ? 'text-primary-100' : 'text-gray-400'}`}>
                          {message.timestamp.toLocaleTimeString()}
                        </div>
                      </>
                    )}
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>

            {isLoading && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="flex justify-start"
              >
                <div className="chat-message assistant-message">
                  <div className="flex items-center space-x-3">
                    <Loader2 className="w-5 h-5 animate-spin text-cotton-600" />
                    <span className="text-gray-600">Thinking...</span>
                  </div>
                </div>
              </motion.div>
            )}

            <div ref={messagesEndRef} />
          </div>
        )}

        {/* Error Message */}
        {error && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="fixed top-20 left-1/2 transform -translate-x-1/2 z-50 max-w-md w-full mx-4"
          >
            <div className="bg-red-50 border-2 border-red-200 text-red-800 px-6 py-4 rounded-2xl shadow-2xl">
              <div className="flex items-start space-x-3">
                <AlertCircle className="w-6 h-6 flex-shrink-0 mt-0.5" />
                <div className="flex-1">
                  <p className="font-semibold text-sm mb-1">Something went wrong</p>
                  <p className="text-sm leading-relaxed">{error}</p>
                </div>
                <button
                  onClick={() => setError(null)}
                  className="text-red-400 hover:text-red-600 transition-colors"
                  aria-label="Dismiss error"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
          </motion.div>
        )}

        {/* Scroll to Bottom Button */}
        <AnimatePresence>
          {showScrollButton && (
            <motion.button
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.8 }}
              onClick={scrollToBottom}
              className="fixed bottom-24 right-6 bg-cotton-600 text-white p-3 rounded-full shadow-lg hover:bg-cotton-700 transition-all duration-200 z-40"
              title="Scroll to bottom"
            >
              <ArrowDown className="w-5 h-5" />
            </motion.button>
          )}
        </AnimatePresence>

        {/* History Sidebar */}
        <AnimatePresence>
          {showHistory && (
            <>
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                onClick={() => setShowHistory(false)}
                className="fixed inset-0 bg-black/20 backdrop-blur-sm z-40"
              />
              <motion.div
                initial={{ x: 300, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                exit={{ x: 300, opacity: 0 }}
                className="fixed right-0 top-0 h-full w-80 bg-white shadow-2xl z-50 overflow-y-auto"
              >
                <div className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h2 className="text-lg font-bold text-gray-900">Chat History</h2>
                    <button
                      onClick={() => setShowHistory(false)}
                      className="text-gray-500 hover:text-gray-700"
                    >
                      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>
                  <div className="text-sm text-gray-600 mb-4">
                    {messages.length} messages • Auto-saved
                  </div>
                  <div className="space-y-3">
                    {messages.map((msg, idx) => (
                      <div
                        key={msg.id}
                        className={`p-3 rounded-lg border ${
                          msg.role === 'user' 
                            ? 'bg-cotton-50 border-cotton-200' 
                            : 'bg-gray-50 border-gray-200'
                        }`}
                      >
                        <div className="flex items-center space-x-2 mb-1">
                          <span className="text-xs font-semibold text-gray-500">
                            {msg.role === 'user' ? 'You' : 'AI'} • {msg.timestamp.toLocaleTimeString()}
                          </span>
                        </div>
                        <p className="text-sm text-gray-700 line-clamp-2">
                          {msg.content}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              </motion.div>
            </>
          )}
        </AnimatePresence>
      </main>

      {/* Input Area */}
      <div className="fixed bottom-0 left-0 right-0 bg-white/80 backdrop-blur-md border-t border-gray-200 shadow-lg">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-end space-x-3">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask about cotton pest management..."
              className="input-box resize-none"
              rows={2}
              disabled={isLoading}
            />
            <button
              onClick={() => sendMessage()}
              disabled={!input.trim() || isLoading}
              className="primary-button disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2 shrink-0"
            >
              {isLoading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <>
                  <Send className="w-5 h-5" />
                  <span className="hidden sm:inline">Send</span>
                </>
              )}
            </button>
          </div>
          <p className="text-xs text-gray-500 mt-2 text-center">
            Powered by ICAR-CICR Advisory 2024 • All answers include source citations
          </p>
        </div>
      </div>
      </div>
    </div>
  )
}
