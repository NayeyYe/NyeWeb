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
  </el-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const loading = ref(false)
const timelineItems = ref([])

// API基础URL
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
  try {
    const response = await axios.get(`${API_BASE_URL}/timeline`)
    timelineItems.value = response.data
  } catch (error) {
    console.error('获取时间线数据失败:', error)
    ElMessage.error('获取时间线数据失败')
  } finally {
    loading.value = false
  }
}

// 组件挂载时获取数据
onMounted(() => {
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

@media (max-width: 768px) {
  .timeline-item-content {
    flex-direction: column;
    gap: 10px;
  }
}
</style>
