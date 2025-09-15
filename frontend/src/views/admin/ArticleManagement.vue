<template>
  <div class="article-management">
    <!-- 操作栏 -->
    <div class="action-bar">
      <div class="action-buttons">
        <!-- 删除新建文章按钮 -->
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
        <el-col :span="8">
          <el-card class="filter-card category-card" shadow="never">
            <template #header>
              <div class="filter-header">
                <span>文章分类</span>
                <el-button link @click="clearCategoryFilter" v-if="filterForm.category" class="reset-link-btn">清空</el-button>
              </div>
            </template>
            <div v-loading="categoryLoading" class="category-content">
              <el-tree
                v-if="!categoryLoading && categoryTree.length > 0"
                :data="categoryTree"
                :props="treeProps"
                @node-click="handleCategoryClick"
                :highlight-current="true"
                :expand-on-click-node="false"
                node-key="path"
                ref="categoryTreeRef"
                class="category-tree"
                :current-node-key="filterForm.category"
              />
              <el-empty v-else-if="!categoryLoading && categoryTree.length === 0" description="暂无分类" :image-size="40" />
            </div>
          </el-card>
        </el-col>

        <!-- 其他筛选条件 -->
        <el-col :span="16">
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
              </div>
              <div class="filter-row">
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
              <div class="filter-row">
                <div class="filter-item">
                  <label>时间排序：</label>
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

    <!-- 文章列表 -->
    <div class="article-list">
      <el-card shadow="never">
        <template #header>
          <div class="list-header">
            <span>文章列表</span>
            <span class="article-count">共 {{ sortedArticles.length }} 篇文章</span>
          </div>
        </template>
        <el-table
          :data="sortedArticles"
          stripe
          class="article-table"
          empty-text="暂无文章数据"
          :header-cell-style="{ background: '#fafafa', color: '#333', fontWeight: '600' }"
        >
          <el-table-column prop="title" label="文章标题" min-width="200" show-overflow-tooltip>
            <template #default="scope">
              <div class="article-title">{{ scope.row.title }}</div>
            </template>
          </el-table-column>
          <el-table-column prop="slug" label="文件名" min-width="150" show-overflow-tooltip>
            <template #default="scope">
              <div class="article-slug">{{ scope.row.slug }}</div>
            </template>
          </el-table-column>
          <el-table-column prop="category" label="分类" min-width="120" show-overflow-tooltip>
            <template #default="scope">
              <span v-if="scope.row.category" class="article-category">{{ scope.row.category }}</span>
              <span v-else class="no-category">未分类</span>
            </template>
          </el-table-column>
          <el-table-column prop="tags" label="标签" min-width="150" show-overflow-tooltip>
            <template #default="scope">
              <div v-if="scope.row.tags && scope.row.tags.length > 0" class="article-tags">
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
                @change="(value) => updateArticleStatus(scope.row, value)"
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
              <div class="article-date">{{ formatDate(scope.row.date) }}</div>
            </template>
          </el-table-column>
          <el-table-column label="操作" min-width="160" align="center">
            <template #default="scope">
              <div class="action-buttons-table">
                <!-- 删除编辑按钮 -->
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
                <el-button size="small" type="danger" @click="deleteArticle(scope.row)">删除</el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
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
import UploadArticleDialog from '@/components/Admin/UploadArticleDialog.vue'

const articles = ref([])
const allTags = ref([])
const categoryTree = ref([])
const categoriesFromDB = ref([])
const categoryLoading = ref(false)
const categoryTreeRef = ref(null)
const showUploadDialog = ref(false)
const filterForm = reactive({
  category: '',
  tags: [],
  title: '',
  status: ''
})

const sortKey = ref('date')
const sortOrder = ref('desc')

const treeProps = {
  children: 'children',
  label: 'label'
}

// 获取分类数据
const fetchCategories = async () => {
  categoryLoading.value = true
  try {
    const response = await axios.get('/api/articles/categories', {
      timeout: 10000,
      headers: {
        'Accept': 'application/json'
      }
    })

    if (response.data && response.data.categories) {
      categoriesFromDB.value = response.data.categories
      // 构建分类树
      buildCategoryTreeFromData()
      console.log(`成功获取 ${categoriesFromDB.value.length} 个分类`)
    }
  } catch (error) {
    console.error('获取分类数据失败:', error)
    // 如果数据库获取失败，尝试从文章数据构建
    buildCategoryTreeFromArticles()
  } finally {
    categoryLoading.value = false
  }
}

// 从数据库数据构建分类树
const buildCategoryTreeFromData = () => {
  const root = []
  const map = new Map()

  categoriesFromDB.value.forEach(cat => {
    const pathParts = cat.path.split('/')
    let currentLevel = root
    let currentPath = ''

    pathParts.forEach((part, index) => {
      currentPath += (index > 0 ? '/' : '') + part
      let node = map.get(currentPath)

      if (!node) {
        node = {
          label: part,
          path: currentPath,
          children: [],
        }
        map.set(currentPath, node)
        currentLevel.push(node)
      }
      currentLevel = node.children
    })
  })

  categoryTree.value = root
  console.log('从数据库构建的分类树:', root)
}

