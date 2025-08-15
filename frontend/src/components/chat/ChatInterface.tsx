import React, { useState, useRef, useEffect } from 'react'
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card'
import { Button } from '../ui/Button'
import { Badge } from '../ui/Badge'

interface ChatMessage {
  id: string
  type: 'user' | 'assistant' | 'system'
  content: string
  timestamp: Date
  status?: 'sending' | 'sent' | 'error'
  metadata?: {
    llmProvider?: string
    processingTime?: number
    dataSourcesUsed?: string[]
  }
}

const INITIAL_MESSAGES: ChatMessage[] = [
  {
    id: '1',
    type: 'system',
    content: '欢迎使用 Prodscope 产品推荐系统！我可以帮助您分析产品数据、识别市场趋势、发现商业机会。您可以问我关于产品分析、市场洞察或竞争分析的任何问题。',
    timestamp: new Date(Date.now() - 60000),
  },
  {
    id: '2',
    type: 'assistant',
    content: '当前已连接到 MindsDB (37,891条记录)、Vertex AI 搜索服务、以及 PyTrends 趋势分析。系统已准备就绪，您可以开始提问了！',
    timestamp: new Date(Date.now() - 30000),
    metadata: {
      llmProvider: 'System',
      dataSourcesUsed: ['MindsDB', 'Vertex AI', 'PyTrends']
    }
  }
]

const SUGGESTED_PROMPTS = [
  '分析沃尔玛圣诞装饰品的市场表现',
  '找出客户评价中最常见的产品问题',
  '对比沃尔玛和亚马逊的定价策略',
  '分析节日装饰品的季节性趋势',
  '识别高潜力的产品创新机会'
]

interface ChatInterfaceProps {
  onSendMessage?: (message: string) => Promise<any>
  isAnalysisRunning?: boolean
  className?: string
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({
  onSendMessage,
  isAnalysisRunning = false,
  className = ""
}) => {
  const [messages, setMessages] = useState<ChatMessage[]>(INITIAL_MESSAGES)
  const [inputMessage, setInputMessage] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: inputMessage.trim(),
      timestamp: new Date(),
      status: 'sent'
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsTyping(true)

    try {
      // 调用真实的API
      if (onSendMessage) {
        const apiResponse = await onSendMessage(userMessage.content)
        
        const assistantMessage: ChatMessage = {
          id: (Date.now() + 1).toString(),
          type: 'assistant',
          content: apiResponse.response,
          timestamp: new Date(apiResponse.timestamp),
          status: 'sent',
          metadata: {
            llmProvider: apiResponse.llm_provider,
            processingTime: Math.round(apiResponse.processing_time * 1000),
            dataSourcesUsed: apiResponse.data_sources_used || []
          }
        }
        setMessages(prev => [...prev, assistantMessage])
      }
    } catch (error) {
      console.error('Error getting response:', error)
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: '抱歉，处理您的请求时出现了错误。请稍后再试。',
        timestamp: new Date(),
        status: 'error',
        metadata: {
          llmProvider: 'Error',
          processingTime: 0,
          dataSourcesUsed: []
        }
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsTyping(false)
    }
  }

  const generateMockResponse = (userInput: string): string => {
    const responses = [
      `基于您的查询"${userInput}"，我已经分析了相关的产品数据。从MindsDB中的沃尔玛产品数据可以看出，这个领域确实有一些有趣的洞察。让我为您整理详细的分析报告...`,
      `好的，我来分析这个问题。根据当前数据源的信息，我发现了几个关键趋势。这需要结合多个数据维度来全面评估，包括销售数据、用户评价情感分析以及市场趋势...`,
      `这是一个很好的问题！从数据分析的角度，我需要查看多个指标。让我运行六层洞察分析来为您提供完整的答案，这可能需要几分钟时间...`,
      `根据当前的产品数据分析，我可以为您提供以下初步洞察。不过为了给您更准确的建议，我建议运行完整的Agent分析流程...`
    ]
    return responses[Math.floor(Math.random() * responses.length)]
  }

