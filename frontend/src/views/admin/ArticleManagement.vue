<template>
  <div class="article-management">
    <!-- 操作栏 -->
    <div class="action-bar">
      <div class="action-buttons">
        <el-button @click="openUploadDialog">
          上传文章
        </el-button>
        <el-button :icon="Refresh" circle @click="refreshArticles"/>
      </div>
    </div>

<!-- 筛选区域 -->
    <div class="filter-section">
      <el-row :gutter="20">
        <!-- 分类筛选 -->
        <el-col :span="24" :md="12">
          <CategoryFilterCard
            v-model="filterForm.category"
          />
        </el-col>

        <!-- 其他筛选条件 -->
        <el-col :span="24" :md="12">
          <FilterControlsCard
              :filters="filterForm"
              :sort-order="sortOrder"
              @reset="resetAllFilters"
              @update:tags="filterForm.tags = $event"
              @update:title="filterForm.title = $event"
              @update:status="filterForm.status = $event"
              @update:sortOrder="sortOrder = $event"
              style="height: 300px;"
          />
        </el-col>
      </el-row>
    </div>

    <!-- 文章列表 -->
    <div class="article-list">
      <ArticleListCard
          :articles="paginatedArticles"
          :total="sortedArticles.length"
          @delete="deleteArticle"
          @edit="openEditDialog"
          @update-status="updateArticleStatus"
          @quick-update-status="quickUpdateStatus"
      />
      
      <!-- 添加分页组件 -->
      <div v-if="sortedArticles.length > pageSize" class="pagination-wrapper">
        <el-pagination
            v-model:current-page="currentPage"
            :page-size="pageSize"
            :total="sortedArticles.length"
            background
            layout="prev, pager, next, jumper, total"
            @current-change="handlePageChange"
        />
      </div>
    </div>

    <!-- 上传文章对话框 -->
    <UploadArticleDialog
        v-model="showUploadDialog"
        @upload-success="refreshArticles"
    />

    <!-- 编辑文章对话框 -->
    <EditArticleDialog
        v-model="showEditDialog"
        :article="editingArticle"
        @update-success="refreshArticles"
    />
  </div>
</template>

<script setup>
import {computed, onMounted, reactive, ref, watch} from 'vue'
import {ElMessage, ElMessageBox} from 'element-plus'
import {Refresh} from '@element-plus/icons-vue'
import axios from 'axios'
import UploadArticleDialog from '@/components/Admin/ArticleManagement/UploadArticleDialog.vue'
import EditArticleDialog from '@/components/Admin/ArticleManagement/EditArticleDialog.vue'
import FilterControlsCard from '@/components/Admin/ArticleManagement/FilterControlsCard.vue'
import CategoryFilterCard from '@/components/Admin/ArticleManagement/CategoryFilterCard.vue'
import ArticleListCard from '@/components/Admin/ArticleManagement/ArticleListCard.vue'

const articles = ref([])
const filterForm = reactive({
  tags: [],
  title: '',
  category: '',
  status: ''
})

const sortOrder = ref('desc')
// 添加分页状态
const currentPage = ref(1)
const pageSize = ref(10)

// 获取文章列表(管理员接口，包含所有状态)
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
    const v1 = new Date(a.date || '1970-01-01')
    const v2 = new Date(b.date || '1970-01-01')

    if (v1 < v2) return sortOrder.value === 'asc' ? -1 : 1
    if (v1 > v2) return sortOrder.value === 'asc' ? 1 : -1
    return 0
  })
  return arr
})

// 添加分页计算属性
const paginatedArticles = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return sortedArticles.value.slice(start, end)
})

// 筛选和排序操作
const resetAllFilters = () => {
  filterForm.tags = []
  filterForm.title = ''
  filterForm.category = ''
  filterForm.status = ''
  currentPage.value = 1
}

// 添加分页处理函数
const handlePageChange = (page) => {
  currentPage.value = page
}

// 监听筛选变化，重置到第一页
watch([() => filterForm.tags, () => filterForm.title, () => filterForm.category, () => filterForm.status, () => sortOrder.value], () => {
  currentPage.value = 1
}, { deep: true })

// 文章操作
const openUploadDialog = () => {
  showUploadDialog.value = true
}

const openEditDialog = (article) => {
  editingArticle.value = {...article}
  showEditDialog.value = true
}

const deleteArticle = async (article) => {
  try {
    await ElMessageBox.confirm('确定要删除该文章吗？', '提示', {type: 'warning'})
    await axios.delete(`/api/articles/${article.id}`)
    ElMessage.success('删除成功')
    refreshArticles()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除文章失败:', error)
      ElMessage.error('删除文章失败')
    }
  }
}

const refreshArticles = async () => {
  await fetchArticles()
}

// 更新文章状态
const updateArticleStatus = async (article, newStatus) => {
  if (article.status === newStatus) return

  try {
    await axios.patch(`/api/articles/${article.id}/status`, {status: newStatus})

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

// 快速更新状态(用于操作按钮)
const quickUpdateStatus = async (article, newStatus) => {
  const actionText = newStatus === 'recycled' ? '回收' : '恢复'

  try {
    await ElMessageBox.confirm(`确定要${actionText}该文章吗？`, '提示', {type: 'warning'})
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

const showUploadDialog = ref(false)
const showEditDialog = ref(false)
const editingArticle = ref(null)

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

.article-list {
  background: white;
  border-radius: 12px;
  overflow: hidden;
}

/* 分页样式 */
.pagination-wrapper {
  display: flex;
  justify-content: center;
  padding: 20px 0;
  border-top: 1px solid #ebeef5;
  background: white;
}

:deep(.el-pagination) {
  --el-pagination-bg-color: #f8f9fa;
  --el-pagination-text-color: #666;
  --el-pagination-border-radius: 6px;
}

:deep(.el-pagination .btn-prev),
:deep(.el-pagination .btn-next) {
  border-radius: 6px;
}

:deep(.el-pagination .el-pager li) {
  border-radius: 6px;
  margin: 0 2px;
}

/* 响应式布局 */
@media (max-width: 768px) {
  .article-management {
    padding: 15px;
  }
  
  .action-bar {
    margin-bottom: 15px;
  }
  
  .filter-section {
    margin-bottom: 15px;
  }
  
  .action-buttons {
    flex-wrap: wrap;
  }
  
  /* 在中等屏幕上也使用垂直布局 */
  .el-row {
    flex-direction: column;
    gap: 15px;
  }
  
  .el-col {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .article-management {
    padding: 10px;
  }
  
  .action-bar {
    margin-bottom: 10px;
  }
  
  .filter-section {
    margin-bottom: 10px;
  }
  
  .el-row {
    flex-direction: column;
    gap: 10px;
  }
  
  .el-col {
    width: 100%;
  }
}
</style>
