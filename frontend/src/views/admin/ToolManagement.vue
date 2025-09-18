<template>
  <div class="tool-management">
    <!-- 操作栏 -->
    <div class="action-bar">
      <div class="action-buttons">
        <el-button type="primary" @click="showCreateDialog = true">新建工具</el-button>
        <el-button :icon="Refresh" circle @click="refreshTools"/>
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
                <el-button class="reset-link-btn" link @click="resetAllFilters">重置</el-button>
              </div>
            </template>
            <div class="filter-controls">
              <!-- 标签筛选独立一行 -->
              <div class="filter-row tag-row">
                <div class="filter-item">
                  <label>标签筛选：</label>
                  <el-select
                      v-model="filterForm.tags"
                      :multiple-limit="3"
                      allow-create
                      filterable
                      multiple
                      placeholder="选择或输入标签（最多3个）"
                      size="default"
                      style="width: 350px"
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
                      clearable
                      placeholder="输入标题关键字"
                      style="width: 250px"
                  />
                </div>
                <div class="filter-item">
                  <label>状态筛选：</label>
                  <el-select v-model="filterForm.status" placeholder="选择状态" style="width: 140px">
                    <el-option label="全部" value=""/>
                    <el-option label="已发布" value="published"/>
                    <el-option label="草稿" value="draft"/>
                    <el-option label="已回收" value="recycled"/>
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
            :header-cell-style="{ background: '#fafafa', color: '#333', fontWeight: '600' }"
            class="tool-table"
            empty-text="暂无工具数据"
            stripe
        >
          <el-table-column label="工具标题" min-width="200" prop="title" show-overflow-tooltip>
            <template #default="scope">
              <div class="tool-title">{{ scope.row.title }}</div>
            </template>
          </el-table-column>
          <el-table-column label="工具链接" min-width="250" prop="url" show-overflow-tooltip>
            <template #default="scope">
              <el-link :href="scope.row.url" class="tool-url" target="_blank" type="primary">
                {{ scope.row.url }}
              </el-link>
            </template>
          </el-table-column>
          <el-table-column label="标签" min-width="150" prop="tags" show-overflow-tooltip>
            <template #default="scope">
              <div v-if="scope.row.tags && scope.row.tags.length > 0" class="tool-tags">
                <el-tag
                    v-for="tag in scope.row.tags.slice(0, 3)"
                    :key="tag"
                    class="tag-item"
                    size="small"
                    type="info"
                >
                  {{ tag }}
                </el-tag>
                <span v-if="scope.row.tags.length > 3" class="more-tags">+{{ scope.row.tags.length - 3 }}</span>
              </div>
              <span v-else class="no-tags">暂无标签</span>
            </template>
          </el-table-column>
          <el-table-column align="center" label="状态" min-width="120" prop="status">
            <template #default="scope">
              <el-select
                  :model-value="scope.row.status"
                  size="small"
                  style="width: 100px"
                  @change="(value) => updateToolStatus(scope.row, value)"
              >
                <el-option label="草稿" value="draft"/>
                <el-option label="已发布" value="published"/>
                <el-option label="已回收" value="recycled"/>
              </el-select>
            </template>
          </el-table-column>
          <el-table-column align="center" label="操作" min-width="160">
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
        :before-close="handleCloseCreateDialog"
        title="新建工具"
        width="600px"
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
              clearable
              placeholder="请输入工具标题"
          />
        </el-form-item>
        <el-form-item label="工具链接" prop="url">
          <el-input
              v-model="createForm.url"
              clearable
              placeholder="请输入完整的URL地址，如：https://example.com"
          />
        </el-form-item>
        <el-form-item label="工具描述">
          <el-input
              v-model="createForm.description"
              :rows="3"
              clearable
              maxlength="500"
              placeholder="请输入工具描述（可选）"
              show-word-limit
              type="textarea"
          />
        </el-form-item>
        <el-form-item label="工具标签">
          <div class="tag-input-container">
            <el-select
                v-model="createForm.tags"
                :reserve-keyword="false"
                allow-create
                filterable
                multiple
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
            <div class="tag-tips">
              <el-text size="small" type="info">
                输入新标签名称后按回车即可创建新标签
              </el-text>
            </div>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="handleCloseCreateDialog">取消</el-button>
          <el-button :loading="creating" type="primary" @click="handleCreateTool">
            创建工具
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 编辑工具对话框 -->
    <el-dialog
        v-model="showEditDialog"
        :before-close="handleCloseEditDialog"
        title="编辑工具"
        width="600px"
    >
      <el-form
          ref="editFormRef"
          :model="editForm"
          :rules="editRules"
          label-width="100px"
      >
        <el-form-item label="工具标题" prop="title">
          <el-input
              v-model="editForm.title"
              clearable
              placeholder="请输入工具标题"
          />
        </el-form-item>
        <el-form-item label="工具链接" prop="url">
          <el-input
              v-model="editForm.url"
              clearable
              placeholder="请输入完整的URL地址，如：https://example.com"
          />
        </el-form-item>
        <el-form-item label="工具描述">
          <el-input
              v-model="editForm.description"
              :rows="3"
              clearable
              maxlength="500"
              placeholder="请输入工具描述（可选）"
              show-word-limit
              type="textarea"
          />
        </el-form-item>
        <el-form-item label="工具标签">
          <div class="tag-input-container">
            <el-select
                v-model="editForm.tags"
                :reserve-keyword="false"
                allow-create
                filterable
                multiple
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
            <div class="tag-tips">
              <el-text size="small" type="info">
                输入新标签名称后按回车即可创建新标签
              </el-text>
            </div>
          </div>
        </el-form-item>
        <el-form-item label="工具状态">
          <el-radio-group v-model="editForm.status">
            <el-radio value="draft">草稿</el-radio>
            <el-radio value="published">已发布</el-radio>
            <el-radio value="recycled">已回收</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="handleCloseEditDialog">取消</el-button>
          <el-button :loading="updating" type="primary" @click="handleUpdateTool">
            保存修改
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import {computed, nextTick, onMounted, reactive, ref} from 'vue'
import {ElMessage, ElMessageBox} from 'element-plus'
import {Refresh} from '@element-plus/icons-vue'
import axios from 'axios'

