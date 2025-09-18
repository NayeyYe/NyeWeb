<template>
  <el-dialog
      :before-close="handleClose"
      :close-on-click-modal="false"
      :model-value="modelValue"
      title="编辑文章"
      width="700px"
      @update:model-value="$emit('update:modelValue', $event)"
  >
    <el-form ref="formRef" :model="formData" :rules="formRules" label-width="100px">
      <!-- 重新上传文件 -->
      <el-form-item label="重新上传" prop="file">
        <el-upload
            ref="uploadRef"
            :auto-upload="false"
            :limit="1"
            :on-change="handleFileChange"
            :on-remove="handleFileRemove"
            :show-file-list="true"
            accept=".md,.markdown"
            class="upload-section"
        >
          <el-button :icon="UploadIcon" type="primary">重新选择Markdown文件</el-button>
          <template #tip>
            <div class="el-upload__tip">
              留空则保持原文件内容不变
            </div>
          </template>
        </el-upload>
      </el-form-item>

      <!-- 文章标题 -->
      <el-form-item label="文章标题" prop="title" required>
        <el-input
            v-model="formData.title"
            maxlength="255"
            placeholder="请输入文章标题"
            show-word-limit
        />
      </el-form-item>

      <!-- 分类文件夹选择 -->
      <el-form-item label="分类文件夹" prop="category">
        <div class="category-section">
          <el-card class="category-selector-card" shadow="never">
            <template #header>
              <div class="category-header">
                <span>选择分类文件夹</span>
                <div class="category-actions">
                  <el-button v-if="formData.category" class="clear-btn" link @click="clearCategorySelection">
                    清空选择
                  </el-button>
                  <el-button :loading="categoryLoading" link @click="refreshCategories">
                    <el-icon>
                      <RefreshIcon/>
                    </el-icon>
                    刷新
                  </el-button>
                </div>
              </div>
            </template>
            <div v-loading="categoryLoading" class="category-tree-container">
              <el-tree
                  v-if="!categoryLoading && categoryTree.length > 0"
                  ref="categoryTreeRef"
                  :current-node-key="formData.category"
                  :data="categoryTree"
                  :expand-on-click-node="false"
                  :highlight-current="true"
                  :props="treeProps"
                  class="category-tree"
                  default-expand-all
                  node-key="path"
                  @node-click="handleCategorySelect"
              >
                <template #default="{ node, data }">
                  <div class="tree-node-content">
                    <span class="tree-node-label">{{ node.label }}</span>
                  </div>
                </template>
              </el-tree>
              <div v-else-if="!categoryLoading" class="no-categories-tip">
                <el-text type="info">暂无分类文件夹</el-text>
              </div>
            </div>
          </el-card>
        </div>
        <div v-if="formData.category" class="selected-category">
          <el-icon>
            <Folder/>
          </el-icon>
          已选择: {{ formData.category }}
        </div>
      </el-form-item>

      <!-- 发布日期 -->
      <el-form-item label="发布日期" prop="date" required>
        <el-date-picker
            v-model="formData.date"
            format="YYYY-MM-DD"
            placeholder="选择发布日期"
            style="width: 100%"
            type="date"
            value-format="YYYY-MM-DD"
        />
      </el-form-item>

      <!-- 文章摘要 -->
      <el-form-item label="文章摘要" prop="summary">
        <el-input
            v-model="formData.summary"
            :rows="4"
            maxlength="500"
            placeholder="请输入文章摘要"
            show-word-limit
            type="textarea"
        />
      </el-form-item>

      <!-- 文章标签 -->
      <el-form-item label="文章标签">
        <el-select
            v-model="formData.tags"
            :multiple-limit="5"
            allow-create
            filterable
            multiple
            placeholder="选择或创建标签"
            style="width: 100%"
        >
          <el-option
              v-for="tag in existingTags"
              :key="tag"
              :label="tag"
              :value="tag"
          />
        </el-select>
        <div class="form-tip">最多可选择5个标签</div>
      </el-form-item>

      <!-- 文章状态 -->
      <el-form-item label="文章状态" prop="status" required>
        <el-radio-group v-model="formData.status">
          <el-radio value="draft">
            <el-icon>
              <Edit/>
            </el-icon>
            草稿
          </el-radio>
          <el-radio value="published">
            <el-icon>
              <Check/>
            </el-icon>
            发布
          </el-radio>
        </el-radio-group>
      </el-form-item>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button :loading="updating" type="primary" @click="handleUpdate">
          <el-icon>
            <Check/>
          </el-icon>
          更新文章
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import {onMounted, reactive, ref, watch} from 'vue'
import {ElMessage, ElMessageBox} from 'element-plus'
import {Check, Edit, Folder, Refresh as RefreshIcon, Upload as UploadIcon} from '@element-plus/icons-vue'
import axios from 'axios'

