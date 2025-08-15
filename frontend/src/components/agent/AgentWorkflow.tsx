import React, { useState, useEffect } from 'react'
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card'
import { Badge } from '../ui/Badge'
import { Progress } from '../ui/Progress'
import { Button } from '../ui/Button'

interface InsightStep {
  id: number
  title: string
  description: string
  status: 'pending' | 'in_progress' | 'completed' | 'error'
  progress: number
  estimatedTime?: string
  llmProvider?: string
  dataSource?: string[]
}

const INITIAL_INSIGHTS: InsightStep[] = [
  {
    id: 1,
    title: '市场宏观趋势 & 视觉偏好分析',
    description: '分析流行趋势、视觉风格偏好、预测趋势变化',
    status: 'completed',
    progress: 100,
    estimatedTime: '2-3分钟',
    llmProvider: 'Gemini Pro',
    dataSource: ['Vertex AI搜索', 'PyTrends', 'walmart_products']
  },
  {
    id: 2,
    title: '产品弱点 & 供应链痛点分析',
    description: '负面评价分析、痛点分类、质量问题识别',
    status: 'in_progress',
    progress: 65,
    estimatedTime: '3-4分钟',
    llmProvider: 'Claude',
    dataSource: ['walmart_product_reviews', 'amazon_reviews']
  },
  {
    id: 3,
    title: '潜在市场需求 & 产品创新机会',
    description: '市场空白识别、潜力评估、细分市场发现',
    status: 'pending',
    progress: 0,
    estimatedTime: '4-5分钟',
    llmProvider: 'Grok',
    dataSource: ['MindsDB聚合', 'Vertex AI搜索']
  },
  {
    id: 4,
    title: '季节性销售 & 定价策略分析',
    description: '价格段分析、促销模式识别、季节规律优化',
    status: 'pending',
    progress: 0,
    estimatedTime: '3-4分钟',
    llmProvider: 'GPT-4o',
    dataSource: ['walmart_products', 'amazon_products']
  },
  {
    id: 5,
    title: '产品功能 & 用户痛点关联性',
    description: '功能关键词提取、情感-功能关联、优化建议',
    status: 'pending',
    progress: 0,
    estimatedTime: '3-5分钟',
    llmProvider: 'Claude',
    dataSource: ['walmart_product_reviews', 'walmart_categories']
  },
  {
    id: 6,
    title: '品牌表现 & 竞争分析',
    description: '品牌表现聚合、竞争品牌分析、用户忠诚度洞察',
    status: 'pending',
    progress: 0,
    estimatedTime: '4-6分钟',
    llmProvider: 'Gemini Pro',
    dataSource: ['MindsDB全量', 'Vertex AI搜索']
  }
]

interface AgentWorkflowProps {
  isRunning?: boolean
  onStartAnalysis?: () => void
  onPauseAnalysis?: () => void
  onResetAnalysis?: () => void
}