  const handleSuggestedPrompt = (prompt: string) => {
    setInputMessage(prompt)
    inputRef.current?.focus()
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const getMessageTypeColor = (type: ChatMessage['type']) => {
    switch (type) {
      case 'user': return 'bg-primary text-primary-foreground'
      case 'assistant': return 'bg-secondary text-secondary-foreground'
      case 'system': return 'bg-muted text-muted-foreground'
      default: return 'bg-background'
    }
  }

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="text-lg flex items-center justify-between">
          <span>智能对话助手</span>
          <div className="flex gap-2">
            {isTyping && (
              <Badge variant="processing" className="text-xs">
                分析中...
              </Badge>
            )}
            {isAnalysisRunning && (
              <Badge variant="outline" className="text-xs">
                Agent运行中
              </Badge>
            )}
          </div>
        </CardTitle>
      </CardHeader>
      <CardContent>
        {/* 消息历史区域 */}
        <div className="h-[600px] overflow-y-auto mb-4 space-y-4 p-4 border border-border rounded-lg bg-background">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[85%] p-4 rounded-lg ${getMessageTypeColor(message.type)}`}
              >
                <div className="text-sm whitespace-pre-wrap leading-relaxed">{message.content}</div>
                <div className="flex items-center justify-between mt-2 text-xs opacity-70">
                  <span>{message.timestamp.toLocaleTimeString()}</span>
                  {message.metadata && (
                    <div className="flex gap-1">
                      {message.metadata.llmProvider && (
                        <span className="px-1 bg-black/10 rounded">
                          {message.metadata.llmProvider}
                        </span>
                      )}
                      {message.metadata.processingTime && (
                        <span className="px-1 bg-black/10 rounded">
                          {message.metadata.processingTime}ms
                        </span>
                      )}
                    </div>
                  )}
                </div>
                {message.metadata?.dataSourcesUsed && (
                  <div className="flex flex-wrap gap-1 mt-1">
                    {message.metadata.dataSourcesUsed.map((source, index) => (
                      <span key={index} className="text-xs px-1 bg-black/5 rounded">
                        {source}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
          
          {isTyping && (
            <div className="flex justify-start">
              <div className="bg-secondary text-secondary-foreground p-3 rounded-lg">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-current rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-current rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-current rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* 建议提示 - 在对话完成后或初始状态时显示 */}
        {(!isTyping && !isAnalysisRunning) && (
          <div className="mb-3">
            <p className="text-xs text-muted-foreground mb-2">
              {messages.some(msg => msg.type === 'user') ? '继续提问:' : '推荐问题:'}
            </p>
            <div className="flex flex-wrap gap-1.5">
              {SUGGESTED_PROMPTS.map((prompt, index) => (
                <button
                  key={index}
                  onClick={() => handleSuggestedPrompt(prompt)}
                  className="inline-flex items-center px-2.5 py-1.5 text-xs bg-accent hover:bg-accent/80 rounded-lg border transition-colors whitespace-nowrap"
                  disabled={isTyping || isAnalysisRunning}
                >
                  {prompt}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* 输入区域 */}
        <div className="flex gap-2">
          <textarea
            ref={inputRef}
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="请输入您的问题或分析需求..."
            className="flex-1 min-h-[100px] p-3 border border-border rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
            disabled={isTyping}
          />
          <div className="flex flex-col gap-2">
            <Button
              onClick={handleSendMessage}
              disabled={!inputMessage.trim() || isTyping}
              size="sm"
              className="h-[50px] px-6"
            >
              发送
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setInputMessage('')}
              className="h-[50px] px-6"
            >
              清空
            </Button>
          </div>
        </div>

        <div className="mt-3 text-xs text-muted-foreground">
          提示: 按 Enter 发送消息，Shift+Enter 换行
        </div>
      </CardContent>
    </Card>
  )
}