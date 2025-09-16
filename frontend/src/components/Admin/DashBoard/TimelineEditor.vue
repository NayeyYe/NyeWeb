<template>
  <div class="timeline-editor">
    <el-card class="editor-card" shadow="never">
      <template #header>
        <div class="header">
          <span>时间线编辑</span>
          <div class="header-actions">
            <el-button @click="refreshTimeline" :icon="Refresh" circle size="small" />
            <el-button @click="showAddDialog = true" type="primary" size="small">
              <el-icon><Plus /></el-icon>
              添加
            </el-button>
          </div>
        </div>
      </template>

      <div v-loading="loading" class="timeline-content">
        <div v-if="timelineList.length > 0" class="timeline-list">
          <div 
            v-for="item in timelineList" 
            :key="item.id" 
            class="timeline-item"
          >
            <div class="item-left">
              <span class="item-date">{{ formatDate(item.timestamp) }}</span>
            </div>
            <div class="item-right">
              <div class="item-content">{{ item.content }}</div>
              <div class="item-actions">
                <el-button 
                  @click="editItem(item)" 
                  type="primary" 
                  size="small" 
                  text
                >
                  编辑
                </el-button>
                <el-button 
                  @click="deleteItem(item)" 
                  type="danger" 
                  size="small" 
                  text
                >
                  删除
                </el-button>
              </div>
            </div>
          </div>
        </div>
        <el-empty v-else description="暂无时间线数据" :image-size="60" />
      </div>
    </el-card>

    <!-- 添加/编辑对话框 -->
    <el-dialog
      v-model="showAddDialog"
      :title="editingItem ? '编辑时间线' : '添加时间线'"
      width="500px"
      :before-close="handleDialogClose"
    >
      <el-form :model="formData" :rules="formRules" label-width="80px" ref="formRef">
        <el-form-item label="日期时间" prop="timestamp" required>
          <el-date-picker
            v-model="formData.timestamp"
            type="datetime"
            placeholder="选择日期时间"
            format="YYYY-MM-DD HH:mm:ss"
            value-format="YYYY-MM-DD HH:mm:ss"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="内容" prop="content" required>
          <el-input
            v-model="formData.content"
            type="textarea"
            :rows="4"
            placeholder="请输入时间线内容"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="handleDialogClose">取消</el-button>
          <el-button type="primary" @click="saveItem" :loading="saving">
            {{ editingItem ? '更新' : '添加' }}
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Refresh } from '@element-plus/icons-vue'
import axios from 'axios'

const loading = ref(false)
const saving = ref(false)
const showAddDialog = ref(false)
const editingItem = ref(null)
const timelineList = ref([])
const formRef = ref(null)

const formData = reactive({
  timestamp: '',
  content: ''
})

const formRules = {
  timestamp: [
    { required: true, message: '请选择日期时间', trigger: 'change' }
  ],
  content: [
    { required: true, message: '请输入内容', trigger: 'blur' },
    { min: 1, max: 500, message: '内容长度应在1-500个字符之间', trigger: 'blur' }
  ]
}

// 获取时间线数据
const fetchTimeline = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/timeline')
    timelineList.value = response.data || []
    timelineList.value.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
  } catch (error) {
    console.error('获取时间线数据失败:', error)
    ElMessage.error('获取时间线数据失败')
  } finally {
    loading.value = false
  }
}

// 刷新数据
const refreshTimeline = () => {
  fetchTimeline()
}

// 格式化日期
const formatDate = (timestamp) => {
  try {
    return new Date(timestamp).toLocaleString('zh-CN')
  } catch (e) {
    return '时间格式错误'
  }
}

// 编辑项目
const editItem = (item) => {
  editingItem.value = item
  formData.timestamp = item.timestamp
  formData.content = item.content
  showAddDialog.value = true
}

// 删除项目
const deleteItem = async (item) => {
  try {
    await ElMessageBox.confirm('确定要删除这条时间线吗？', '提示', {
      type: 'warning'
    })
    
    await axios.delete(`/api/timeline/${item.id}`)
    ElMessage.success('删除成功')
    fetchTimeline()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

// 保存项目
const saveItem = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    saving.value = true
    
    if (editingItem.value) {
      // 更新
      await axios.put(`/api/timeline/${editingItem.value.id}`, formData)
      ElMessage.success('更新成功')
    } else {
      // 新增
      await axios.post('/api/timeline', formData)
      ElMessage.success('添加成功')
    }
    
    handleDialogClose()
    fetchTimeline()
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

// 关闭对话框
const handleDialogClose = () => {
  showAddDialog.value = false
  editingItem.value = null
  formData.timestamp = ''
  formData.content = ''
  if (formRef.value) {
    formRef.value.resetFields()
  }
}

onMounted(() => {
  fetchTimeline()
})
</script>

<style scoped>
.timeline-editor {
  height: 400px;
  display: flex;
  flex-direction: column;
}

.editor-card {
  height: 100%;
  display: flex;
  flex-direction: column;
  border-radius: 12px;
  border: 1px solid #e1e8ed;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.timeline-content {
  flex: 1;
  overflow-y: auto;
  padding: 0;
}

.timeline-list {
  display: flex;
  flex-direction: column;
}

.timeline-item {
  display: flex;
  padding: 12px 16px;
  border-bottom: 1px solid #f0f0f0;
  transition: background-color 0.2s ease;
}

.timeline-item:hover {
  background: #f8f9fa;
}

.timeline-item:last-child {
  border-bottom: none;
}

.item-left {
  width: 140px;
  flex-shrink: 0;
  padding-right: 16px;
}

.item-date {
  font-size: 12px;
  color: #666;
  font-family: 'Monaco', 'Consolas', monospace;
}

.item-right {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.item-content {
  color: #333;
  line-height: 1.5;
  font-size: 14px;
  flex: 1;
  padding-right: 12px;
}

.item-actions {
  display: flex;
  gap: 4px;
  flex-shrink: 0;
}

.dialog-footer {
  text-align: right;
}

/* 自定义滚动条 */
.timeline-content::-webkit-scrollbar {
  width: 6px;
}

.timeline-content::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.timeline-content::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.timeline-content::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

:deep(.el-card__body) {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  padding: 0;
}

:deep(.el-card__header) {
  padding: 16px 20px;
  background: #fafafa;
  border-bottom: 1px solid #ebeef5;
}
</style>
