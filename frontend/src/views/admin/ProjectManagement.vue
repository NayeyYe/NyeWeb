<template>
  <div class="project-management">
    <!-- 操作栏 -->
    <div class="action-bar">
      <div class="action-buttons">
        <el-button type="primary" @click="handleCreateProject">新建项目</el-button>
        <el-button @click="handleUploadProject">上传项目</el-button>
        <el-button @click="refreshProjects" :icon="Refresh" circle />
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
                <div class="filter-item">
                  <label>排序：</label>
                  <el-button-group>
                    <el-button :type="sortOrder === 'asc' ? 'primary' : ''" @click="setSortOrder('asc')">升序</el-button>
                    <el-button :type="sortOrder === 'desc' ? 'primary' : ''" @click="setSortOrder('desc')">降序</el-button>
                  </el-button-group>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 项目列表 -->
    <div class="project-list">
      <el-card shadow="never">
        <template #header>
          <div class="list-header">
            <span>项目列表</span>
            <span class="project-count">共 {{ sortedProjects.length }} 个项目</span>
          </div>
        </template>
        <el-table
          :data="sortedProjects"
          stripe
          class="project-table"
          empty-text="暂无项目数据"
          :header-cell-style="{ background: '#fafafa', color: '#333', fontWeight: '600' }"
        >
          <el-table-column prop="title" label="项目标题" min-width="200" show-overflow-tooltip>
            <template #default="scope">
              <div class="project-title">{{ scope.row.title }}</div>
            </template>
          </el-table-column>
          <el-table-column prop="slug" label="项目标识" min-width="150" show-overflow-tooltip>
            <template #default="scope">
              <div class="project-slug">{{ scope.row.slug }}</div>
            </template>
          </el-table-column>
          <el-table-column prop="summary" label="项目简介" min-width="200" show-overflow-tooltip>
            <template #default="scope">
              <div class="project-summary">{{ scope.row.summary || '暂无简介' }}</div>
            </template>
          </el-table-column>
          <el-table-column prop="tags" label="标签" min-width="150" show-overflow-tooltip>
            <template #default="scope">
              <div v-if="scope.row.tags && scope.row.tags.length > 0" class="project-tags">
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
                @change="(value) => updateProjectStatus(scope.row, value)"
                size="small"
                style="width: 100px"
              >
                <el-option label="草稿" value="draft" />
                <el-option label="已发布" value="published" />
                <el-option label="已回收" value="recycled" />
              </el-select>
            </template>
          </el-table-column>
          <el-table-column prop="date" label="创建时间" min-width="120">
            <template #default="scope">
              <div class="project-date">{{ formatDate(scope.row.date) }}</div>
            </template>
          </el-table-column>
          <el-table-column label="操作" min-width="160" align="center">
            <template #default="scope">
              <div class="action-buttons-table">
                <el-button size="small" type="primary" @click="handleEditProject(scope.row)">编辑</el-button>
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
                <el-button size="small" type="danger" @click="deleteProject(scope.row)">删除</el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import {computed, onMounted, reactive, ref} from 'vue'
import {ElMessage, ElMessageBox} from 'element-plus'
import {Refresh} from '@element-plus/icons-vue'
import axios from 'axios'

const projects = ref([])
const allTags = ref([])
const filterForm = reactive({
  tags: [],
  title: '',
  status: ''
})

const sortOrder = ref('desc')

// 获取项目列表（管理员接口，包含所有状态）
const fetchProjects = async () => {
  try {
    const res = await axios.get('/api/admin/projects')
    projects.value = res.data
  } catch (error) {
    console.error('获取项目列表失败:', error)
    ElMessage.error('获取项目列表失败')
  }
}

// 获取标签
const fetchTags = async () => {
  try {
    const res = await axios.get('/api/project-tags')
    allTags.value = res.data.tags || []
  } catch (error) {
    console.error('获取项目标签失败:', error)
  }
}

// 项目筛选
const filteredProjects = computed(() => {
  let arr = projects.value
  if (filterForm.tags && filterForm.tags.length) {
    arr = arr.filter(p => p.tags && filterForm.tags.every(tag => p.tags.includes(tag)))
  }
  if (filterForm.title) {
    arr = arr.filter(p => p.title && p.title.includes(filterForm.title))
  }
  if (filterForm.status) {
    arr = arr.filter(p => p.status === filterForm.status)
  }
  return arr
})

// 排序
const sortedProjects = computed(() => {
  const arr = [...filteredProjects.value]
  arr.sort((a, b) => {
    const v1 = new Date(a.date || '1970-01-01')
    const v2 = new Date(b.date || '1970-01-01')
    
    if (v1 < v2) return sortOrder.value === 'asc' ? -1 : 1
    if (v1 > v2) return sortOrder.value === 'asc' ? 1 : -1
    return 0
  })
  return arr
})

// 筛选和排序操作
const resetAllFilters = () => {
  filterForm.tags = []
  filterForm.title = ''
  filterForm.status = ''
}

const setSortOrder = (order) => {
  sortOrder.value = order
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return '暂无'
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}

// 项目操作
const handleCreateProject = () => {
  ElMessage.info('新建项目功能开发中，敬请期待！')
}

const handleUploadProject = () => {
  ElMessage.info('上传项目功能开发中，敬请期待！')
}

const handleEditProject = (project) => {
  ElMessage.info(`编辑项目 "${project.title}" 功能开发中，敬请期待！`)
}

const deleteProject = async (project) => {
  try {
    await ElMessageBox.confirm('确定要删除该项目吗？', '提示', { type: 'warning' })
    // TODO: 实现删除API
    ElMessage.info('删除项目功能开发中，敬请期待！')
  } catch {}
}

const refreshProjects = async () => {
  await fetchProjects()
  await fetchTags()
}

// 更新项目状态
const updateProjectStatus = async (project, newStatus) => {
  if (project.status === newStatus) return
  
  try {
    await axios.patch(`/api/projects/${project.id}/status`, { status: newStatus })
    
    // 更新本地数据
    project.status = newStatus
    
    const statusText = getStatusText(newStatus)
    ElMessage.success(`项目状态已更新为：${statusText}`)
  } catch (error) {
    console.error('更新项目状态失败:', error)
    ElMessage.error('更新项目状态失败')
    // 刷新数据以恢复原状态
    refreshProjects()
  }
}

// 快速更新状态（用于操作按钮）
const quickUpdateStatus = async (project, newStatus) => {
  const actionText = newStatus === 'recycled' ? '回收' : '恢复'
  
  try {
    await ElMessageBox.confirm(`确定要${actionText}该项目吗？`, '提示', { type: 'warning' })
    await updateProjectStatus(project, newStatus)
  } catch (error) {
    if (error !== 'cancel') {
      console.error(`${actionText}项目失败:`, error)
    }
  }
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
  refreshProjects()
})
</script>

<style scoped>
.project-management {
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

.project-list .filter-card {
  border: 1px solid #e1e8ed;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  color: #333;
}

.project-count {
  color: #666;
  font-size: 14px;
  font-weight: normal;
}

.project-table {
  border-radius: 8px;
  overflow: hidden;
}

.project-title {
  font-weight: 500;
  color: #333;
}

.project-slug {
  font-family: 'Monaco', 'Consolas', monospace;
  color: #666;
  font-size: 13px;
}

.project-summary {
  color: #666;
  font-size: 14px;
}

.project-tags {
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

.project-date {
  color: #666;
  font-size: 13px;
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
</style>

