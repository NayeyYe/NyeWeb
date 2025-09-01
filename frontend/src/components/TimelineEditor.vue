<template>
  <el-card class="timeline-card">
    <template #header>
      <div class="card-header">
        <span>我的历程</span>
        <el-button size="small" @click="switchDataSource">
          切换数据源: {{ dataSource }}
        </el-button>
      </div>
    </template>

    <div v-loading="loading" class="timeline-container">
      <!-- 调试信息显示 -->
      <div class="debug-info" style="margin-bottom: 20px;">
        <p>数据源: {{ dataSource }}</p>
        <p>数据数量: {{ timelineItems.length }}</p>
        <p>最后请求URL: {{ lastRequestUrl }}</p>
        <p>加载状态: {{ loading }}</p>
        <p>错误信息: {{ error || '无' }}</p>
        <el-button type="primary" @click="forceRefresh">强制刷新</el-button>
        <el-button type="warning" @click="resetToLocalData">重置为本地数据</el-button>
        <details v-if="timelineItems.length > 0">
          <summary>当前显示数据</summary>
          <pre>{{ JSON.stringify(timelineItems, null, 2) }}</pre>
        </details>
        <details v-if="lastResponse">
          <summary>上次API响应</summary>
          <pre>{{ JSON.stringify(lastResponse, null, 2) }}</pre>
        </details>
      </div>

      <!-- 主要的时间线显示 -->
      <el-timeline v-if="!loading && timelineItems.length > 0">
        <el-timeline-item
          v-for="item in timelineItems"
          :key="'item-' + item.id"
          :timestamp="formatTimestamp(item.timestamp)"
          placement="top"
        >
          <div class="timeline-item-content">
            <el-tooltip
              :disabled="item.content.length <= 50"
              effect="dark"
              :content="item.content"
              placement="top"
            >
              <p class="timeline-content">
                {{ item.content.length > 50 ? item.content.slice(0, 50) + '...' : item.content }}
              </p>
            </el-tooltip>
          </div>
        </el-timeline-item>
      </el-timeline>

      <el-empty v-else-if="!loading && timelineItems.length === 0" description="暂无历程数据">
        <el-button type="primary" @click="forceRefresh">重新加载</el-button>
      </el-empty>
    </div>

    <div v-if="error" class="error-message">{{ error }}</div>
  </el-card>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const loading = ref(false)
const timelineItems = ref([])
const error = ref('')
const dataSource = ref('未知')
const lastRequestUrl = ref('')
const lastResponse = ref(null)
const currentApiSource = ref('timeline') // 'timeline' 或 'timeline/database'

// 直接从数据库获取的数据 - 确保这些数据能显示
const timelineData = [
  {
    "id": 6,
    "timestamp": "2025-10-10T00:00:00",
    "content": "优化了整体UI，统一了卡片圆角和布局对齐。"
  },
  {
    "id": 5,
    "timestamp": "2025-10-05T00:00:00",
    "content": "将数据源切换为JSON文件，为后续连接数据库做准备。"
  },
  {
    "id": 4,
    "timestamp": "2025-09-22T00:00:00",
    "content": "引入了KaTeX来支持数学公式的渲染。"
  },
  {
    "id": 3,
    "timestamp": "2025-09-15T00:00:00",
    "content": "添加了知识文章模块，并实现了Markdown文件的动态渲染。"
  },
  {
    "id": 2,
    "timestamp": "2025-09-01T00:00:00",
    "content": "完成了初步的页面布局和组件化。"
  },
  {
    "id": 1,
    "timestamp": "2025-08-25T00:00:00",
    "content": "网站开始搭建"
  }
]

// 确保API_BASE_URL没有尾部斜杠
const API_BASE_URL = 'http://localhost:8080/api'.replace(/\/$/, '')

// 格式化时间戳显示
const formatTimestamp = (timestamp) => {
  try {
    if (!timestamp) return '未知时间'

    const date = new Date(timestamp)
    if (isNaN(date.getTime())) {
      console.error('无效的时间戳:', timestamp)
      return '无效时间'
    }
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    })
  } catch (e) {
    console.error('时间戳格式化错误:', e)
    return '时间格式错误'
  }
}

// 切换数据源
const switchDataSource = () => {
  if (currentApiSource.value === 'timeline') {
    currentApiSource.value = 'timeline/database'
    ElMessage.info('切换到数据库API格式')
  } else {
    currentApiSource.value = 'timeline'
    ElMessage.info('切换到标准API格式')
  }
  fetchTimelineData()
}

