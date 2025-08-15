export interface Insight {
  id: string
  title: string
  description: string
  llm: string
  status: 'pending' | 'processing' | 'completed' | 'error'
  dataSource: string
  dataCount: number
  chartData?: any[]
  type: 'trend' | 'comparison' | 'correlation' | 'heatmap'
}

export interface DataSource {
  name: string
  table: string
  count: number
  description: string
}

export interface LLMTask {
  llm: 'Gemini' | 'Claude' | 'Grok' | 'GPT-4o'
  task: string
  status: 'idle' | 'processing' | 'completed'
  progress: number
}

export interface ProductRecommendation {
  id: string
  title: string
  description: string
  rationale: string
  insights: string[]
  priority: 'high' | 'medium' | 'low'
}