const props = defineProps({
  modelValue: Boolean,
  article: Object
})

const emit = defineEmits(['update:modelValue', 'update-success'])

const formData = reactive({
  title: '',
  category: '',
  date: '',
  summary: '',
  tags: [],
  status: 'draft',
  file: null,
  content: ''
})

const formRules = {
  title: [
    {required: true, message: '请输入文章标题', trigger: 'blur'},
    {min: 1, max: 255, message: '标题长度应在1-255个字符之间', trigger: 'blur'}
  ],
  date: [
    {required: true, message: '请选择发布日期', trigger: 'change'}
  ],
  status: [
    {required: true, message: '请选择文章状态', trigger: 'change'}
  ]
}

const formRef = ref(null)
const uploadRef = ref(null)
const categoryTreeRef = ref(null)
const categoryTree = ref([])
const existingTags = ref([])
const updating = ref(false)
const categoryLoading = ref(false)
const hasChanges = ref(false)

const treeProps = {
  children: 'children',
  label: 'label'
}

// 监听文章数据变化，初始化表单
watch(() => props.article, (newArticle) => {
  if (newArticle && props.modelValue) {
    initializeForm(newArticle)
  }
}, {immediate: true})

const initializeForm = (article) => {
  Object.assign(formData, {
    title: article.title || '',
    category: article.category || '',
    date: article.date || '',
    summary: article.summary || '',
    tags: Array.isArray(article.tags) ? [...article.tags] : [],
    status: article.status || 'draft',
    file: null,
    content: ''
  })
  hasChanges.value = false

  // 设置选中的分类
  if (categoryTreeRef.value && formData.category) {
    categoryTreeRef.value.setCurrentKey(formData.category)
  }
}

// 监听表单数据变化
watch(() => [formData.title, formData.category, formData.date, formData.summary, formData.tags, formData.status], () => {
  hasChanges.value = true
}, {deep: true})

const fetchCategories = async () => {
  categoryLoading.value = true
  try {
    const response = await axios.get('/api/articles/categories')
    if (response.data?.categories && Array.isArray(response.data.categories)) {
      categoryTree.value = buildCategoryTreeFromData(response.data.categories)
    } else {
      categoryTree.value = []
    }
  } catch (error) {
    console.error('获取分类失败:', error)
    categoryTree.value = []
  } finally {
    categoryLoading.value = false
  }
}

const buildCategoryTreeFromData = (categories) => {
  if (!categories || categories.length === 0) return []

  const nodeMap = new Map()
  const root = []
  const allPaths = new Set()

  categories.forEach(category => {
    if (!category.path) return
    const pathParts = category.path.split('/')
    let currentPath = ''
    pathParts.forEach((part) => {
      if (!part.trim()) return
      const parentPath = currentPath
      currentPath = currentPath ? `${currentPath}/${part}` : part
      allPaths.add(currentPath)
    })
  })

  const sortedPaths = Array.from(allPaths).sort((a, b) => {
    const aDepth = a.split('/').length
    const bDepth = b.split('/').length
    if (aDepth !== bDepth) return aDepth - bDepth
    return a.localeCompare(b)
  })

  sortedPaths.forEach(fullPath => {
    if (!nodeMap.has(fullPath)) {
      const pathParts = fullPath.split('/')
      const label = pathParts[pathParts.length - 1]
      const parentPath = pathParts.slice(0, -1).join('/')

      const node = {
        path: fullPath,
        label: label,
        children: []
      }

      nodeMap.set(fullPath, node)

      if (parentPath && nodeMap.has(parentPath)) {
        const parentNode = nodeMap.get(parentPath)
        if (!parentNode.children.find(child => child.path === fullPath)) {
          parentNode.children.push(node)
        }
      } else if (!parentPath) {
        if (!root.find(child => child.path === fullPath)) {
          root.push(node)
        }
      }
    }
  })

  return root
}

const fetchTags = async () => {
  try {
    const res = await axios.get('/api/tags')
    if (res.data?.tags && Array.isArray(res.data.tags)) {
      existingTags.value = res.data.tags
    } else {
      existingTags.value = []
    }
  } catch (error) {
    console.error('获取标签失败:', error)
    existingTags.value = []
  }
}

const refreshCategories = async () => {
  await fetchCategories()
}

const handleCategorySelect = (data) => {
  if (formData.category === data.path) {
    clearCategorySelection()
  } else {
    formData.category = data.path
  }
}

