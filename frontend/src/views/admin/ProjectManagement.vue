<template>
  <div class="project-management">
    <!-- 操作栏 -->
    <div class="action-bar">
      <div class="action-buttons">
        <el-button @click="openUploadDialog">
          上传项目
        </el-button>
        <el-button :icon="Refresh" circle @click="refreshProjects"/>
      </div>
    </div>

    <!-- 筛选区域 -->
    <div class="filter-section">
      <el-row :gutter="20">
        <el-col :span="24">
          <FilterControlsCard
              :filters="filterForm"
              :sort-order="sortOrder"
              @reset="resetAllFilters"
              @update:tags="filterForm.tags = $event"
              @update:title="filterForm.title = $event"
              @update:status="filterForm.status = $event"
              @update:sortOrder="sortOrder = $event"
          />
        </el-col>
      </el-row>
    </div>

    <!-- 项目列表 -->
    <div class="project-list">
      <ProjectListCard
          :projects="sortedProjects"
          @delete="deleteProject"
          @edit="openEditDialog"
          @update-status="updateProjectStatus"
          @quick-update-status="quickUpdateStatus"
      />
    </div>

    <!-- 上传项目对话框 -->
    <UploadProjectDialog
        v-model="showUploadDialog"
        @upload-success="refreshProjects"
    />

    <!-- 编辑项目对话框 -->
    <EditProjectDialog
        v-model="showEditDialog"
        :project="editingProject"
        @update-success="refreshProjects"
    />
  </div>
</template>

<script setup>
import {computed, onMounted, reactive, ref} from 'vue'
import {ElMessage, ElMessageBox} from 'element-plus'
import {Refresh} from '@element-plus/icons-vue'
import axios from 'axios'
import UploadProjectDialog from '@/components/Admin/ProjectManagement/UploadProjectDialog.vue'
import EditProjectDialog from '@/components/Admin/ProjectManagement/EditProjectDialog.vue'
import FilterControlsCard from '@/components/Admin/ProjectManagement/FilterControlsCard.vue'
import ProjectListCard from '@/components/Admin/ProjectManagement/ProjectListCard.vue'

const projects = ref([])
const filterForm = reactive({
  tags: [],
  title: '',
  status: ''
})

const sortOrder = ref('desc')
const showUploadDialog = ref(false)
const showEditDialog = ref(false)
const editingProject = ref(null)

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

// 项目操作
const openUploadDialog = () => {
  showUploadDialog.value = true
}

const openEditDialog = (project) => {
  editingProject.value = {...project}
  showEditDialog.value = true
}

const deleteProject = async (project) => {
  try {
    await ElMessageBox.confirm('确定要删除该项目吗？', '提示', {type: 'warning'})
    await axios.delete(`/api/projects/${project.id}`)
    ElMessage.success('删除成功')
    refreshProjects()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除项目失败:', error)
      ElMessage.error('删除项目失败')
    }
  }
}

const refreshProjects = async () => {
  await fetchProjects()
}

// 更新项目状态
const updateProjectStatus = async (project, newStatus) => {
  if (project.status === newStatus) return

  try {
    await axios.patch(`/api/projects/${project.id}/status`, {status: newStatus})

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
    await ElMessageBox.confirm(`确定要${actionText}该项目吗？`, '提示', {type: 'warning'})
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
</style>
