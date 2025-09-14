<template>
  <div class="tool-management">
    <!-- 操作栏 -->
    <div class="action-bar">
      <div class="action-buttons">
        <el-button type="primary" @click="showCreateDialog = true">新建工具</el-button>
        <el-button @click="refreshTools" :icon="Refresh" circle />
      </div>
    </div>

    <!-- 筛选区域 -->
    <div class="filter-section">
      <el-row :gutter="20">
        <el-col :span="24">
          <el-card class="filter-card" shadow="never">
            <template #header>
              <div class="filter-header">
                <span>筛选条件</span>
                <el-button link @click="resetAllFilters" class="reset-link-btn">重置</el-button>
              </div>
            </template>
            <div class="filter-controls">
              <!-- 标签筛选独立一行 -->
              <div class="filter-row tag-row">
                <div class="filter-item">
                  <label>标签筛选：</label>
                  <el-select
                    v-model="filterForm.tags"
                    multiple
                    filterable
                    allow-create
                    placeholder="选择或输入标签（最多3个）"
                    style="width: 350px"
                    size="default"
                    :multiple-limit="3"
                  >
                    <el-option
                      v-for="tag in allTags"
                      :key="tag"
                      :label="tag"
                      :value="tag"
                    />
                  </el-select>
                </div>
              </div>
              <!-- 其他筛选条件 -->
              <div class="filter-row">
                <div class="filter-item">
                  <label>标题搜索：</label>
                  <el-input
                    v-model="filterForm.title"
                    placeholder="输入标题关键字"
                    style="width: 250px"
                    clearable
                  />
                </div>
                <div class="filter-item">
                  <label>状态筛选：</label>
                  <el-select v-model="filterForm.status" style="width: 140px" placeholder="选择状态">
                    <el-option label="全部" value="" />
                    <el-option label="已发布" value="published" />
                    <el-option label="草稿" value="draft" />
                    <el-option label="已回收" value="recycled" />
                  </el-select>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 工具列表 -->
    <div class="tool-list">
      <el-card shadow="never">
        <template #header>
          <div class="list-header">
            <span>工具列表</span>
            <span class="tool-count">共 {{ filteredTools.length }} 个工具</span>
          </div>
        </template>
        <el-table
          :data="filteredTools"
          stripe
          class="tool-table"
          empty-text="暂无工具数据"
          :header-cell-style="{ background: '#fafafa', color: '#333', fontWeight: '600' }"
        >
          <el-table-column prop="title" label="工具标题" min-width="200" show-overflow-tooltip>
            <template #default="scope">
              <div class="tool-title">{{ scope.row.title }}</div>
            </template>
          </el-table-column>
          <el-table-column prop="url" label="工具链接" min-width="250" show-overflow-tooltip>
            <template #default="scope">
              <el-link :href="scope.row.url" target="_blank" type="primary" class="tool-url">
                {{ scope.row.url }}
              </el-link>
            </template>
          </el-table-column>
          <el-table-column prop="tags" label="标签" min-width="150" show-overflow-tooltip>
            <template #default="scope">
              <div v-if="scope.row.tags && scope.row.tags.length > 0" class="tool-tags">
                <el-tag
                  v-for="tag in scope.row.tags.slice(0, 3)"
                  :key="tag"
                  size="small"
                  type="info"
                  class="tag-item"
                >
                  {{ tag }}
                </el-tag>
                <span v-if="scope.row.tags.length > 3" class="more-tags">+{{ scope.row.tags.length - 3 }}</span>
              </div>
              <span v-else class="no-tags">暂无标签</span>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" min-width="120" align="center">
            <template #default="scope">
              <el-select
                :model-value="scope.row.status"
                @change="(value) => updateToolStatus(scope.row, value)"
                size="small"
                style="width: 100px"
              >
                <el-option label="草稿" value="draft" />
                <el-option label="已发布" value="published" />
                <el-option label="已回收" value="recycled" />
              </el-select>
            </template>
          </el-table-column>
          <el-table-column label="操作" min-width="160" align="center">
            <template #default="scope">
              <div class="action-buttons-table">
                <el-button size="small" type="primary" @click="handleEditTool(scope.row)">编辑</el-button>
                <el-button 
                  v-if="scope.row.status !== 'recycled'"
                  size="small" 
                  type="warning" 
                  @click="quickUpdateStatus(scope.row, 'recycled')"
                >
                  回收
                </el-button>
                <el-button 
                  v-if="scope.row.status === 'recycled'"
                  size="small" 
                  type="success" 
                  @click="quickUpdateStatus(scope.row, 'published')"
                >
                  恢复
                </el-button>
                <el-button size="small" type="danger" @click="deleteTool(scope.row)">删除</el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>

    <!-- 新建工具对话框 -->
    <el-dialog
      v-model="showCreateDialog"
      title="新建工具"
      width="600px"
      :before-close="handleCloseDialog"
    >
      <el-form
        ref="createFormRef"
        :model="createForm"
        :rules="createRules"
        label-width="100px"
      >
        <el-form-item label="工具标题" prop="title">
          <el-input
            v-model="createForm.title"
            placeholder="请输入工具标题"
            clearable
          />
        </el-form-item>
        <el-form-item label="工具链接" prop="url">
          <el-input
            v-model="createForm.url"
            placeholder="请输入完整的URL地址，如：https://example.com"
            clearable
          />
        </el-form-item>
        <el-form-item label="工具标签">
          <el-select
            v-model="createForm.tags"
            multiple
            filterable
            allow-create
            placeholder="选择或创建标签"
            style="width: 100%"
          >
            <el-option
              v-for="tag in allTags"
              :key="tag"
              :label="tag"
              :value="tag"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="handleCloseDialog">取消</el-button>
          <el-button type="primary" @click="handleCreateTool" :loading="creating">
            创建工具
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import {computed, onMounted, reactive, ref} from 'vue'
import {ElMessage, ElMessageBox} from 'element-plus'
import {Refresh} from '@element-plus/icons-vue'
import axios from 'axios'