const tools = ref([])
const allTags = ref([])
const showCreateDialog = ref(false)
const showEditDialog = ref(false)
const creating = ref(false)
const updating = ref(false)
const createFormRef = ref(null)
const editFormRef = ref(null)
const currentEditTool = ref(null)

const filterForm = reactive({
  tags: [],
  title: '',
  status: ''
})

const createForm = reactive({
  title: '',
  url: '',
  description: '',
  tags: []
})

const editForm = reactive({
  title: '',
  url: '',
  description: '',
  tags: [],
  status: 'draft'
})

const createRules = {
  title: [
    {required: true, message: '请输入工具标题', trigger: 'blur'},
    {min: 1, max: 255, message: '标题长度应在1-255个字符之间', trigger: 'blur'}
  ],
  url: [
    {required: true, message: '请输入工具链接', trigger: 'blur'},
    {
      pattern: /^https?:\/\/.+/,
      message: '请输入有效的URL地址（必须以http://或https://开头）',
      trigger: 'blur'
    }
  ]
}

const editRules = {
  title: [
    {required: true, message: '请输入工具标题', trigger: 'blur'},
    {min: 1, max: 255, message: '标题长度应在1-255个字符之间', trigger: 'blur'}
  ],
  url: [
    {required: true, message: '请输入工具链接', trigger: 'blur'},
    {
      pattern: /^https?:\/\/.+/,
      message: '请输入有效的URL地址（必须以http://或https://开头）',
      trigger: 'blur'
    }
  ]
}

// 获取工具列表(管理员接口，包含所有状态)
const fetchTools = async () => {
  try {
    const res = await axios.get('/api/admin/tools', {
      timeout: 8000
    })

    if (res.data && Array.isArray(res.data)) {
      tools.value = res.data.map(tool => ({
        ...tool,
        tags: Array.isArray(tool.tags) ? tool.tags : []
      }))
    } else {
      console.warn('工具列表数据格式异常:', res.data)
      tools.value = []
    }
  } catch (error) {
    console.error('获取工具列表失败:', error)

    if (error.response?.status === 401) {
      ElMessage.error('登录已过期，请重新登录')
    } else if (error.code === 'ECONNABORTED') {
      ElMessage.error('请求超时，请检查网络连接')
    } else {
      ElMessage.error('获取工具列表失败，请刷新页面重试')
    }
  }
}