const clearCategorySelection = () => {
  formData.category = ''
  if (categoryTreeRef.value) {
    categoryTreeRef.value.setCurrentKey(null)
  }
}

const handleFileChange = (file) => {
  if (file && file.raw) {
    formData.file = file.raw
    hasChanges.value = true

    const reader = new FileReader()
    reader.onload = (e) => {
      formData.content = e.target.result
    }
    reader.onerror = () => {
      ElMessage.error('文件读取失败')
    }
    reader.readAsText(file.raw, 'utf-8')
  }
}

const handleFileRemove = () => {
  formData.file = null
  formData.content = ''
  hasChanges.value = true
}

const handleUpdate = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()

    updating.value = true

    const updateData = {
      title: formData.title,
      category: formData.category,
      date: formData.date,
      summary: formData.summary,
      tags: formData.tags,
      status: formData.status
    }

    // 如果有新文件，则包含内容
    if (formData.file && formData.content) {
      updateData.content = formData.content
    }

    // 首先尝试PUT方法
    let response
    try {
      response = await axios.put(`/api/articles/${props.article.id}`, updateData, {
        timeout: 30000,
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      })
    } catch (putError) {
      // 如果PUT方法不支持，尝试PATCH方法
      if (putError.response?.status === 405) {
        try {
          response = await axios.patch(`/api/articles/${props.article.id}`, updateData, {
            timeout: 30000,
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json'
            }
          })
        } catch (patchError) {
          // 如果PATCH也不支持，尝试POST到更新端点
          if (patchError.response?.status === 405) {
            response = await axios.post(`/api/articles/${props.article.id}/edit`, updateData, {
              timeout: 30000,
              headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
              }
            })
          } else {
            throw patchError
          }
        }
      } else {
        throw putError
      }
    }

    ElMessage.success('文章更新成功')
    hasChanges.value = false
    emit('update-success')
    emit('update:modelValue', false)
  } catch (error) {
    console.error('更新失败:', error)
    handleUpdateError(error)
  } finally {
    updating.value = false
  }
}

const handleUpdateError = (error) => {
  if (error.response?.status === 409) {
    ElMessage.error('文章标题已存在')
  } else if (error.response?.status === 400) {
    ElMessage.error(error.response.data?.detail || '请求参数错误')
  } else if (error.response?.status === 404) {
    ElMessage.error('文章不存在或已被删除')
  } else if (error.response?.status === 405) {
    ElMessage.error('编辑功能暂时不可用，请联系管理员')
  } else {
    ElMessage.error('更新失败: ' + (error.response?.data?.detail || error.message))
  }
}

const handleClose = () => {
  if (hasChanges.value) {
    ElMessageBox.confirm(
        '确定要关闭吗？未保存的修改将丢失。',
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
    ).then(() => {
      resetForm()
      emit('update:modelValue', false)
    }).catch(() => {
    })
  } else {
    resetForm()
    emit('update:modelValue', false)
  }
}

const resetForm = () => {
  if (uploadRef.value) {
    uploadRef.value.clearFiles()
  }
  if (formRef.value) {
    formRef.value.resetFields()
  }
  hasChanges.value = false
}

onMounted(() => {
  fetchCategories()
  fetchTags()
})
</script>

<style scoped>
.upload-section {
  width: 100%;
}

.category-section {
  width: 100%;
}

.category-selector-card {
  border: 1px solid #e1e8ed;
  border-radius: 8px;
  height: 280px;
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.category-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.clear-btn {
  color: #666 !important;
  font-weight: normal !important;
}

.clear-btn:hover {
  color: #409eff !important;
}

.category-tree-container {
  height: 200px;
  overflow-y: auto;
}

.category-tree {
  background: transparent;
}

.selected-category {
  color: #409eff;
  font-size: 12px;
  margin-top: 6px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.form-tip {
  color: #909399;
  font-size: 12px;
  margin-top: 4px;
}

.dialog-footer {
  text-align: right;
}

.tree-node-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding-right: 8px;
}

.tree-node-label {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.no-categories-tip {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #909399;
  font-size: 14px;
  text-align: center;
  padding: 20px;
}

:deep(.el-card__header) {
  padding: 12px 16px;
  background: #fafafa;
  border-bottom: 1px solid #ebeef5;
}

:deep(.el-card__body) {
  padding: 16px;
}

:deep(.el-tree-node__content) {
  padding: 8px 0;
  border-radius: 4px;
  position: relative;
}

:deep(.el-tree-node__content:hover) {
  background-color: #f5f7fa;
}

:deep(.el-tree .el-tree-node.is-current > .el-tree-node__content) {
  background-color: #e8f4fd;
  color: #409eff;
}
</style>
