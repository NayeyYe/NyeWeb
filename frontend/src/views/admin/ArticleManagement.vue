<template>
  <div class="management-panel">
    <div class="panel-header">
      <h2>文章管理</h2>
      <p>管理知识分享文章，包括技术文档、学习笔记、经验分享等内容。</p>
    </div>

    <!-- 工具栏 -->
    <div class="toolbar">
      <div class="toolbar-left">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索文章标题或内容..."
          style="width: 300px"
          clearable
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-select v-model="selectedCategory" placeholder="选择分类" clearable style="width: 200px;">
          <el-option label="全部分类" value="" />
          <el-option
            v-for="category in categories"
            :key="category"
            :label="category"
            :value="category"
          />
        </el-select>
        <el-select v-model="sortBy" style="width: 150px;">
          <el-option label="创建时间" value="date" />
          <el-option label="标题" value="title" />
          <el-option label="分类" value="category" />
        </el-select>
        <el-select v-model="sortOrder" style="width: 100px;">
          <el-option label="降序" value="desc" />
          <el-option label="升序" value="asc" />
        </el-select>
      </div>
      <div class="toolbar-right">
        <el-button type="primary" @click="showCreateDialog = true">
          <el-icon><Plus /></el-icon>
          新建文章
        </el-button>
        <el-button @click="showUploadDialog = true">
          <el-icon><Upload /></el-icon>
          上传文章
        </el-button>
        <el-button @click="refreshArticles">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>
    </div>

    <!-- 文章列表 -->
    <div class="panel-content">
      <el-card class="content-card">
        <div v-loading="loading" class="articles-container">
          <div v-if="!loading && filteredAndSortedArticles.length === 0" class="no-articles">
            <el-empty description="暂无文章数据">
              <el-button type="primary" @click="refreshArticles">刷新数据</el-button>
            </el-empty>
          </div>
          <div v-else class="articles-table">
            <el-table :data="displayedArticles" stripe>
              <el-table-column prop="title" label="标题" min-width="200">
                <template #default="{ row }">
                  <div class="article-title-cell">
                    <span class="title-text">{{ row.title }}</span>
                    <div class="article-meta">
                      <el-tag v-if="row.category" size="small" type="info">{{ row.category }}</el-tag>
                      <span class="slug-text">{{ row.slug }}</span>
                    </div>
                  </div>
                </template>
              </el-table-column>

              <el-table-column prop="summary" label="摘要" min-width="250" show-overflow-tooltip>
                <template #default="{ row }">
                  <p class="summary-text">{{ row.summary || '暂无摘要' }}</p>
                </template>
              </el-table-column>

              <el-table-column prop="date" label="发布日期" width="120" sortable>
                <template #default="{ row }">
                  <span>{{ row.date || '未设置' }}</span>
                </template>
              </el-table-column>

              <el-table-column prop="tags" label="标签" width="150">
                <template #default="{ row }">
                  <div class="tags-cell">
                    <el-tag
                      v-for="tag in row.tags?.slice(0, 2)"
                      :key="tag"
                      size="small"
                      class="tag-item"
                    >
                      {{ tag }}
                    </el-tag>
                    <span v-if="row.tags?.length > 2" class="more-tags">+{{ row.tags.length - 2 }}</span>
                  </div>
                </template>
              </el-table-column>

              <el-table-column label="操作" width="200" fixed="right">
                <template #default="{ row }">
                  <el-button-group size="small">
                    <el-button type="primary" @click="previewArticle(row)">
                      <el-icon><View /></el-icon>
                      预览
                    </el-button>
                    <el-button type="warning" @click="editArticle(row)">
                      <el-icon><Edit /></el-icon>
                      编辑
                    </el-button>
                    <el-button type="danger" @click="deleteArticle(row)">
                      <el-icon><Delete /></el-icon>
                      删除
                    </el-button>
                  </el-button-group>
                </template>
              </el-table-column>
            </el-table>

            <!-- 分页 -->
            <div class="pagination-container">
              <el-pagination
                v-model:current-page="currentPage"
                v-model:page-size="pageSize"
                :page-sizes="[10, 20, 50, 100]"
                :total="filteredAndSortedArticles.length"
                layout="total, sizes, prev, pager, next, jumper"
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
              />
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 回收站功能占位 -->
    <div class="recycle-bin">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>回收站功能</span>
            <el-badge :value="0" class="item">
              <el-button size="small" disabled>
                <el-icon><Delete /></el-icon>
                回收站 (待开发)
              </el-button>
            </el-badge>
          </div>
        </template>
        <p class="feature-placeholder">
          回收站功能正在开发中，将支持已删除文章的恢复操作。
        </p>
      </el-card>
    </div>

    <!-- 文章编辑器对话框 -->
    <ArticleEditor
      v-model="showCreateDialog"
      :article="currentArticle"
      :mode="editorMode"
      @save="handleArticleSave"
      @close="handleEditorClose"
    />

    <!-- 文章上传对话框 -->
    <UploadArticleDialog
      v-model="showUploadDialog"
      @upload-success="handleUploadSuccess"
    />

    <!-- 文章预览对话框 -->
    <ArticlePreviewDialog
      v-model="showPreviewDialog"
      :article="previewArticleData"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Plus, Upload, Refresh, View, Edit, Delete } from '@element-plus/icons-vue'
import axios from 'axios'
import ArticleEditor from '@/components/Admin/ArticleEditor.vue'
import UploadArticleDialog from '@/components/Admin/UploadArticleDialog.vue'
import ArticlePreviewDialog from '@/components/Admin/ArticlePreviewDialog.vue'

