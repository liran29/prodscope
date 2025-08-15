import { useState } from 'react'
import './App.css'
import { ChatInterface } from './components/chat'

function App() {
  const [isAnalysisRunning, setIsAnalysisRunning] = useState(false)

  return (
    <div className="prodscope-container">
      <header className="bg-primary text-primary-foreground p-4">
        <h1 className="text-2xl font-bold">Prodscope - 产品推荐</h1>
      </header>
      
      <main className="flex justify-center min-h-[calc(100vh-8rem)] p-6">
        <div className="w-full max-w-6xl">
          <ChatInterface 
            onSendMessage={async (message) => {
              console.log('Chat message sent:', message)
              setIsAnalysisRunning(true)
              
              try {
                // 调用真实的后端API
                const response = await fetch('http://localhost:8000/api/chat/message', {
                  method: 'POST',
                  headers: {
                    'Content-Type': 'application/json',
                  },
                  body: JSON.stringify({
                    message: message,
                    user_id: 'default',
                    session_id: 'default'
                  })
                })
                
                if (!response.ok) {
                  throw new Error('API request failed')
                }
                
                const data = await response.json()
                console.log('API Response:', data)
                
                return data
                
              } catch (error) {
                console.error('Error calling API:', error)
                throw error
              } finally {
                setIsAnalysisRunning(false)
              }
            }}
            isAnalysisRunning={isAnalysisRunning}
          />
        </div>
      </main>
    </div>
  )
}

export default App