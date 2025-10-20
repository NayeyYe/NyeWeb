<template>
  <div class="resource-management">
    <!-- Tab切换 -->
    <el-tabs v-model="activeTab" class="resource-tabs">
      <el-tab-pane label="图书管理" name="books">
        <!-- 图书操作栏 -->
        <div class="action-bar">
          <div class="action-buttons">
            <el-button type="primary" @click="showUploadBookDialog = true">上传图书</el-button>
            <el-button :icon="Refresh" circle @click="refreshBooks"/>
          </div>
        </div>

        <!-- 图书筛选区域 -->
        <div class="filter-section">
          <el-row :gutter="20">
            <el-col :span="24">
              <el-card class="filter-card" shadow="never">
                <template #header>
                  <div class="filter-header">
                    <span>筛选条件</span>
                    <el-button class="reset-link-btn" link @click="resetBookFilters">重置</el-button>
                  </div>
                </template>
                <div class="filter-controls">
                  <!-- 标签筛选独立一行 -->
                  <div class="filter-row tag-row">
                    <div class="filter-item">
                      <label>标签筛选：</label>
                      <el-select
                          v-model="bookFilterForm.tags"
                          :multiple-limit="3"
                          allow-create
                          filterable
                          multiple
                          placeholder="选择或输入标签（最多3个）"
                          size="default"
                          style="width: 350px"
                      >
                        <el-option
                            v-for="tag in allBookTags"
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
                          v-model="bookFilterForm.title"
                          clearable
                          placeholder="输入书籍标题关键字"
                          style="width: 250px"
                      />
                    </div>
                    <div class="filter-item">
                      <label>状态筛选：</label>
                      <el-select v-model="bookFilterForm.status" placeholder="选择状态" style="width: 140px">
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

        <!-- 图书列表 -->
        <div class="resource-list">
          <el-card shadow="never">
            <template #header>
              <div class="list-header">
                <span>图书列表</span>
                <span class="resource-count">共 {{ filteredBooks.length }} 本图书</span>
              </div>
            </template>
            <el-table
                :data="paginatedBooks"
                :header-cell-style="{ background: '#fafafa', color: '#333', fontWeight: '600' }"
                class="resource-table"
                empty-text="暂无图书数据"
                stripe
            >
              <el-table-column label="图书标题" min-width="200" prop="title" show-overflow-tooltip>
                <template #default="scope">
                  <div class="resource-title">{{ scope.row.title }}</div>
                </template>
              </el-table-column>
              <el-table-column label="文件名" min-width="150" prop="filename" show-overflow-tooltip>
                <template #default="scope">
                  <div class="resource-filename">{{ scope.row.filename || '暂无文件' }}</div>
                </template>
              </el-table-column>
              <el-table-column label="图书描述" min-width="200" prop="description" show-overflow-tooltip>
                <template #default="scope">
                  <div class="resource-description">{{ scope.row.description || '暂无描述' }}</div>
                </template>
              </el-table-column>
              <el-table-column label="标签" min-width="150" prop="tags" show-overflow-tooltip>
                <template #default="scope">
                  <div v-if="scope.row.tags && scope.row.tags.length > 0" class="resource-tags">
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
                      @change="(value) => updateBookStatus(scope.row, value)"
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
                    <el-button size="small" type="primary" @click="handleEditBook(scope.row)">编辑</el-button>
                    <el-button
                        v-if="scope.row.status !== 'recycled'"
                        size="small"
                        type="warning"
                        @click="quickUpdateBookStatus(scope.row, 'recycled')"
                    >
                      回收
                    </el-button>
                    <el-button
                        v-if="scope.row.status === 'recycled'"
                        size="small"
                        type="success"
                        @click="quickUpdateBookStatus(scope.row, 'published')"
                    >
                      恢复
                    </el-button>
                    <el-button size="small" type="danger" @click="deleteBook(scope.row)">删除</el-button>
                  </div>
                </template>
              </el-table-column>
            </el-table>
            
            <!-- 添加图书分页组件 -->
            <div v-if="filteredBooks.length > pageSize" class="pagination-wrapper">
              <el-pagination
                  v-model:current-page="bookCurrentPage"
                  :page-size="pageSize"
                  :total="filteredBooks.length"
                  background
                  layout="prev, pager, next, jumper, total"
                  @current-change="handleBookPageChange"
              />
            </div>
          </el-card>
        </div>
      </el-tab-pane>

      <el-tab-pane label="图片管理" name="figures">
        <!-- 图片操作栏 -->
        <div class="action-bar">
          <div class="action-buttons">
            <el-button type="primary" @click="showUploadFigureDialog = true">上传图片</el-button>
            <el-button :icon="Refresh" circle @click="refreshFigures"/>
          </div>
        </div>

        <!-- 图片筛选区域 -->
        <div class="filter-section">
          <el-row :gutter="20">
            <el-col :span="24">
              <el-card class="filter-card" shadow="never">
                <template #header>
                  <div class="filter-header">
                    <span>筛选条件</span>
                    <el-button class="reset-link-btn" link @click="resetFigureFilters">重置</el-button>
                  </div>
                </template>
                <div class="filter-controls">
                  <!-- 标签筛选独立一行 -->
                  <div class="filter-row tag-row">
                    <div class="filter-item">
                      <label>标签筛选：</label>
                      <el-select
                          v-model="figureFilterForm.tags"
                          :multiple-limit="3"
                          allow-create
                          filterable
                          multiple
                          placeholder="选择或输入标签（最多3个）"
                          size="default"
                          style="width: 350px"
                      >
                        <el-option
                            v-for="tag in allFigureTags"
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
                          v-model="figureFilterForm.title"
                          clearable
                          placeholder="输入图片标题关键字"
                          style="width: 250px"
                      />
                    </div>
                    <div class="filter-item">
                      <label>状态筛选：</label>
                      <el-select v-model="figureFilterForm.status" placeholder="选择状态" style="width: 140px">
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

        <!-- 图片列表 -->
        <div class="resource-list">
          <el-card shadow="never">
            <template #header>
              <div class="list-header">
                <span>图片列表</span>
                <span class="resource-count">共 {{ filteredFigures.length }} 张图片</span>
              </div>
            </template>
            <el-table
                :data="paginatedFigures"
                :header-cell-style="{ background: '#fafafa', color: '#333', fontWeight: '600' }"
                class="resource-table"
                empty-text="暂无图片数据"
                stripe
            >
              <el-table-column label="图片标题" min-width="200" prop="title" show-overflow-tooltip>
                <template #default="scope">
                  <div class="resource-title">{{ scope.row.title }}</div>
                </template>
              </el-table-column>
              <el-table-column label="图床链接" min-width="200" prop="url" show-overflow-tooltip>
                <template #default="scope">
                  <div class="resource-filename">{{ scope.row.url || '暂无链接' }}</div>
                </template>
              </el-table-column>
              <el-table-column label="图片描述" min-width="200" prop="description" show-overflow-tooltip>
                <template #default="scope">
                  <div class="resource-description">{{ scope.row.description || '暂无描述' }}</div>
                </template>
              </el-table-column>
              <el-table-column label="标签" min-width="150" prop="tags" show-overflow-tooltip>
                <template #default="scope">
                  <div v-if="scope.row.tags && scope.row.tags.length > 0" class="resource-tags">
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
                      @change="(value) => updateFigureStatus(scope.row, value)"
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
                    <el-button size="small" type="primary" @click="handleEditFigure(scope.row)">编辑</el-button>
                    <el-button
                        v-if="scope.row.status !== 'recycled'"
                        size="small"
                        type="warning"
                        @click="quickUpdateFigureStatus(scope.row, 'recycled')"
                    >
                      回收
                    </el-button>
                    <el-button
                        v-if="scope.row.status === 'recycled'"
                        size="small"
                        type="success"
                        @click="quickUpdateFigureStatus(scope.row, 'published')"
                    >
                      恢复
                    </el-button>
                    <el-button size="small" type="danger" @click="deleteFigure(scope.row)">删除</el-button>
                  </div>
                </template>
              </el-table-column>
            </el-table>
            
            <!-- 添加图片分页组件 -->
            <div v-if="filteredFigures.length > pageSize" class="pagination-wrapper">
              <el-pagination
                  v-model:current-page="figureCurrentPage"
                  :page-size="pageSize"
                  :total="filteredFigures.length"
                  background
                  layout="prev, pager, next, jumper, total"
                  @current-change="handleFigurePageChange"
              />
            </div>
          </el-card>
        </div>
      </el-tab-pane>
    </el-tabs>

    <!-- 图书上传对话框 -->
    <UploadBookDialog
        v-model="showUploadBookDialog"
        @upload-success="handleBookUploadSuccess"
    />

    <!-- 图书编辑对话框 -->
    <EditBookDialog
        v-model="showEditBookDialog"
        :book="currentEditBook"
        @save-success="handleBookEditSuccess"
    />

    <!-- 图片上传对话框 -->
    <UploadFigureDialog
        v-model="showUploadFigureDialog"
        @upload-success="handleFigureUploadSuccess"
    />

    <!-- 图片编辑对话框 -->
    <EditFigureDialog
        v-model="showEditFigureDialog"
        :figure="currentEditFigure"
        @save-success="handleFigureEditSuccess"
    />
  </div>