// 强制刷新数据
const forceRefresh = () => {
  fetchTimelineData()
}

// 重置为本地数据
const resetToLocalData = () => {
  timelineItems.value = [...timelineData]
  dataSource.value = '本地数据(手动重置)'
  ElMessage.success('已重置为本地数据')
}

// 解析API响应数据
const parseApiResponse = (response) => {
  if (!response || !response.data) {
    return null
  }

  lastResponse.value = response.data

  // 数据库API格式 (包含 status, data, total)
  if (typeof response.data === 'object' && response.data.status === 'success' && Array.isArray(response.data.data)) {
    return response.data.data
  }

  // 标准API格式 (直接返回数组)
  if (Array.isArray(response.data)) {
    return response.data
  }

  return null
}

// 获取时间线数据 - 修正后的逻辑
const fetchTimelineData = async () => {
  loading.value = true
  error.value = ''

  console.log('=== 开始获取时间线数据 ===')

  // 构建请求URL
  const requestUrl = `${API_BASE_URL}/${currentApiSource.value}`
  lastRequestUrl.value = requestUrl
  console.log('请求URL:', requestUrl)

  try {
    const response = await axios.get(requestUrl, {
      timeout: 10000,
      headers: {
        'Accept': 'application/json',
        'Cache-Control': 'no-cache'
      }
    })

    console.log('API响应状态:', response.status)
    console.log('API响应数据类型:', typeof response.data)
    if (Array.isArray(response.data)) {
      console.log('API响应数据长度:', response.data.length)
    } else if (response.data && Array.isArray(response.data.data)) {
      console.log('API响应数据长度:', response.data.data.length)
    }

    // 解析响应数据
    const parsedData = parseApiResponse(response)

    if (parsedData && parsedData.length > 0) {
      // 确保每个项目都有id、timestamp和content
      const validData = parsedData.filter(item => item && item.id && item.content)

      if (validData.length > 0) {
        timelineItems.value = validData
        dataSource.value = currentApiSource.value === 'timeline' ? 'API' : '数据库API'
        console.log(`成功解析 ${validData.length} 条有效数据`)
        ElMessage.success(`成功获取 ${validData.length} 条时间线数据`)
      } else {
        console.log('API返回的数据缺少必要属性')
        error.value = 'API数据缺少必要属性'
        useFallbackData('数据验证失败')
      }
    } else {
      console.log('未能从API响应中提取有效数据')
      error.value = '未能从API响应中提取有效数据'
      useFallbackData('数据格式错误')
    }

  } catch (apiError) {
    console.error('API请求失败:', apiError)
    error.value = `API请求失败: ${apiError.message}`
    useFallbackData('API失败')
  } finally {
    loading.value = false
    console.log('=== 数据获取完成 ===')
    console.log('最终数据源:', dataSource.value)
    console.log('最终数据数量:', timelineItems.value.length)
  }
}

// 使用本地备用数据
const useFallbackData = (reason) => {
  timelineItems.value = [...timelineData]
  dataSource.value = `本地数据(${reason})`
  console.log(`使用本地数据，原因: ${reason}`)
  ElMessage.warning(`使用本地数据 (${reason})`)
}

// 组件挂载时获取数据
onMounted(() => {
  console.log('=== TimelineEditor组件已挂载 ===')

  // 优先使用标准API
  currentApiSource.value = 'timeline'
  fetchTimelineData()
})
</script>

<style scoped>
.timeline-card {
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 18px;
  font-weight: bold;
}

.timeline-container {
  min-height: 200px;
}

.timeline-item-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.timeline-content {
  margin: 0;
  color: #606266;
  line-height: 1.5;
  flex: 1;
}

.error-message {
  color: #f56c6c;
  padding: 10px;
  margin-top: 10px;
  font-size: 14px;
  background-color: #fef0f0;
  border-radius: 4px;
}

.debug-info {
  margin-top: 10px;
  padding: 10px;
  background-color: #f5f5f5;
  border-radius: 4px;
  font-size: 12px;
  color: #666;
  border: 1px solid #ddd;
}

.debug-info pre {
  font-size: 10px;
  max-height: 200px;
  overflow-y: auto;
  background: white;
  padding: 5px;
  border-radius: 3px;
}

@media (max-width: 768px) {
  .timeline-item-content {
    flex-direction: column;
    gap: 10px;
  }
}
</style>
