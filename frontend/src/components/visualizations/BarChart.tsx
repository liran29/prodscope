import React from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

// Mock数据用于测试
const mockBarData = [
  { category: '圣诞球', positive: 85, negative: 15, total: 100 },
  { category: '灯串', positive: 78, negative: 22, total: 100 },
  { category: '花环', positive: 92, negative: 8, total: 100 },
  { category: '挂饰', positive: 74, negative: 26, total: 100 },
  { category: '圣诞树', positive: 68, negative: 32, total: 100 },
]

interface BarChartProps {
  data?: typeof mockBarData
  title?: string
  height?: number
  showLegend?: boolean
}

export const BarChartComponent: React.FC<BarChartProps> = ({
  data = mockBarData,
  title = "产品类别满意度分析",
  height = 300,
  showLegend = true
}) => {
  return (
    <div className="chart-container">
      {title && (
        <h3 className="text-lg font-semibold mb-4 text-center">{title}</h3>
      )}
      
      <ResponsiveContainer width="100%" height={height}>
        <BarChart
          data={data}
          margin={{
            top: 20,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
          <XAxis 
            dataKey="category" 
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
          
          <Bar 
            dataKey="positive" 
            stackId="a"
            fill="hsl(var(--primary))" 
            name="正面评价 (%)"
            radius={[0, 0, 0, 0]}
          />
          <Bar 
            dataKey="negative" 
            stackId="a"
            fill="hsl(var(--destructive))" 
            name="负面评价 (%)"
            radius={[4, 4, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
      
      <div className="mt-2 text-xs text-muted-foreground text-center">
        数据来源: MindsDB walmart_product_reviews (情感分析)
      </div>
    </div>
  )
}