</template>

<script setup>
import {computed, onMounted, reactive, ref, watch} from 'vue'
import {ElMessage, ElMessageBox} from 'element-plus'
import {Refresh} from '@element-plus/icons-vue'
import axios from 'axios'
import UploadBookDialog from '@/components/Admin/ResourceManagement/UploadBookDialog.vue'
import EditBookDialog from '@/components/Admin/ResourceManagement/EditBookDialog.vue'
import UploadFigureDialog from '@/components/Admin/ResourceManagement/UploadFigureDialog.vue'
import EditFigureDialog from '@/components/Admin/ResourceManagement/EditFigureDialog.vue'

const activeTab = ref('books')
const books = ref([])
const figures = ref([])
const allBookTags = ref([])
const allFigureTags = ref([])
const showUploadBookDialog = ref(false)
const showEditBookDialog = ref(false)
const currentEditBook = ref(null)
const showUploadFigureDialog = ref(false)
const showEditFigureDialog = ref(false)
const currentEditFigure = ref(null)

const bookFilterForm = reactive({
  tags: [],
  title: '',
  status: ''
})

const figureFilterForm = reactive({
  tags: [],
  title: '',
  status: ''
})

// 添加分页状态
const bookCurrentPage = ref(1)
const figureCurrentPage = ref(1)
const pageSize = ref(10)