// 获取标签
const fetchTags = async () => {
  try {
    const res = await axios.get('/api/tool-tags', {
      timeout: 5000
    })
    allTags.value = Array.isArray(res.data?.tags) ? res.data.tags : []
  } catch (error) {
    console.warn('获取工具标签失败:', error)
    // 标签获取失败不影响主要功能，只记录警告
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
  if (!tool || !tool.id) {
    ElMessage.error('无效的工具数据')
    return
  }

  currentEditTool.value = {...tool} // 创建副本避免直接修改原数据

  // 填充编辑表单，确保数据类型正确
  editForm.title = tool.title || ''
  editForm.url = tool.url || ''
  editForm.description = tool.description || ''
  editForm.tags = Array.isArray(tool.tags) ? [...tool.tags] : []
  editForm.status = tool.status || 'draft'

  showEditDialog.value = true

  // 确保表单验证状态正确
  nextTick(() => {
    if (editFormRef.value) {
      editFormRef.value.clearValidate()
    }
  })
}

const deleteTool = async (tool) => {
  try {
    await ElMessageBox.confirm('确定要删除该工具吗？', '提示', {type: 'warning'})
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
    await axios.patch(`/api/tools/${tool.id}/status`, {status: newStatus})

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

// 快速更新状态(用于操作按钮)
const quickUpdateStatus = async (tool, newStatus) => {
  const actionText = newStatus === 'recycled' ? '回收' : '恢复'

  try {
    await ElMessageBox.confirm(`确定要${actionText}该工具吗？`, '提示', {type: 'warning'})
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

const handleCloseCreateDialog = () => {
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
    description: '',
    tags: []
  })
}

// 编辑工具相关
const handleUpdateTool = async () => {
  if (!editFormRef.value || !currentEditTool.value) return

  try {
    // 表单验证
    const isValid = await editFormRef.value.validate().catch(() => false)
    if (!isValid) {
      ElMessage.warning('请检查表单填写是否正确')
      return
    }

    updating.value = true

    // 准备更新数据，确保数据格式正确
    const updateData = {
      title: editForm.title?.trim() || '',
      url: editForm.url?.trim() || '',
      description: editForm.description?.trim() || '',
      tags: Array.isArray(editForm.tags) ? editForm.tags.filter(tag => tag?.trim()) : [],
      status: editForm.status || 'draft'
    }

    // 数据验证
    if (!updateData.title) {
      ElMessage.error('工具标题不能为空')
      return
    }

    if (!updateData.url) {
      ElMessage.error('工具链接不能为空')
      return
    }

    // URL格式验证
    const urlPattern = /^https?:\/\/.+/
    if (!urlPattern.test(updateData.url)) {
      ElMessage.error('请输入有效的URL地址')
      return
    }

    console.log('发送更新请求:', updateData)

    // 执行更新操作
    const response = await axios.put(`/api/tools/${currentEditTool.value.id}`, updateData, {
      timeout: 15000, // 15秒超时
      headers: {
        'Content-Type': 'application/json',
      }
    })

    console.log('更新响应:', response)

    // 检查响应状态
    if (response.status === 200) {
      // 更新本地数据
      const index = tools.value.findIndex(t => t.id === currentEditTool.value.id)
      if (index !== -1) {
        // 使用响应数据更新本地数据
        const updatedTool = response.data || {
          ...tools.value[index],
          ...updateData
        }

        // 确保数组字段的正确性
        updatedTool.tags = Array.isArray(updatedTool.tags) ? updatedTool.tags : []

        // 更新本地数据
        tools.value[index] = updatedTool
        console.log('本地数据已更新:', updatedTool)
      }

      ElMessage.success('工具更新成功')
      showEditDialog.value = false
      resetEditForm()

      // 异步刷新标签列表以获取可能新创建的标签
      fetchTags().catch(error => {
        console.warn('刷新标签列表失败:', error)
      })

    } else {
      throw new Error(`更新失败，状态码: ${response.status}`)
    }

  } catch (error) {
    console.error('更新工具失败:', error)

    // 详细的错误处理
    if (error.response) {
      const status = error.response.status
      const errorData = error.response.data
      const message = errorData?.detail || errorData?.message || '服务器错误'

      console.log('错误响应:', error.response)

      switch (status) {
        case 400:
          ElMessage.error(`请求参数错误: ${message}`)
          break
        case 401:
          ElMessage.error('登录已过期，请重新登录')
          break
        case 403:
          ElMessage.error('没有权限执行此操作')
          break
        case 404:
          ElMessage.error('工具不存在或已被删除')
          break
        case 409:
          ElMessage.error(`数据冲突: ${message}`)
          break
        case 422:
          ElMessage.error(`数据验证失败: ${message}`)
          break
        case 500:
          ElMessage.error('服务器内部错误，请稍后重试')
          break
        default:
          ElMessage.error(`更新失败: ${message}`)
      }
    } else if (error.code === 'ECONNABORTED') {
      ElMessage.error('请求超时，请检查网络连接后重试')
    } else if (error.message?.includes('Network Error')) {
      ElMessage.error('网络连接失败，请检查网络后重试')
    } else {
      ElMessage.error('更新工具失败，请稍后重试')
    }
  } finally {
    updating.value = false
  }
}

const handleCloseEditDialog = () => {
  // 检查是否有未保存的更改
  if (hasUnsavedChanges()) {
    ElMessageBox.confirm(
        '您有未保存的更改，确定要关闭吗？',
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
    ).then(() => {
      showEditDialog.value = false
      resetEditForm()
    }).catch(() => {
      // 用户取消关闭
    })
  } else {
    showEditDialog.value = false
    resetEditForm()
  }
}

const resetEditForm = () => {
  if (editFormRef.value) {
    editFormRef.value.clearValidate()
    editFormRef.value.resetFields()
  }
  Object.assign(editForm, {
    title: '',
    url: '',
    description: '',
    tags: [],
    status: 'draft'
  })
  currentEditTool.value = null
}

// 检查是否有未保存的更改
const hasUnsavedChanges = () => {
  if (!currentEditTool.value) return false

  const current = currentEditTool.value
  return (
      editForm.title !== (current.title || '') ||
      editForm.url !== (current.url || '') ||
      editForm.description !== (current.description || '') ||
      editForm.status !== (current.status || 'draft') ||
      JSON.stringify(editForm.tags || []) !== JSON.stringify(current.tags || [])
  )
}

// 状态相关方法
const getStatusText = (status) => {
  switch (status) {
    case 'published':
      return '已发布'
    case 'draft':
      return '草稿'
    case 'recycled':
      return '已回收'
    default:
      return '未知'
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

/* 对话框样式 */
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* 状态单选按钮组样式 */
:deep(.el-radio-group) {
  display: flex;
  gap: 16px;
}

:deep(.el-radio) {
  margin-right: 0;
}

/* 多选标签样式优化 */
:deep(.el-select .el-select__tags) {
  max-height: 120px;
  overflow-y: auto;
}

:deep(.el-select .el-select__tags .el-tag) {
  margin: 2px 4px 2px 0;
}

/* 标签输入容器样式 */
.tag-input-container {
  width: 100%;
}

.tag-tips {
  margin-top: 8px;
}

.tag-tips .el-text {
  color: #909399;
}

/* 文本域样式优化 */
:deep(.el-textarea__inner) {
  resize: vertical;
  min-height: 80px;
}

/* 字数统计样式 */
:deep(.el-input__count) {
  color: #909399;
  font-size: 12px;
}

/* 表单项间距优化 */
:deep(.el-form-item) {
  margin-bottom: 22px;
}

:deep(.el-form-item:last-child) {
  margin-bottom: 0;
}

/* 对话框内容区域优化 */
:deep(.el-dialog__body) {
  padding: 20px 20px 10px 20px;
}

/* 编辑对话框优化样式 */
:deep(.el-dialog__header) {
  padding: 20px 20px 10px 20px;
  border-bottom: 1px solid #ebeef5;
}

:deep(.el-dialog__title) {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

/* 表单验证错误提示样式 */
:deep(.el-form-item__error) {
  color: #f56c6c;
  font-size: 12px;
  line-height: 1;
  padding-top: 4px;
}

/* 加载状态按钮样式 */
:deep(.el-button.is-loading) {
  position: relative;
  pointer-events: none;
}

:deep(.el-button.is-loading:before) {
  pointer-events: none;
  content: '';
  position: absolute;
  left: -1px;
  top: -1px;
  right: -1px;
  bottom: -1px;
  border-radius: inherit;
  background-color: rgba(255, 255, 255, .35);
}
</style>