const tools = ref([])
const allTags = ref([])
const showCreateDialog = ref(false)
const creating = ref(false)
const createFormRef = ref(null)

const filterForm = reactive({
  tags: [],
  title: '',
  status: ''
})

const createForm = reactive({
  title: '',
  url: '',
  tags: []
})

const createRules = {
  title: [
    { required: true, message: '请输入工具标题', trigger: 'blur' },
    { min: 1, max: 255, message: '标题长度应在1-255个字符之间', trigger: 'blur' }
  ],
  url: [
    { required: true, message: '请输入工具链接', trigger: 'blur' },
    { 
      pattern: /^https?:\/\/.+/,
      message: '请输入有效的URL地址（必须以http://或https://开头）',
      trigger: 'blur'
    }
  ]
}

// 获取工具列表（管理员接口，包含所有状态）
const fetchTools = async () => {
  try {
    const res = await axios.get('/api/admin/tools')
    tools.value = res.data
  } catch (error) {
    console.error('获取工具列表失败:', error)
    ElMessage.error('获取工具列表失败')
  }
}

// 获取标签
const fetchTags = async () => {
  try {
    const res = await axios.get('/api/tool-tags')
    allTags.value = res.data.tags || []
  } catch (error) {
    console.error('获取工具标签失败:', error)
  }
}

// 工具筛选
const filteredTools = computed(() => {
  let arr = tools.value
  if (filterForm.tags && filterForm.tags.length) {
    arr = arr.filter(t => t.tags && filterForm.tags.every(tag => t.tags.includes(tag)))
  }
  if (filterForm.title) {
    arr = arr.filter(t => t.title && t.title.includes(filterForm.title))
  }
  if (filterForm.status) {
    arr = arr.filter(t => t.status === filterForm.status)
  }
  return arr
})

// 筛选操作
const resetAllFilters = () => {
  filterForm.tags = []
  filterForm.title = ''
  filterForm.status = ''
}

// 工具操作
const handleEditTool = (tool) => {
  ElMessage.info(`编辑工具 "${tool.title}" 功能开发中，敬请期待！`)
}

const deleteTool = async (tool) => {
  try {
    await ElMessageBox.confirm('确定要删除该工具吗？', '提示', { type: 'warning' })
    await axios.delete(`/api/tools/${tool.id}`)
    ElMessage.success('工具删除成功')
    refreshTools()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除工具失败:', error)
      ElMessage.error('删除工具失败')
    }
  }
}

const refreshTools = async () => {
  await fetchTools()
  await fetchTags()
}