// 获取图书列表(管理员接口，包含所有状态)
const fetchBooks = async () => {
  try {
    const res = await axios.get('/api/admin/books')
    books.value = res.data
  } catch (error) {
    console.error('获取图书列表失败:', error)
    ElMessage.error('获取图书列表失败')
  }
}

// 获取图片列表(管理员接口，包含所有状态)
const fetchFigures = async () => {
  try {
    const res = await axios.get('/api/admin/figures')
    figures.value = res.data
  } catch (error) {
    console.error('获取图片列表失败:', error)
    ElMessage.error('获取图片列表失败')
  }
}

// 获取图书标签
const fetchBookTags = async () => {
  try {
    const res = await axios.get('/api/book-tags')
    allBookTags.value = res.data.tags || []
  } catch (error) {
    console.error('获取图书标签失败:', error)
  }
}

// 获取图片标签
const fetchFigureTags = async () => {
  try {
    const res = await axios.get('/api/figure-tags')
    allFigureTags.value = res.data.tags || []
  } catch (error) {
    console.error('获取图片标签失败:', error)
  }
}

// 图书筛选
const filteredBooks = computed(() => {
  let arr = books.value
  if (bookFilterForm.tags && bookFilterForm.tags.length) {
    arr = arr.filter(b => b.tags && bookFilterForm.tags.every(tag => b.tags.includes(tag)))
  }
  if (bookFilterForm.title) {
    arr = arr.filter(b => b.title && b.title.includes(bookFilterForm.title))
  }
  if (bookFilterForm.status) {
    arr = arr.filter(b => b.status === bookFilterForm.status)
  }
  return arr
})

