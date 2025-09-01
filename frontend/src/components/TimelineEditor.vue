<template>
  <el-card class="timeline-card">
    <template #header>
      <div class="card-header">
        <span>我的历程</span>
      </div>
    </template>

    <div v-loading="loading" class="timeline-container">
      <el-timeline v-if="!loading && timelineItems.length > 0">
        <el-timeline-item
          v-for="item in timelineItems"
          :key="item.id"
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

      <el-empty v-else-if="!loading && timelineItems.length === 0" description="暂无历程数据" />
    </div>
    <div v-if="error" class="error-message">{{ error }}</div>
    <!-- 调试信息 -->
    <div class="debug-info">
      <p>数据源: {{ dataSource }}</p>
      <p>数据数量: {{ timelineItems.length }}</p>
    </div>
  </el-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const loading = ref(false)
const timelineItems = ref([])
const error = ref('')
const dataSource = ref('未知')

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

const API_BASE_URL = 'http://localhost:8080/api'

// 格式化时间戳显示
const formatTimestamp = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 获取时间线数据
const fetchTimelineData = async () => {
  loading.value = true
  error.value = ''

  console.log('TimelineEditor: 开始获取数据')

  try {
    console.log(`TimelineEditor: 尝试从API获取数据: ${API_BASE_URL}/timeline`)

    const response = await axios.get(`${API_BASE_URL}/timeline`, {
      timeout: 5000,
      headers: {
        'Accept': 'application/json'
      }
    })

    console.log('TimelineEditor: API响应状态:', response.status)
    console.log('TimelineEditor: API响应数据:', response.data)

    if (response.data && Array.isArray(response.data) && response.data.length > 0) {
      timelineItems.value = response.data
      dataSource.value = 'API'
      console.log(`TimelineEditor: 成功从API获取 ${response.data.length} 条数据`)
      ElMessage.success(`成功从API获取 ${response.data.length} 条时间线数据`)
    } else {
      console.log('TimelineEditor: API返回空数据，使用本地数据')
      timelineItems.value = timelineData
      dataSource.value = '本地数据(API空)'
      ElMessage.warning('API返回空数据，已切换到本地数据')
    }

  } catch (apiError) {
    console.error('TimelineEditor: API请求失败:', apiError)

    // API调用失败，使用本地数据
    timelineItems.value = timelineData
    dataSource.value = '本地数据(API失败)'

    console.log(`TimelineEditor: 使用本地数据，共 ${timelineData.length} 条记录`)

    if (apiError.response) {
      error.value = `API请求失败: ${apiError.response.status} ${apiError.response.statusText}`
      ElMessage.error(`API请求失败: ${apiError.response.status}`)
    } else if (apiError.request) {
      error.value = '无法连接到服务器'
      ElMessage.error('无法连接到服务器，使用本地数据')
    } else {
      error.value = `请求错误: ${apiError.message}`
      ElMessage.error('请求设置错误，使用本地数据')
    }
  } finally {
    loading.value = false
    console.log(`TimelineEditor: 最终数据数量: ${timelineItems.value.length}`)
  }
}

// 组件挂载时获取数据
onMounted(() => {
  console.log('TimelineEditor: 组件已挂载')
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
}

@media (max-width: 768px) {
  .timeline-item-content {
    flex-direction: column;
    gap: 10px;
  }
}
</style>
