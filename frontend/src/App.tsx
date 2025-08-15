import { useState } from 'react'
import './App.css'
import { Card, CardHeader, CardTitle, CardContent } from './components/ui/Card'
import { Button } from './components/ui/Button'
import { Badge } from './components/ui/Badge'
import { TrendChart, BarChartComponent } from './components/visualizations'
import { AgentWorkflow } from './components/agent'
import { DataSourceStatus } from './components/data-sources'
import { ChatInterface } from './components/chat'

function App() {
  const [count, setCount] = useState(0)
  const [isAnalysisRunning, setIsAnalysisRunning] = useState(false)

  return (
    <div className="prodscope-container">
      <header className="bg-primary text-primary-foreground p-4">
        <h1 className="text-2xl font-bold">ProdScope - 产品分析与推荐系统</h1>
        <p className="text-sm opacity-90">AI驱动的六层洞察分析演示</p>
      </header>
      
      <main className="three-column-layout">
        <aside className="workflow-panel">
          <AgentWorkflow 
            isRunning={isAnalysisRunning}
            onStartAnalysis={() => setIsAnalysisRunning(true)}
            onPauseAnalysis={() => setIsAnalysisRunning(false)}
            onResetAnalysis={() => {
              setIsAnalysisRunning(false)
              // 可以在这里添加重置逻辑
            }}
          />
        </aside>
        
        <section className="insights-panel">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">洞察结果</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground mb-4">分析结果和可视化图表将在这里展示</p>
              
              <div className="bg-secondary p-4 rounded-lg mb-6">
                <h3 className="font-medium mb-2">
                  {isAnalysisRunning ? '🔄 分析进行中...' : '✅ Agent工作流 & 图表配置成功!'}
                </h3>
                <p className="text-sm text-secondary-foreground mb-3">
                  {isAnalysisRunning 
                    ? '六层洞察分析正在运行，实时生成洞察结果和可视化图表'
                    : 'AgentWorkflow、Card、Button、Badge、Progress、Recharts组件已准备就绪'
                  }
                </p>
                
                <div className="flex gap-2">
                  <Button 
                    onClick={() => setCount(count + 1)}
                    size="sm"
                    variant={isAnalysisRunning ? "outline" : "default"}
                  >
                    交互测试: {count}
                  </Button>
                  <Button 
                    variant="outline" 
                    size="sm"
                    onClick={() => setCount(0)}
                  >
                    重置计数
                  </Button>
                  {isAnalysisRunning && (
                    <Badge variant="processing" className="ml-2">
                      分析运行中
                    </Badge>
                  )}
                </div>
              </div>

              {/* 图表展示区域 */}
              <div className="space-y-6">
                <Card>
                  <CardContent className="pt-6">
                    <TrendChart 
                      title="洞察1: 市场宏观趋势分析"
                      height={250}
                    />
                  </CardContent>
                </Card>

                <Card>
                  <CardContent className="pt-6">
                    <BarChartComponent 
                      title="洞察2: 产品满意度分析" 
                      height={250}
                    />
                  </CardContent>
                </Card>
              </div>
            </CardContent>
          </Card>
        </section>
        
        <aside className="interaction-panel">
          <div className="space-y-6">
            <DataSourceStatus 
              onDataSourceClick={(dataSource) => {
                console.log('Clicked data source:', dataSource.name)
                // 可以在这里添加数据源详情弹窗或其他交互
              }}
              onRefreshAll={() => {
                console.log('Refreshing all data sources...')
                // 可以在这里添加全局刷新逻辑
              }}
              autoRefresh={true}
            />
            
            <ChatInterface 
              onSendMessage={(message) => {
                console.log('Chat message sent:', message)
                // 可以在这里集成后端API调用
              }}
              isAnalysisRunning={isAnalysisRunning}
            />
          </div>
        </aside>
      </main>
      
      <footer className="bg-muted p-4 text-center">
        <p className="text-muted-foreground">
          ProdScope Frontend v1.0 - Agent工作流 & 数据源状态 & 智能对话完整集成 🎉
        </p>
        <p className="text-xs text-muted-foreground mt-1">
          访问地址: http://localhost:5173/ | 组件: AgentWorkflow + DataSourceStatus + ChatInterface + 图表可视化
        </p>
      </footer>
    </div>
  )
}

export default App