// 添加图书分页计算属性
const paginatedBooks = computed(() => {
  const start = (bookCurrentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredBooks.value.slice(start, end)
})

// 图片筛选
const filteredFigures = computed(() => {
  let arr = figures.value
  if (figureFilterForm.tags && figureFilterForm.tags.length) {
    arr = arr.filter(f => f.tags && figureFilterForm.tags.every(tag => f.tags.includes(tag)))
  }
  if (figureFilterForm.title) {
    arr = arr.filter(f => f.title && f.title.includes(figureFilterForm.title))
  }
  if (figureFilterForm.status) {
    arr = arr.filter(f => f.status === figureFilterForm.status)
  }
  return arr
})

// 添加图片分页计算属性
const paginatedFigures = computed(() => {
  const start = (figureCurrentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredFigures.value.slice(start, end)
})

// 筛选操作
const resetBookFilters = () => {
  bookFilterForm.tags = []
  bookFilterForm.title = ''
  bookFilterForm.status = ''
  bookCurrentPage.value = 1
}

const resetFigureFilters = () => {
  figureFilterForm.tags = []
  figureFilterForm.title = ''
  figureFilterForm.status = ''
  figureCurrentPage.value = 1
}

// 添加分页处理函数
const handleBookPageChange = (page) => {
  bookCurrentPage.value = page
}

const handleFigurePageChange = (page) => {
  figureCurrentPage.value = page
}

// 监听筛选变化，重置到第一页
watch([() => bookFilterForm.tags, () => bookFilterForm.title, () => bookFilterForm.status], () => {
  bookCurrentPage.value = 1
}, { deep: true })

watch([() => figureFilterForm.tags, () => figureFilterForm.title, () => figureFilterForm.status], () => {
  figureCurrentPage.value = 1
}, { deep: true })

// 图书操作
const handleUploadBook = () => {
  showUploadBookDialog.value = true
}

const handleBookUploadSuccess = () => {
  refreshBooks()
}

const handleEditBook = (book) => {
  console.log('编辑图书:', book)
  currentEditBook.value = book
  showEditBookDialog.value = true
}

const handleBookEditSuccess = () => {
  refreshBooks()
}

const deleteBook = async (book) => {
  try {
    await ElMessageBox.confirm('确定要删除该图书吗？', '提示', {type: 'warning'})
    await axios.delete(`/api/books/${book.id}`)
    ElMessage.success('图书删除成功')
    refreshBooks()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除图书失败:', error)
      ElMessage.error('删除图书失败')
    }
  }
}

const refreshBooks = async () => {
  await fetchBooks()
  await fetchBookTags()
}

// 图片操作
const handleUploadFigure = () => {
  showUploadFigureDialog.value = true
}

const handleFigureUploadSuccess = () => {
  refreshFigures()
}

const handleEditFigure = (figure) => {
  console.log('编辑图片:', figure)
  currentEditFigure.value = figure
  showEditFigureDialog.value = true
}

const handleFigureEditSuccess = () => {
  refreshFigures()
}

const deleteFigure = async (figure) => {
  try {
    await ElMessageBox.confirm('确定要删除该图片吗？', '提示', {type: 'warning'})
    await axios.delete(`/api/figures/${figure.id}`)
    ElMessage.success('图片删除成功')
    refreshFigures()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除图片失败:', error)
      ElMessage.error('删除图片失败')
    }
  }
}

const refreshFigures = async () => {
  await fetchFigures()
  await fetchFigureTags()
}

// 更新图书状态
const updateBookStatus = async (book, newStatus) => {
  if (book.status === newStatus) return

  try {
    await axios.patch(`/api/books/${book.id}/status`, {status: newStatus})
    book.status = newStatus
    const statusText = getStatusText(newStatus)
    ElMessage.success(`图书状态已更新为：${statusText}`)
  } catch (error) {
    console.error('更新图书状态失败:', error)
    ElMessage.error('更新图书状态失败')
    refreshBooks()
  }
}

