import React, { useState, useEffect } from 'react'
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card'
import { Badge } from '../ui/Badge'
import { Button } from '../ui/Button'
import { Progress } from '../ui/Progress'

interface DataSource {
  id: string
  name: string
  type: 'database' | 'api' | 'search' | 'trends'
  status: 'online' | 'connecting' | 'offline' | 'error'
  description: string
  recordCount?: number
  lastSync?: string
  responseTime?: number
  endpoint?: string
  capabilities?: string[]
}

const INITIAL_DATA_SOURCES: DataSource[] = [
  {
    id: 'mindsdb',
    name: 'MindsDB',
    type: 'database',
    status: 'online',
    description: '产品数据主库',
    recordCount: 37891,
    lastSync: '2分钟前',
    responseTime: 45,
    endpoint: 'prodscope_db',
    capabilities: ['SQL查询', '实时聚合', '情感分析']
  },
  {
    id: 'vertex-ai',
    name: 'Vertex AI',
    type: 'search',
    status: 'online',
    description: '搜索增强服务',
    lastSync: '30秒前',
    responseTime: 320,
    endpoint: 'Global Endpoint',
    capabilities: ['网络搜索', '引用生成', '多语言支持']
  },
  {
    id: 'pytrends',
    name: 'PyTrends',
    type: 'trends',
    status: 'connecting',
    description: '趋势数据源',
    lastSync: '5分钟前',
    responseTime: 8500,
    endpoint: 'Google Trends API',
    capabilities: ['趋势分析', '地域数据', '相关查询']
  },
  {
    id: 'walmart-api',
    name: 'Walmart API',
    type: 'api',
    status: 'offline',
    description: '沃尔玛产品API',
    lastSync: '1小时前',
    responseTime: 0,
    endpoint: 'partner.walmart.com',
    capabilities: ['产品信息', '价格监控', '库存状态']
  }
]

interface DataSourceStatusProps {
  onDataSourceClick?: (dataSource: DataSource) => void
  onRefreshAll?: () => void
  autoRefresh?: boolean
}

