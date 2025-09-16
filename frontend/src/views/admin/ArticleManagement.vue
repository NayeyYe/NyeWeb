<template>
  <div class="article-management">
    <!-- 操作栏 -->
    <div class="action-bar">
      <div class="action-buttons">
        <el-button @click="openUploadDialog">
          上传文章
        </el-button>
        <el-button @click="refreshArticles" :icon="Refresh" circle />
      </div>
    </div>

    <!-- 筛选区域 -->
    <div class="filter-section">
      <el-row :gutter="20">
        <!-- 分类筛选 -->
        <el-col :span="6">
          <CategoryFilterCard
            v-model="filterForm.category"
          />
        </el-col>

        <!-- 其他筛选条件 -->
        <el-col :span="18">
          <FilterControlsCard
            :filters="filterForm"
            :sort-order="sortOrder"
            @update:tags="filterForm.tags = $event"
            @update:title="filterForm.title = $event"
            @update:status="filterForm.status = $event"
            @update:sortOrder="sortOrder = $event"
            @reset="resetAllFilters"
          />
        </el-col>
      </el-row>
    </div>

    <!-- 文章列表 -->
    <div class="article-list">
      <ArticleListCard
        :articles="sortedArticles"
        @update-status="updateArticleStatus"
        @quick-update-status="quickUpdateStatus"
        @delete="deleteArticle"
      />
    </div>

    <!-- 上传文章对话框 -->
    <UploadArticleDialog
      v-model="showUploadDialog"
      @upload-success="refreshArticles"
    />
  </div>
</template>

<script setup>
import {computed, onMounted, reactive, ref} from 'vue'
import {ElMessage, ElMessageBox} from 'element-plus'
import {Refresh} from '@element-plus/icons-vue'
import axios from 'axios'
import UploadArticleDialog from '@/components/Admin/ArticleManagement/UploadArticleDialog.vue'
import CategoryFilterCard from '@/components/Admin/ArticleManagement/CategoryFilterCard.vue'
import FilterControlsCard from '@/components/Admin/ArticleManagement/FilterControlsCard.vue'
import ArticleListCard from '@/components/Admin/ArticleManagement/ArticleListCard.vue'

const articles = ref([])
const showUploadDialog = ref(false)
const filterForm = reactive({
  category: '',
  tags: [],
  title: '',
  status: ''
})

const sortOrder = ref('desc')

// 获取文章列表（管理员接口，包含所有状态）
const fetchArticles = async () => {
  try {
    const res = await axios.get('/api/admin/articles')
    articles.value = res.data
  } catch (error) {
    console.error('获取文章列表失败:', error)
    ElMessage.error('获取文章列表失败')
  }
}

// 文章筛选
const filteredArticles = computed(() => {
  let arr = articles.value
  if (filterForm.category && filterForm.category !== '') {
    arr = arr.filter(a =>
      a.category &&
      (a.category === filterForm.category || a.category.startsWith(filterForm.category + '/'))
    )
  }
  if (filterForm.tags && filterForm.tags.length) {
    arr = arr.filter(a => a.tags && filterForm.tags.every(tag => a.tags.includes(tag)))
  }
  if (filterForm.title) {
    arr = arr.filter(a => a.title && a.title.includes(filterForm.title))
  }
  if (filterForm.status) {
    arr = arr.filter(a => a.status === filterForm.status)
  }
  return arr
})

// 排序
const sortedArticles = computed(() => {
  const arr = [...filteredArticles.value]
  arr.sort((a, b) => {
    const v1 = new Date(a.date)
    const v2 = new Date(b.date)
    
    if (v1 < v2) return sortOrder.value === 'asc' ? -1 : 1
    if (v1 > v2) return sortOrder.value === 'asc' ? 1 : -1
    return 0
  })
  return arr
})

// 筛选和排序操作
const resetAllFilters = () => {
  filterForm.category = ''
  filterForm.tags = []
  filterForm.title = ''
  filterForm.status = ''
}

// 文章操作
const openUploadDialog = () => {
  showUploadDialog.value = true
}

const deleteArticle = async (article) => {
  try {
    await ElMessageBox.confirm('确定要删除该文章吗？', '提示', { type: 'warning' })
    await axios.delete(`/api/articles/${article.id}`)
    ElMessage.success('删除成功')
    refreshArticles()
  } catch {}
}

const refreshArticles = async () => {
  await fetchArticles()
}

// 更新文章状态
const updateArticleStatus = async (article, newStatus) => {
  if (article.status === newStatus) return
  
  try {
    await axios.patch(`/api/articles/${article.id}/status`, { status: newStatus })
    
    // 更新本地数据
    article.status = newStatus
    
    const statusText = getStatusText(newStatus)
    ElMessage.success(`文章状态已更新为：${statusText}`)
  } catch (error) {
    console.error('更新文章状态失败:', error)
    ElMessage.error('更新文章状态失败')
    // 刷新数据以恢复原状态
    refreshArticles()
  }
}

// 快速更新状态（用于操作按钮）
const quickUpdateStatus = async (article, newStatus) => {
  const statusText = getStatusText(newStatus)
  const actionText = newStatus === 'recycled' ? '回收' : '恢复'
  
  try {
    await ElMessageBox.confirm(`确定要${actionText}该文章吗？`, '提示', { type: 'warning' })
    await updateArticleStatus(article, newStatus)
  } catch (error) {
    if (error !== 'cancel') {
      console.error(`${actionText}文章失败:`, error)
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

// 刷新所有数据
const refreshAllData = async () => {
  await Promise.all([
    fetchArticles(),
    fetchTags()
  ])
}

onMounted(() => {
  refreshArticles()
})
</script>

<style scoped>
.article-management {
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