const quickUpdateBookStatus = async (book, newStatus) => {
  const actionText = newStatus === 'recycled' ? '回收' : '恢复'
  try {
    await ElMessageBox.confirm(`确定要${actionText}该图书吗？`, '提示', {type: 'warning'})
    await updateBookStatus(book, newStatus)
  } catch (error) {
    if (error !== 'cancel') {
      console.error(`${actionText}图书失败:`, error)
    }
  }
}

// 更新图片状态
const updateFigureStatus = async (figure, newStatus) => {
  if (figure.status === newStatus) return

  try {
    await axios.patch(`/api/figures/${figure.id}/status`, {status: newStatus})
    figure.status = newStatus
    const statusText = getStatusText(newStatus)
    ElMessage.success(`图片状态已更新为：${statusText}`)
  } catch (error) {
    console.error('更新图片状态失败:', error)
    ElMessage.error('更新图片状态失败')
    refreshFigures()
  }
}

const quickUpdateFigureStatus = async (figure, newStatus) => {
  const actionText = newStatus === 'recycled' ? '回收' : '恢复'
  try {
    await ElMessageBox.confirm(`确定要${actionText}该图片吗？`, '提示', {type: 'warning'})
    await updateFigureStatus(figure, newStatus)
  } catch (error) {
    if (error !== 'cancel') {
      console.error(`${actionText}图片失败:`, error)
    }
  }
}

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
  refreshBooks()
  refreshFigures()
})
</script>

<style scoped>
.resource-management {
  padding: 20px;
  background: #f8f9fa;
  min-height: 100vh;
}

.resource-tabs {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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

.resource-list .filter-card {
  border: 1px solid #e1e8ed;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  color: #333;
}

.resource-count {
  color: #666;
  font-size: 14px;
  font-weight: normal;
}

.resource-table {
  border-radius: 8px;
  overflow: hidden;
}

.resource-title {
  font-weight: 500;
  color: #333;
}

.resource-filename {
  font-family: 'Monaco', 'Consolas', monospace;
  color: #666;
  font-size: 13px;
}

.resource-description {
  color: #666;
  font-size: 14px;
}

.resource-tags {
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

:deep(.el-tabs__header) {
  margin-bottom: 20px;
}

:deep(.el-tabs__nav-wrap::after) {
  height: 1px;
}

:deep(.el-tabs__item) {
  font-size: 16px;
  font-weight: 500;
  padding: 0 30px;
}

/* 状态下拉框样式 */:deep(.el-select .el-input__inner) {
  text-align: center;
  padding: 0 8px;
}:deep(.el-select--small .el-input__inner) {
  height: 28px;
  line-height: 28px;
}

/* 分页样式 */
.pagination-wrapper {
  display: flex;
  justify-content: center;
  padding: 20px 0;
  border-top: 1px solid #ebeef5;
  margin-top: 20px;
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
  .resource-management {
    padding: 15px;
  }
  
  .resource-tabs {
    padding: 15px;
  }
  
  .action-bar {
    margin-bottom: 15px;
  }
  
  .filter-section {
    margin-bottom: 15px;
  }
  
  .filter-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .filter-item {
    width: 100%;
  }
  
  .filter-item label {
    min-width: 60px;
  }
  
  .action-buttons {
    flex-wrap: wrap;
  }
  
  .list-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .resource-count {
    align-self: flex-end;
  }
}

@media (max-width: 480px) {
  .resource-management {
    padding: 10px;
  }
  
  .resource-tabs {
    padding: 10px;
  }
  
  .action-bar {
    margin-bottom: 10px;
  }
  
  .filter-section {
    margin-bottom: 10px;
  }
  
  .tag-row {
    margin-bottom: 15px;
  }
  
  .filter-row {
    margin-bottom: 12px;
  }
  
  .filter-item label {
    min-width: 50px;
    font-size: 13px;
  }
  
  :deep(.el-tabs__item) {
    font-size: 14px;
    padding: 0 15px;
  }
  
  :deep(.el-card__header) {
    padding: 12px 15px;
  }
  
  :deep(.el-card__body) {
    padding: 15px;
  }
}
</style>