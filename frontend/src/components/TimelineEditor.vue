<template>
  <el-card class="timeline-card">
    <template #header>
      <div class="card-header">
        <span>我的历程</span>
        <el-button class="button" type="primary" plain @click="dialogVisible = true">
          添加新条目
        </el-button>
      </div>
    </template>

    <el-dialog v-model="dialogVisible" title="添加新条目" width="500">
      <el-form :model="newItem" label-width="80px">
        <el-form-item label="日期">
          <el-date-picker
            v-model="newItem.timestamp"
            type="datetime"
            placeholder="选择日期和时间"
            value-format="YYYY-MM-DD HH:mm:ss"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="内容">
          <el-input v-model="newItem.content" type="textarea" placeholder="请输入内容" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="addItem" :loading="loading">确认</el-button>
        </span>
      </template>
    </el-dialog>

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
            <div class="timeline-actions">
              <el-button size="small" text @click="editItem(item)">编辑</el-button>
              <el-button size="small" text type="danger" @click="deleteItem(item.id)">删除</el-button>
            </div>
          </div>
        </el-timeline-item>
      </el-timeline>

      <el-empty v-else-if="!loading && timelineItems.length === 0" description="暂无历程数据" />
    </div>

    <!-- 编辑对话框 -->
    <el-dialog v-model="editDialogVisible" title="编辑条目" width="500">
      <el-form :model="editingItem" label-width="80px">
        <el-form-item label="日期">
          <el-date-picker
            v-model="editingItem.timestamp"
            type="datetime"
            placeholder="选择日期和时间"
            value-format="YYYY-MM-DD HH:mm:ss"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="内容">
          <el-input v-model="editingItem.content" type="textarea" placeholder="请输入内容" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="updateItem" :loading="loading">更新</el-button>
        </span>
      </template>
    </el-dialog>
  </el-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'

const dialogVisible = ref(false)
const editDialogVisible = ref(false)
const loading = ref(false)
const timelineItems = ref([])

const newItem = ref({
  timestamp: '',
  content: ''
})

const editingItem = ref({
  id: null,
  timestamp: '',
  content: ''
})

// API基础URL
const API_BASE_URL = 'http://localhost:5173/api'

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

// 添加新条目
const addItem = async () => {
  if (!newItem.value.timestamp || !newItem.value.content) {
    ElMessage.warning('请填写完整信息')
    return
  }

  loading.value = true
  try {
    const response = await axios.post(`${API_BASE_URL}/timeline`, newItem.value)
    timelineItems.value.unshift(response.data)

    // 重新排序
    timelineItems.value.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))

    ElMessage.success('添加成功')
    dialogVisible.value = false

    // 清空表单
    newItem.value = {
      timestamp: '',
      content: ''
    }
  } catch (error) {
    console.error('添加时间线条目失败:', error)
    ElMessage.error('添加失败')
  } finally {
    loading.value = false
  }
}

// 编辑条目
const editItem = (item) => {
  editingItem.value = {
    id: item.id,
    timestamp: item.timestamp,
    content: item.content
  }
  editDialogVisible.value = true
}

// 更新条目
const updateItem = async () => {
  if (!editingItem.value.timestamp || !editingItem.value.content) {
    ElMessage.warning('请填写完整信息')
    return
  }

  loading.value = true
  try {
    const response = await axios.put(
      `${API_BASE_URL}/timeline/${editingItem.value.id}`,
      {
        timestamp: editingItem.value.timestamp,
        content: editingItem.value.content
      }
    )

    // 更新本地数据
    const index = timelineItems.value.findIndex(item => item.id === editingItem.value.id)
    if (index !== -1) {
      timelineItems.value[index] = response.data
    }

    // 重新排序
    timelineItems.value.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))

    ElMessage.success('更新成功')
    editDialogVisible.value = false
  } catch (error) {
    console.error('更新时间线条目失败:', error)
    ElMessage.error('更新失败')
  } finally {
    loading.value = false
  }
}

// 删除条目
const deleteItem = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除这个条目吗？', '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    loading.value = true
    await axios.delete(`${API_BASE_URL}/timeline/${id}`)

    // 从本地数据中移除
    timelineItems.value = timelineItems.value.filter(item => item.id !== id)

    ElMessage.success('删除成功')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除时间线条目失败:', error)
      ElMessage.error('删除失败')
    }
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

.timeline-actions {
  margin-left: 10px;
  flex-shrink: 0;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

@media (max-width: 768px) {
  .timeline-item-content {
    flex-direction: column;
    gap: 10px;
  }

  .timeline-actions {
    margin-left: 0;
    align-self: flex-start;
  }
}
</style>