export const AgentWorkflow: React.FC<AgentWorkflowProps> = ({
  isRunning = false,
  onStartAnalysis,
  onPauseAnalysis,
  onResetAnalysis
}) => {
  const [insights, setInsights] = useState<InsightStep[]>(INITIAL_INSIGHTS)
  const [currentStep, setCurrentStep] = useState<number>(2)
  const [overallProgress, setOverallProgress] = useState<number>(27)
  const [estimatedTimeRemaining, setEstimatedTimeRemaining] = useState<string>('15-20分钟')

  // 模拟进度更新
  useEffect(() => {
    if (!isRunning) return

    const interval = setInterval(() => {
      setInsights(prev => {
        const updated = [...prev]
        const currentInsight = updated.find(insight => insight.status === 'in_progress')
        
        if (currentInsight && currentInsight.progress < 100) {
          currentInsight.progress = Math.min(100, currentInsight.progress + Math.random() * 15)
          
          // 如果当前洞察完成，移动到下一个
          if (currentInsight.progress >= 100) {
            currentInsight.status = 'completed'
            const nextIndex = updated.findIndex(insight => insight.status === 'pending')
            if (nextIndex !== -1) {
              updated[nextIndex].status = 'in_progress'
              setCurrentStep(updated[nextIndex].id)
            }
          }
        }
        
        return updated
      })

      // 更新整体进度
      setOverallProgress(prev => {
        const completedCount = insights.filter(i => i.status === 'completed').length
        const inProgressCount = insights.filter(i => i.status === 'in_progress').length
        const inProgressProgress = insights.find(i => i.status === 'in_progress')?.progress || 0
        
        return Math.min(100, (completedCount * 100 + inProgressProgress * inProgressCount) / insights.length)
      })
    }, 2000)

    return () => clearInterval(interval)
  }, [isRunning, insights])

  const getStatusColor = (status: InsightStep['status']) => {
    switch (status) {
      case 'completed': return 'bg-green-500'
      case 'in_progress': return 'bg-blue-500 animate-pulse'
      case 'error': return 'bg-red-500'
      default: return 'bg-gray-300'
    }
  }

  const getStatusBadge = (status: InsightStep['status']) => {
    switch (status) {
      case 'completed': return <Badge variant="success">完成</Badge>
      case 'in_progress': return <Badge variant="processing">分析中</Badge>
      case 'error': return <Badge variant="destructive">错误</Badge>
      default: return <Badge variant="outline">等待</Badge>
    }
  }

  const getLlmProviderColor = (provider?: string) => {
    switch (provider) {
      case 'Gemini Pro': return 'bg-blue-100 text-blue-800'
      case 'Claude': return 'bg-purple-100 text-purple-800'
      case 'Grok': return 'bg-green-100 text-green-800'
      case 'GPT-4o': return 'bg-orange-100 text-orange-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg flex items-center justify-between">
          <span>Agent工作流</span>
          <div className="flex gap-2">
            {!isRunning ? (
              <Button 
                size="sm" 
                onClick={onStartAnalysis}
                className="text-xs"
              >
                开始分析
              </Button>
            ) : (
              <Button 
                size="sm" 
                variant="outline" 
                onClick={onPauseAnalysis}
                className="text-xs"
              >
                暂停
              </Button>
            )}
            <Button 
              size="sm" 
              variant="outline" 
              onClick={onResetAnalysis}
              className="text-xs"
            >
              重置
            </Button>
          </div>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="mb-6">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium">六层洞察分析进度</span>
            <span className="text-sm text-muted-foreground">{Math.round(overallProgress)}%</span>
          </div>
          <Progress value={overallProgress} showLabel={false} />
          <div className="flex justify-between items-center mt-2 text-xs text-muted-foreground">
            <span>第 {currentStep} 层洞察进行中</span>
            <span>预计剩余: {estimatedTimeRemaining}</span>
          </div>
        </div>

        <div className="space-y-4">
          {insights.map((insight) => (
            <div key={insight.id} className="border border-border rounded-lg p-4 hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-3">
                  <div className={`w-3 h-3 rounded-full ${getStatusColor(insight.status)}`}></div>
                  <div>
                    <h4 className="font-medium text-sm">{insight.title}</h4>
                    <p className="text-xs text-muted-foreground mt-1">{insight.description}</p>
                  </div>
                </div>
                {getStatusBadge(insight.status)}
              </div>

              {insight.status === 'in_progress' && (
                <div className="mb-3">
                  <Progress value={insight.progress} showLabel={false} />
                  <div className="flex justify-between text-xs text-muted-foreground mt-1">
                    <span>{Math.round(insight.progress)}% 完成</span>
                    <span>预计用时: {insight.estimatedTime}</span>
                  </div>
                </div>
              )}

              <div className="flex flex-wrap gap-2 mt-3">
                {insight.llmProvider && (
                  <span className={`px-2 py-1 rounded text-xs font-medium ${getLlmProviderColor(insight.llmProvider)}`}>
                    {insight.llmProvider}
                  </span>
                )}
                {insight.dataSource?.map((source, index) => (
                  <span key={index} className="px-2 py-1 bg-accent text-accent-foreground rounded text-xs">
                    {source}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className="mt-6 p-4 bg-secondary rounded-lg">
          <h4 className="font-medium text-sm mb-2">洞察组合策略</h4>
          <div className="grid grid-cols-2 gap-2 text-xs">
            <div className="p-2 bg-background rounded border">
              <span className="font-medium">优质大众产品</span>
              <br />
              <span className="text-muted-foreground">洞察1+2组合</span>
            </div>
            <div className="p-2 bg-background rounded border">
              <span className="font-medium">创新细分产品</span>
              <br />
              <span className="text-muted-foreground">洞察3+6组合</span>
            </div>
            <div className="p-2 bg-background rounded border">
              <span className="font-medium">性能升级产品</span>
              <br />
              <span className="text-muted-foreground">洞察5+4组合</span>
            </div>
            <div className="p-2 bg-background rounded border">
              <span className="font-medium">高端艺术产品</span>
              <br />
              <span className="text-muted-foreground">洞察1+6组合</span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}