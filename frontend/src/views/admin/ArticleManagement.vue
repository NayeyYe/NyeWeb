<template>
  <div class="article-management">
    <!-- 操作栏 -->
    <div class="action-bar">
      <div class="action-buttons">
        <el-button type="primary" @click="openEditor('create')">新建文章</el-button>
        <el-button @click="openUploadDialog">上传文章</el-button>
        <el-button @click="refreshArticles" :icon="Refresh" circle />
      </div>
    </div>

    <!-- 筛选区域 -->
    <div class="filter-section">
      <el-row :gutter="20">
        <!-- 分类筛选 -->
        <el-col :span="6">
          <el-card class="filter-card" shadow="never">
            <template #header>
              <div class="filter-header">
                <span>文章分类</span>
                <el-button link type="primary" @click="clearCategoryFilter" v-if="filterForm.category">清空</el-button>
              </div>
            </template>
            <div v-loading="categoryLoading">
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
              />
              <el-empty v-else-if="!categoryLoading && categoryTree.length === 0" description="暂无分类" :image-size="40" />
            </div>
          </el-card>
        </el-col>

        <!-- 其他筛选条件 -->
        <el-col :span="18">
          <el-card class="filter-card" shadow="never">
            <template #header>
              <div class="filter-header">
                <span>筛选条件</span>
                <el-button link type="primary" @click="resetAllFilters">重置</el-button>
              </div>
            </template>
            <div class="filter-controls">
              <div class="filter-row">
                <div class="filter-item">
                  <label>标签筛选：</label>
                  <el-select
                    v-model="filterForm.tags"
                    multiple
                    filterable
                    allow-create
                    placeholder="选择或输入标签"
                    style="width: 200px"
                    size="default"
                  >
                    <el-option
                      v-for="tag in allTags"
                      :key="tag"
                      :label="tag"
                      :value="tag"
                    />
                  </el-select>
                </div>
                <div class="filter-item">
                  <label>标题搜索：</label>
                  <el-input
                    v-model="filterForm.title"
                    placeholder="输入标题关键字"
                    style="width: 200px"
                    clearable
                  />
                </div>
              </div>
              <div class="filter-row">
                <div class="filter-item">
                  <label>排序方式：</label>
                  <el-select v-model="sortKey" style="width: 120px" @change="applySort">
                    <el-option label="创建时间" value="date" />
                    <el-option label="标题" value="title" />
                    <el-option label="文件名" value="slug" />
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
              <el-tag v-if="scope.row.category" size="small" type="info">{{ scope.row.category }}</el-tag>
              <span v-else class="no-category">未分类</span>
            </template>
          </el-table-column>
          <el-table-column prop="date" label="创建时间" min-width="120">
            <template #default="scope">
              <div class="article-date">{{ formatDate(scope.row.date) }}</div>
            </template>
          </el-table-column>
          <el-table-column label="操作" min-width="180" align="center">
            <template #default="scope">
              <div class="action-buttons-table">
                <el-button size="small" @click="previewArticle(scope.row)">预览</el-button>
                <el-button size="small" type="primary" @click="openEditor('edit', scope.row)">编辑</el-button>
                <el-button size="small" type="danger" @click="deleteArticle(scope.row)">删除</el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>

    <!-- 文章编辑器 -->
    <ArticleEditor
      v-model="showEditor"
      :mode="editorMode"
      :article="currentArticle"
      @save="onEditorSave"
      @close="showEditor = false"
    />

    <!-- 上传文章对话框 -->
    <UploadArticleDialog
      v-model="showUploadDialog"
      @upload-success="refreshArticles"
    />

    <!-- 文章预览对话框 -->
    <ArticlePreviewDialog
      v-model="showPreviewDialog"
      :article="previewingArticle"
      @edit="openEditor('edit', $event)"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import axios from 'axios'
import ArticleEditor from '@/components/Admin/ArticleEditor.vue'
import UploadArticleDialog from '@/components/Admin/UploadArticleDialog.vue'
import ArticlePreviewDialog from '@/components/Admin/ArticlePreviewDialog.vue'

const articles = ref([])
const allTags = ref([])
const categoryTree = ref([])
const categoriesFromDB = ref([])
const categoryLoading = ref(false)
const categoryTreeRef = ref(null)
const showEditor = ref(false)
const editorMode = ref('create')
const currentArticle = ref(null)
const showUploadDialog = ref(false)
const showPreviewDialog = ref(false)
const previewingArticle = ref(null)
const filterForm = reactive({
  category: '',
  tags: [],
  title: ''
})

const sortKey = ref('date')
const sortOrder = ref('desc')

const treeProps = {
  children: 'children',
  label: 'label'
}

// 获取分类数据 - 参考ArticleCategoryTree.vue的写法
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
      console.log(`成功获取 ${categoriesFromDB.value.length} 个分类`)
    }
  } catch (error) {
    console.error('获取分类数据失败:', error)
    categoriesFromDB.value = []
  } finally {
    categoryLoading.value = false
  }
}

// 构建分类树 - 参考ArticleCategoryTree.vue的写法
const buildCategoryTree = computed(() => {
  const articlesToProcess = categoriesFromDB.value.length > 0
    ? categoriesFromDB.value.flatMap(cat => cat.articles.map(article => ({ ...article, category: cat.path })))
    : articles.value

  const root = []
  const map = new Map()

  articlesToProcess.forEach(article => {
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

  return root
})

// 使用computed属性
categoryTree.value = buildCategoryTree

// 获取文章列表
const fetchArticles = async () => {
  const res = await axios.get('/api/articles')
  articles.value = res.data
}

// 获取标签
const fetchTags = async () => {
  const res = await axios.get('/api/tags')
  allTags.value = res.data.tags || []
}

// 分类点击处理
const handleCategoryClick = (data) => {
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
  return arr
})

// 排序
const sortedArticles = computed(() => {
  const arr = [...filteredArticles.value]
  arr.sort((a, b) => {
    let v1 = a[sortKey.value]
    let v2 = b[sortKey.value]
    if (sortKey.value === 'date') {
      v1 = new Date(v1)
      v2 = new Date(v2)
    }
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
const openEditor = (mode, article = null) => {
  editorMode.value = mode
  currentArticle.value = article
  showEditor.value = true
}

const openUploadDialog = () => {
  showUploadDialog.value = true
}

const previewArticle = (article) => {
  previewingArticle.value = article
  showPreviewDialog.value = true
}

const deleteArticle = async (article) => {
  try {
    await ElMessageBox.confirm('确定要删除该文章吗？', '提示', { type: 'warning' })
    await axios.delete(`/api/articles/${article.id}`)
    ElMessage.success('删��成功')
    refreshArticles()
  } catch {}
}

const onEditorSave = () => {
  showEditor.value = false
  refreshArticles()
}

const refreshArticles = () => {
  fetchArticles()
  fetchTags()
  fetchCategories()
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
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  color: #333;
}

.filter-controls {
  padding: 10px 0;
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
  background: #f5f5f5;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
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
</style>
