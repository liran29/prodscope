import React from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

// Mock数据用于测试
const mockTrendData = [
  { month: '1月', walmart: 120, amazon: 110, market_avg: 115 },
  { month: '2月', walmart: 132, amazon: 125, market_avg: 128 },
  { month: '3月', walmart: 145, amazon: 140, market_avg: 142 },
  { month: '4月', walmart: 155, amazon: 138, market_avg: 146 },
  { month: '5月', walmart: 168, amazon: 155, market_avg: 161 },
  { month: '6月', walmart: 180, amazon: 172, market_avg: 176 },
]

interface TrendChartProps {
  data?: typeof mockTrendData
  title?: string
  height?: number
  showLegend?: boolean
}

export const TrendChart: React.FC<TrendChartProps> = ({
  data = mockTrendData,
  title = "产品排名趋势",
  height = 300,
  showLegend = true
}) => {
  return (
    <div className="chart-container">
      {title && (
        <h3 className="text-lg font-semibold mb-4 text-center">{title}</h3>
      )}
      
      <ResponsiveContainer width="100%" height={height}>
        <LineChart
          data={data}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
          <XAxis 
            dataKey="month" 
            stroke="hsl(var(--muted-foreground))"
            fontSize={12}
          />
          <YAxis 
            stroke="hsl(var(--muted-foreground))"
            fontSize={12}
          />
          <Tooltip 
            contentStyle={{
              backgroundColor: 'hsl(var(--card))',
              border: '1px solid hsl(var(--border))',
              borderRadius: '6px',
              color: 'hsl(var(--card-foreground))'
            }}
          />
          {showLegend && <Legend />}
          
          <Line 
            type="monotone" 
            dataKey="walmart" 
            stroke="hsl(var(--primary))" 
            strokeWidth={2}
            name="Walmart排名"
            dot={{ fill: 'hsl(var(--primary))', strokeWidth: 2, r: 4 }}
          />
          <Line 
            type="monotone" 
            dataKey="amazon" 
            stroke="hsl(var(--destructive))" 
            strokeWidth={2}
            name="Amazon排名"
            dot={{ fill: 'hsl(var(--destructive))', strokeWidth: 2, r: 4 }}
          />
          <Line 
            type="monotone" 
            dataKey="market_avg" 
            stroke="hsl(var(--muted-foreground))" 
            strokeWidth={2}
            strokeDasharray="5 5"
            name="市场平均"
            dot={{ fill: 'hsl(var(--muted-foreground))', strokeWidth: 2, r: 3 }}
          />
        </LineChart>
      </ResponsiveContainer>
      
      <div className="mt-2 text-xs text-muted-foreground text-center">
        数据来源: MindsDB walmart_ranking_history
      </div>
    </div>
  )
}