// 响应式数据
const articles = ref([])
const categories = ref([])
const loading = ref(false)
const searchKeyword = ref('')
const selectedCategory = ref('')
const sortBy = ref('date')
const sortOrder = ref('desc')
const currentPage = ref(1)
const pageSize = ref(20)

// 对话框控制
const showCreateDialog = ref(false)
const showUploadDialog = ref(false)
const showPreviewDialog = ref(false)
const currentArticle = ref(null)
const editorMode = ref('create')
const previewArticleData = ref(null)

// 计算属性 - 过滤和排序的文章
const filteredAndSortedArticles = computed(() => {
  let filtered = articles.value

  // 关键词搜索
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    filtered = filtered.filter(article =>
      article.title.toLowerCase().includes(keyword) ||
      article.summary?.toLowerCase().includes(keyword) ||
      article.category?.toLowerCase().includes(keyword)
    )
  }

  // 分类过滤
  if (selectedCategory.value) {
    filtered = filtered.filter(article => article.category === selectedCategory.value)
  }

  // 排序
  filtered.sort((a, b) => {
    let aValue = a[sortBy.value] || ''
    let bValue = b[sortBy.value] || ''

    if (sortBy.value === 'date') {
      aValue = new Date(aValue || 0)
      bValue = new Date(bValue || 0)
    } else {
      aValue = aValue.toString().toLowerCase()
      bValue = bValue.toString().toLowerCase()
    }

    if (sortOrder.value === 'asc') {
      return aValue > bValue ? 1 : -1
    } else {
      return aValue < bValue ? 1 : -1
    }
  })

  return filtered
})

// 计算属性 - 当前页显示的文章
const displayedArticles = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredAndSortedArticles.value.slice(start, end)
})

// 获取文章列表
const fetchArticles = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/articles')
    articles.value = response.data || []

    // 提取分类
    const categorySet = new Set()
    articles.value.forEach(article => {
      if (article.category) {
        categorySet.add(article.category)
      }
    })
    categories.value = Array.from(categorySet)

    console.log(`成功获取 ${articles.value.length} 篇文章`)
  } catch (error) {
    console.error('获取文章列表失败:', error)
    ElMessage.error('获取文章列表失败')
  } finally {
    loading.value = false
  }
}

// 刷新文章列表
const refreshArticles = () => {
  fetchArticles()
}

// 预览文章
const previewArticle = (article) => {
  previewArticleData.value = article
  showPreviewDialog.value = true
}

// 编辑文章
const editArticle = (article) => {
  currentArticle.value = { ...article }
  editorMode.value = 'edit'
  showCreateDialog.value = true
}

// 删除文章
const deleteArticle = async (article) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除文章 "${article.title}" 吗？`,
      '删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )

    await axios.delete(`/api/articles/${article.id}`)
    ElMessage.success('文章删除成功')
    fetchArticles()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除文章失败:', error)
      ElMessage.error('删除文章失败')
    }
  }
}

// 处理文章保存
const handleArticleSave = () => {
  showCreateDialog.value = false
  fetchArticles()
}

// 处理编辑器关闭
const handleEditorClose = () => {
  showCreateDialog.value = false
  currentArticle.value = null
  editorMode.value = 'create'
}

// 处理文章上传成功
const handleUploadSuccess = () => {
  showUploadDialog.value = false
  fetchArticles()
}

// 分页处理
const handleSizeChange = (val) => {
  pageSize.value = val
  currentPage.value = 1
}

const handleCurrentChange = (val) => {
  currentPage.value = val
}

// 组件挂载
onMounted(() => {
  fetchArticles()
})
</script>

<style scoped>
.management-panel {
  padding: 20px;
}

.panel-header {
  margin-bottom: 20px;
}

.panel-header h2 {
  margin: 0 0 8px 0;
  color: #303133;
  font-size: 24px;
}

.panel-header p {
  margin: 0;
  color: #606266;
  font-size: 14px;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 10px;
}

.toolbar-left {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.toolbar-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.panel-content {
  margin-bottom: 20px;
}

.content-card {
  border-radius: 12px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.articles-container {
  min-height: 400px;
}

.no-articles {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.article-title-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.title-text {
  font-weight: 600;
  color: #303133;
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.slug-text {
  font-size: 12px;
  color: #909399;
  font-family: monospace;
}

.summary-text {
  margin: 0;
  font-size: 13px;
  color: #606266;
  line-height: 1.4;
}

.tags-cell {
  display: flex;
  align-items: center;
  gap: 4px;
  flex-wrap: wrap;
}

.tag-item {
  margin: 1px 0;
}

.more-tags {
  font-size: 12px;
  color: #909399;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.recycle-bin {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.feature-placeholder {
  color: #909399;
  font-size: 14px;
  text-align: center;
  margin: 20px 0;
}

:deep(.el-table) {
  border-radius: 8px;
  overflow: hidden;
}

:deep(.el-table th) {
  background-color: #fafafa;
  color: #606266;
  font-weight: 600;
}

:deep(.el-button-group .el-button) {
  margin: 0;
}

@media (max-width: 768px) {
  .toolbar {
    flex-direction: column;
    align-items: stretch;
  }

  .toolbar-left,
  .toolbar-right {
    justify-content: center;
  }

  :deep(.el-table) {
    font-size: 12px;
  }
}
</style>
