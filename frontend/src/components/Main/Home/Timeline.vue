<template>
  <el-card class="timeline-card">
    <template #header>
      <div class="card-header">
        <span>我的历程</span>
      </div>
    </template>

    <div v-loading="loading" class="timeline-container">
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
                :content="item.content"
                :disabled="item.content.length <= 50"
                effect="dark"
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
      </el-empty>
    </div>
  </el-card>
</template>

<script setup>
import {onMounted, ref} from 'vue'
import axios from 'axios'

const loading = ref(false)
const timelineItems = ref([])

const API_BASE_URL = '/api'

const formatTimestamp = (timestamp) => {
  try {
    if (!timestamp) return '未知时间'
    const date = new Date(timestamp)
    if (isNaN(date.getTime())) {
      return '无效时间'
    }
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    })
  } catch (e) {
    return '时间格式错误'
  }
}

const fetchTimelineData = async () => {
  loading.value = true
  try {
    const response = await axios.get(`${API_BASE_URL}/timeline`, {
      timeout: 10000,
      headers: {
        'Accept': 'application/json'
      }
    })

    if (response.data && Array.isArray(response.data)) {
      timelineItems.value = response.data
    } else if (response.data && response.data.data && Array.isArray(response.data.data)) {
      timelineItems.value = response.data.data
    }
  } catch (error) {
    console.error('获取时间线数据失败:', error)
  } finally {
    loading.value = false
  }
}

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

.error-message {
  color: #f56c6c;
  padding: 10px;
  margin-top: 10px;
  font-size: 14px;
  background-color: #fef0f0;
  border-radius: 4px;
}
</style>