export const DataSourceStatus: React.FC<DataSourceStatusProps> = ({
  onDataSourceClick,
  onRefreshAll,
  autoRefresh = true
}) => {
  const [dataSources, setDataSources] = useState<DataSource[]>(INITIAL_DATA_SOURCES)
  const [lastRefresh, setLastRefresh] = useState<Date>(new Date())
  const [refreshing, setRefreshing] = useState(false)

  // 模拟数据源状态更新
  useEffect(() => {
    if (!autoRefresh) return

    const interval = setInterval(() => {
      setDataSources(prev => prev.map(source => {
        // 模拟PyTrends连接状态变化
        if (source.id === 'pytrends' && source.status === 'connecting') {
          const shouldConnect = Math.random() > 0.7
          return {
            ...source,
            status: shouldConnect ? 'online' : 'connecting',
            responseTime: shouldConnect ? 2100 : source.responseTime,
            lastSync: shouldConnect ? '刚刚' : source.lastSync
          }
        }
        
        // 模拟其他数据源的响应时间波动
        if (source.status === 'online') {
          const variation = Math.random() * 0.3 - 0.15 // ±15%
          return {
            ...source,
            responseTime: Math.round((source.responseTime || 100) * (1 + variation))
          }
        }
        
        return source
      }))
      setLastRefresh(new Date())
    }, 3000)

    return () => clearInterval(interval)
  }, [autoRefresh])

  const handleRefreshAll = async () => {
    setRefreshing(true)
    // 模拟刷新延迟
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    setDataSources(prev => prev.map(source => ({
      ...source,
      lastSync: '刚刚',
      status: source.id === 'walmart-api' ? 'offline' : 'online'
    })))
    
    setLastRefresh(new Date())
    setRefreshing(false)
    onRefreshAll?.()
  }

  const getStatusColor = (status: DataSource['status']) => {
    switch (status) {
      case 'online': return 'success'
      case 'connecting': return 'warning'
      case 'offline': return 'outline'
      case 'error': return 'destructive'
      default: return 'outline'
    }
  }

  const getStatusText = (status: DataSource['status']) => {
    switch (status) {
      case 'online': return '在线'
      case 'connecting': return '连接中'
      case 'offline': return '离线'
      case 'error': return '错误'
      default: return '未知'
    }
  }

  const getTypeIcon = (type: DataSource['type']) => {
    switch (type) {
      case 'database': return '🗄️'
      case 'api': return '🔌'
      case 'search': return '🔍'
      case 'trends': return '📈'
      default: return '📊'
    }
  }

  const getResponseTimeStatus = (responseTime?: number) => {
    if (!responseTime) return { color: 'text-muted-foreground', label: '-' }
    if (responseTime < 100) return { color: 'text-green-600', label: '优秀' }
    if (responseTime < 500) return { color: 'text-blue-600', label: '良好' }
    if (responseTime < 2000) return { color: 'text-yellow-600', label: '一般' }
    return { color: 'text-red-600', label: '较慢' }
  }

  const totalOnline = dataSources.filter(ds => ds.status === 'online').length
  const healthPercentage = (totalOnline / dataSources.length) * 100

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg flex items-center justify-between">
          <span>数据源 & 服务状态</span>
          <Button 
            size="sm" 
            variant="outline" 
            onClick={handleRefreshAll}
            disabled={refreshing}
            className="text-xs"
          >
            {refreshing ? '刷新中...' : '刷新'}
          </Button>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="mb-4">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium">系统健康度</span>
            <span className="text-sm text-muted-foreground">{totalOnline}/{dataSources.length} 在线</span>
          </div>
          <Progress value={healthPercentage} showLabel={false} />
          <div className="flex justify-between items-center mt-1 text-xs text-muted-foreground">
            <span>最后更新: {lastRefresh.toLocaleTimeString()}</span>
            <span className={healthPercentage >= 75 ? 'text-green-600' : 'text-yellow-600'}>
              {healthPercentage >= 75 ? '健康' : '需注意'}
            </span>
          </div>
        </div>

        <div className="space-y-3">
          {dataSources.map((source) => {
            const responseStatus = getResponseTimeStatus(source.responseTime)
            
            return (
              <div 
                key={source.id} 
                className="border border-border rounded-lg p-3 hover:shadow-md transition-all cursor-pointer"
                onClick={() => onDataSourceClick?.(source)}
              >
                <div className="flex justify-between items-start mb-2">
                  <div className="flex items-center gap-2">
                    <span className="text-lg">{getTypeIcon(source.type)}</span>
                    <div>
                      <div className="font-medium text-sm">{source.name}</div>
                      <div className="text-xs text-muted-foreground">{source.description}</div>
                    </div>
                  </div>
                  <Badge variant={getStatusColor(source.status)} className="text-xs">
                    {getStatusText(source.status)}
                  </Badge>
                </div>

                <div className="grid grid-cols-2 gap-3 text-xs">
                  <div>
                    <span className="text-muted-foreground">端点: </span>
                    <span className="font-mono">{source.endpoint}</span>
                  </div>
                  <div>
                    <span className="text-muted-foreground">最后同步: </span>
                    <span>{source.lastSync}</span>
                  </div>
                  {source.recordCount && (
                    <div>
                      <span className="text-muted-foreground">记录数: </span>
                      <span className="font-semibold">{source.recordCount.toLocaleString()}</span>
                    </div>
                  )}
                  {source.responseTime !== undefined && (
                    <div>
                      <span className="text-muted-foreground">响应时间: </span>
                      <span className={responseStatus.color}>
                        {source.responseTime}ms ({responseStatus.label})
                      </span>
                    </div>
                  )}
                </div>

                {source.capabilities && (
                  <div className="mt-2">
                    <div className="flex flex-wrap gap-1">
                      {source.capabilities.map((capability, index) => (
                        <span 
                          key={index} 
                          className="px-2 py-1 bg-accent text-accent-foreground rounded text-xs"
                        >
                          {capability}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )
          })}
        </div>

        <div className="mt-4 p-3 bg-secondary rounded-lg text-xs">
          <div className="font-medium mb-1">连接状态说明</div>
          <div className="text-muted-foreground space-y-1">
            <div>• 🟢 在线: 正常响应，数据实时同步</div>
            <div>• 🟡 连接中: 正在建立连接或重连</div>
            <div>• ⚪ 离线: 服务不可用或维护中</div>
            <div>• 🔴 错误: 连接异常，需要检查配置</div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}