// 更新工具状态
const updateToolStatus = async (tool, newStatus) => {
  if (tool.status === newStatus) return
  
  try {
    await axios.patch(`/api/tools/${tool.id}/status`, { status: newStatus })
    
    // 更新本地数据
    tool.status = newStatus
    
    const statusText = getStatusText(newStatus)
    ElMessage.success(`工具状态已更新为：${statusText}`)
  } catch (error) {
    console.error('更新工具状态失败:', error)
    ElMessage.error('更新工具状态失败')
    // 刷新数据以恢复原状态
    refreshTools()
  }
}

// 快速更新状态（用于操作按钮）
const quickUpdateStatus = async (tool, newStatus) => {
  const actionText = newStatus === 'recycled' ? '回收' : '恢复'
  
  try {
    await ElMessageBox.confirm(`确定要${actionText}该工具吗？`, '提示', { type: 'warning' })
    await updateToolStatus(tool, newStatus)
  } catch (error) {
    if (error !== 'cancel') {
      console.error(`${actionText}工具失败:`, error)
    }
  }
}

// 创建工具相关
const handleCreateTool = async () => {
  if (!createFormRef.value) return
  
  try {
    await createFormRef.value.validate()
    creating.value = true
    
    await axios.post('/api/tools', createForm)
    
    ElMessage.success('工具创建成功')
    showCreateDialog.value = false
    resetCreateForm()
    refreshTools()
  } catch (error) {
    if (error.errors) {
      // 表单验证错误
      return
    }
    console.error('创建工具失败:', error)
    ElMessage.error('创建工具失败')
  } finally {
    creating.value = false
  }
}

const handleCloseDialog = () => {
  showCreateDialog.value = false
  resetCreateForm()
}

const resetCreateForm = () => {
  if (createFormRef.value) {
    createFormRef.value.resetFields()
  }
  Object.assign(createForm, {
    title: '',
    url: '',
    tags: []
  })
}

// 状态相关方法
const getStatusText = (status) => {
  switch (status) {
    case 'published': return '已发布'
    case 'draft': return '草稿'
    case 'recycled': return '已回收'
    default: return '未知'
  }
}

onMounted(() => {
  refreshTools()
})
</script>

<style scoped>
.tool-management {
  padding: 20px;
  background: #f8f9fa;
  min-height: 100vh;
}

.action-bar {
  margin-bottom: 20px;
}

.action-buttons {
  display: flex;
  gap: 12px;
}

.filter-section {
  margin-bottom: 20px;
}

.filter-card {
  border-radius: 12px;
  border: 1px solid #e1e8ed;
}

.filter-controls {
  padding: 10px 0;
}

.tag-row {
  margin-bottom: 20px;
}

.filter-row {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 16px;
}

.filter-row:last-child {
  margin-bottom: 0;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-item label {
  color: #666;
  font-size: 14px;
  white-space: nowrap;
  min-width: 80px;
}

.tool-list .filter-card {
  border: 1px solid #e1e8ed;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  color: #333;
}

.tool-count {
  color: #666;
  font-size: 14px;
  font-weight: normal;
}

.tool-table {
  border-radius: 8px;
  overflow: hidden;
}

.tool-title {
  font-weight: 500;
  color: #333;
}

.tool-url {
  font-family: 'Monaco', 'Consolas', monospace;
  font-size: 13px;
}

.tool-tags {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 4px;
}

.tag-item {
  margin: 0;
}

.more-tags {
  color: #999;
  font-size: 12px;
  margin-left: 4px;
}

.no-tags {
  color: #999;
  font-style: italic;
}

.action-buttons-table {
  display: flex;
  gap: 6px;
  justify-content: center;
  flex-wrap: wrap;
}

.action-buttons-table .el-button {
  margin: 2px 0;
}

.el-button {
  border-radius: 6px;
  font-weight: 500;
}

.el-button--primary {
  background: #409eff;
  border-color: #409eff;
}

.el-button--danger {
  background: #f56c6c;
  border-color: #f56c6c;
}

.reset-link-btn {
  color: #666 !important;
  font-weight: normal !important;
}

.reset-link-btn:hover {
  color: #409eff !important;
  background: transparent !important;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

:deep(.el-card__header) {
  padding: 16px 20px;
  background: #fafafa;
  border-bottom: 1px solid #ebeef5;
}

:deep(.el-card__body) {
  padding: 20px;
}

:deep(.el-table th) {
  background: #fafafa !important;
}

/* 状态下拉框样式 */
:deep(.el-select .el-input__inner) {
  text-align: center;
  padding: 0 8px;
}

:deep(.el-select--small .el-input__inner) {
  height: 28px;
  line-height: 28px;
}

/* 对话框样式 */
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>