// 从文章数据构建分类树（备用方案）
const buildCategoryTreeFromArticles = () => {
  const root = []
  const map = new Map()

  articles.value.forEach(article => {
    if (!article.category) return

    const pathParts = article.category.split('/')
    let currentLevel = root
    let currentPath = ''

    pathParts.forEach((part, index) => {
      currentPath += (index > 0 ? '/' : '') + part
      let node = map.get(currentPath)

      if (!node) {
        node = {
          label: part,
          path: currentPath,
          children: [],
        }
        map.set(currentPath, node)
        currentLevel.push(node)
      }
      currentLevel = node.children
    })
  })

  categoryTree.value = root
  console.log('从文章构建的分类树:', root)
}

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

// 获取标签
const fetchTags = async () => {
  const res = await axios.get('/api/tags')
  allTags.value = res.data.tags || []
}

// 分类点击处理
const handleCategoryClick = (data) => {
  console.log('点击分类:', data)
  if (filterForm.category === data.path) {
    clearCategoryFilter()
  } else {
    filterForm.category = data.path
  }
}

const clearCategoryFilter = () => {
  filterForm.category = ''
  if (categoryTreeRef.value) {
    categoryTreeRef.value.setCurrentKey(null)
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
  clearCategoryFilter()
}

const setSortOrder = (order) => {
  sortOrder.value = order
}

const applySort = () => {}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}

// 文章操作
const openUploadDialog = () => {
  showUploadDialog.value = true
}

// 显示待开发提示
const showDevelopingMessage = () => {
  ElMessage.info('该功能正在开发中，敬请期待！')
}

const deleteArticle = async (article) => {
  try {
    await ElMessageBox.confirm('确定要删除该文章吗？', '提示', { type: 'warning' })
    await axios.delete(`/api/articles/${article.id}`)
    ElMessage.success('删��成功')
    refreshArticles()
  } catch {}
}

const refreshArticles = async () => {
  await fetchArticles()
  await fetchTags()
  await fetchCategories()
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
const getStatusType = (status) => {
  switch (status) {
    case 'published': return 'success'
    case 'draft': return 'warning'
    case 'recycled': return 'danger'
    default: return 'info'
  }
}

const getStatusText = (status) => {
  switch (status) {
    case 'published': return '已��布'
    case 'draft': return '草稿'
    case 'recycled': return '已回收'
    default: return '未知'
  }
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

.filter-card {
  border-radius: 12px;
  border: 1px solid #e1e8ed;
  height: 300px; /* 固定卡片高度 */
}

.category-card .category-content {
  height: 220px; /* 固定分类内容区域高度 */
  overflow-y: auto; /* 添加滚动 */
}

.filter-controls {
  padding: 10px 0;
  height: 220px; /* 固定筛选内容区域高度 */
  overflow-y: auto; /* 添加滚动 */
}

.tag-row {
  margin-bottom: 20px; /* 标签行单独间距 */
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

.category-tree {
  background: transparent;
}

.article-list .filter-card {
  border: 1px solid #e1e8ed;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  color: #333;
}

.article-count {
  color: #666;
  font-size: 14px;
  font-weight: normal;
}

.article-table {
  border-radius: 8px;
  overflow: hidden;
}

.article-title {
  font-weight: 500;
  color: #333;
}

.article-slug {
  font-family: 'Monaco', 'Consolas', monospace;
  color: #666;
  font-size: 13px;
}

.article-category {
  color: #666;
}

.article-tags {
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

.article-date {
  color: #666;
  font-size: 13px;
}

.no-category {
  color: #999;
  font-style: italic;
}

.action-buttons-table {
  display: flex;
  gap: 8px;
  justify-content: center;
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

.clear-category-btn {
  color: #666 !important;
  font-weight: normal !important;
}

.clear-category-btn:hover {
  color: #409eff !important;
  background: transparent !important;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 自定义滚动条样式 */
.category-content::-webkit-scrollbar,
.filter-controls::-webkit-scrollbar {
  width: 6px;
}

.category-content::-webkit-scrollbar-track,
.filter-controls::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.category-content::-webkit-scrollbar-thumb,
.filter-controls::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.category-content::-webkit-scrollbar-thumb:hover,
.filter-controls::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
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

:deep(.el-tree-node__content) {
  padding: 6px 0;
}

:deep(.el-tree-node__content:hover) {
  background-color: #f5f7fa;
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

/* 操作按钮样式优化 */
.action-buttons-table {
  display: flex;
  gap: 6px;
  justify-content: center;
  flex-wrap: wrap;
}

.action-buttons-table .el-button {
  margin: 2px 0;
}

/* 禁用按钮样式 */
.el-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.action-buttons .el-button:disabled {
  background-color: #f5f7fa;
  border-color: #e4e7ed;
  color: #c0c4cc;
}

.action-buttons .el-button--primary:disabled {
  background-color: #a0cfff;
  border-color: #a0cfff;
  color: #ffffff;
}
</style>
