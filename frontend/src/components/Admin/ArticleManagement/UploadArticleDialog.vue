<template>
  <el-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    title="上传文章"
    width="700px"
    :before-close="handleClose"
    :close-on-click-modal="false"
  >
    <el-form :model="formData" :rules="formRules" label-width="100px" ref="formRef">
      <!-- 文件上传 -->
      <el-form-item label="选择文件" prop="file" required>
        <el-upload
          ref="uploadRef"
          :auto-upload="false"
          :show-file-list="true"
          :on-change="handleFileChange"
          :on-remove="handleFileRemove"
          accept=".md,.markdown"
          :limit="1"
          class="upload-section"
        >
          <el-button type="primary" :icon="UploadIcon">选择Markdown文件</el-button>
          <template #tip>
            <div class="el-upload__tip">
              只能上传 .md 或 .markdown 文件
            </div>
          </template>
        </el-upload>
      </el-form-item>

      <!-- 文章标题 -->
      <el-form-item label="文章标题" prop="title" required>
        <el-input
          v-model="formData.title"
          placeholder="请输入文章标题"
          maxlength="255"
          show-word-limit
        />
      </el-form-item>

      <!-- 分类文件夹�������择 -->
      <el-form-item label="分类文件夹" prop="category">
        <div class="category-section">
          <el-card class="category-selector-card" shadow="never">
            <template #header>
              <div class="category-header">
                <span>选择分类文件夹</span>
                <div class="category-actions">
                  <el-button link @click="clearCategorySelection" v-if="formData.category" class="clear-btn">
                    清空选择
                  </el-button>
                  <el-button link @click="refreshCategories" :loading="categoryLoading">
                    <el-icon><RefreshIcon /></el-icon>
                    刷新
                  </el-button>
                  <el-button @click="showDevelopingMessage" size="small" type="success" disabled>
                    新建文件夹
                    <el-text type="warning" size="small" style="margin-left: 8px;">(待开发)</el-text>
                  </el-button>
                </div>
              </div>
            </template>
            <div v-loading="categoryLoading" class="category-tree-container">
              <el-tree
                v-if="!categoryLoading && categoryTree.length > 0"
                :data="categoryTree"
                :props="treeProps"
                @node-click="handleCategorySelect"
                :highlight-current="true"
                :expand-on-click-node="false"
                node-key="path"
                ref="categoryTreeRef"
                class="category-tree"
                :current-node-key="formData.category"
                default-expand-all
              />
              <el-empty 
                v-else-if="!categoryLoading && categoryTree.length === 0" 
                description="暂无分类文件夹，请先在系统中创建"
                :image-size="60"
              >
                <el-button @click="showDevelopingMessage" type="primary" disabled>
                  创建分类功能开发中
                </el-button>
              </el-empty>
            </div>
          </el-card>
        </div>
        <div class="form-tip">请选择已存在的分类文件夹</div>
        <div v-if="formData.category" class="selected-category">
          <el-icon><Folder /></el-icon>
          已选择: {{ formData.category }}
        </div>
      </el-form-item>

      <!-- 发布日期 -->
      <el-form-item label="发布日期" prop="date" required>
        <el-date-picker
          v-model="formData.date"
          type="date"
          placeholder="选择发布日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          style="width: 100%"
        />
      </el-form-item>

      <!-- 文章摘要 -->
      <el-form-item label="文章摘要" prop="summary">
        <el-input
          v-model="formData.summary"
          type="textarea"
          :rows="4"
          placeholder="请输入文章摘要，或使用AI生成"
          maxlength="500"
          show-word-limit
        />
        <div class="summary-actions">
          <el-button 
            size="small" 
            @click="generateSummary" 
            :loading="summaryLoading"
            :disabled="!formData.content"
            type="primary"
          >
            <el-icon><MagicStick /></el-icon>
            AI生成摘要
          </el-button>
        </div>
      </el-form-item>

      <!-- 文章标签 -->
      <el-form-item label="文章标签">
        <el-select
          v-model="formData.tags"
          multiple
          filterable
          allow-create
          placeholder="选择或创建标签"
          style="width: 100%"
          :multiple-limit="5"
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
            <el-icon><Edit /></el-icon>
            草稿
          </el-radio>
          <el-radio value="published">
            <el-icon><Check /></el-icon>
            发布
          </el-radio>
        </el-radio-group>
      </el-form-item>
    </el-form>

    <!-- 主对话框底部按钮 -->
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" @click="handleUpload" :loading="uploading">
          <el-icon><Upload /></el-icon>
          上传文章
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { onMounted, reactive, ref, watch, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Upload, 
  Edit, 
  Check, 
  MagicStick, 
  Upload as UploadIcon, 
  Refresh as RefreshIcon,
  Folder
} from '@element-plus/icons-vue'
import axios from 'axios'

// Props和Emits
const props = defineProps({
  modelValue: Boolean
})

const emit = defineEmits(['update:modelValue', 'upload-success'])

// 响应式数据
const formData = reactive({
  title: '',
  category: '',
  date: new Date().toISOString().split('T')[0],
  summary: '',
  tags: [],
  status: 'draft',
  file: null,
  content: ''
})

// 表单验证规则
const formRules = {
  title: [
    { required: true, message: '请输入文章标题', trigger: 'blur' },
    { min: 1, max: 255, message: '标题长度应在1-255个字符之间', trigger: 'blur' }
  ],
  date: [
    { required: true, message: '请选择发布日期', trigger: 'change' }
  ],
  status: [
    { required: true, message: '请选择文章状态', trigger: 'change' }
  ],
  file: [
    { required: true, message: '请选择要上传的文件', trigger: 'change' }
  ]
}

// 引用
const formRef = ref(null)
const uploadRef = ref(null)
const categoryTreeRef = ref(null)

// 状态数据
const categoryTree = ref([])
const existingTags = ref([])
const showCreateCategory = ref(false)
const uploading = ref(false)
const summaryLoading = ref(false)
const categoryLoading = ref(false)

// 树形控件配置
const treeProps = {
  children: 'children',
  label: 'label'
}

// 计算预览路径
const previewPath = computed(() => {
  let path = ''
  
  if (newCategory.parent) {
    path = newCategory.parent
  }
  
  if (newCategory.name) {
    const safeName = newCategory.name.trim()
    path = path ? `${path}/${safeName}` : safeName
  }
  
  return path || '根目录'
})

const previewPathTip = computed(() => {
  if (!previewPath.value || previewPath.value === '根目录') {
    return '文件夹将创建在根目录下'
  }
  return `文件夹路径: articles/knowledge/${previewPath.value}`
})

// 分类操作
const handleCategorySelect = (data) => {
  console.log('选择分类:', data)
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

// 显示待开发提示
const showDevelopingMessage = () => {
  ElMessage.info('该功能正在开发中，敬请期待！')
}

// 获取分类数据 - 使用API
const fetchCategories = async () => {
  categoryLoading.value = true
  try {
    console.log('开始获取分类数据...')

    const response = await axios.get('/api/articles/categories', {
      timeout: 10000,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })

    console.log('分类数据响应:', response.data)
    
    if (response.data?.categories && Array.isArray(response.data.categories)) {
      // 使用与ArticleManagement相同的方式构建分类树
      categoryTree.value = buildCategoryTreeFromData(response.data.categories)
      console.log('构建的分类树:', categoryTree.value)
    } else {
      console.warn('分类数据格式异常或为空:', response.data)
      categoryTree.value = []
    }
  } catch (error) {
    console.error('获取分类失败详情:', {
      message: error.message,
      status: error.response?.status,
      statusText: error.response?.statusText,
      data: error.response?.data,
      url: error.config?.url
    })
    
    if (error.code === 'NETWORK_ERROR' || error.message === 'Network Error') {
      console.error('网络连接错误，请检查服务器状态')
      ElMessage.error('无法连接到服务器，请检查网络连接和服务器状态')
    } else if (error.response?.status === 404) {
      console.warn('分类API接口不存在')
      ElMessage.warning('分类接��暂不可用，请联系管理员')
    } else if (error.response?.status >= 500) {
      console.error('服务器内部错误:', error.response.data)
      ElMessage.error('服务器错误，请稍后重试')
    } else {
      console.error('其他错误:', error)
      ElMessage.error('获取分类列表失败，请稍后重试')
    }

    categoryTree.value = []
  } finally {
    categoryLoading.value = false
  }
}

const refreshCategories = async () => {
  await fetchCategories()
}

// 从数据库数据构建分类树（与ArticleManagement保持一致）
const buildCategoryTreeFromData = (categories) => {
  console.log('输入分类数据:', categories)
  
  if (!categories || categories.length === 0) {
    return []
  }

  const nodeMap = new Map()
  const root = []

  // 收集所有路径段
  const allPaths = new Set()

  categories.forEach(category => {
    if (!category.path) return

    const pathParts = category.path.split('/')
    let currentPath = ''

    // 为每个路径段创建完整路径
    pathParts.forEach((part, index) => {
      if (!part.trim()) return // 跳过空路径段

      const parentPath = currentPath
      currentPath = currentPath ? `${currentPath}/${part}` : part
      allPaths.add(currentPath)
    })
  })

  // 按路径长度排序，确保父节点先创建
  const sortedPaths = Array.from(allPaths).sort((a, b) => {
    const aDepth = a.split('/').length
    const bDepth = b.split('/').length
    if (aDepth !== bDepth) return aDepth - bDepth
    return a.localeCompare(b)
  })

  // 创建所有节点
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

      // 找到父节点并添加到其children���
      if (parentPath && nodeMap.has(parentPath)) {
        const parentNode = nodeMap.get(parentPath)
        if (!parentNode.children.find(child => child.path === fullPath)) {
          parentNode.children.push(node)
        }
      } else if (!parentPath) {
        // 根节点
        if (!root.find(child => child.path === fullPath)) {
          root.push(node)
        }
      }
    }
  })

  console.log('构建的分类树:', root)
  return root
}

// 处理分类变化 - 修复级联选择器的值处理
const handleCategoryChange = (value) => {
  console.log('分类变化:', value)
  if (value && value.length > 0) {
    // 级联选择器返回的是路径数组，我们取最后一个值作为完整路径
    formData.category = value[value.length - 1]
    formData.categoryPath = value
  } else {
    formData.category = ''
    formData.categoryPath = []
  }
  console.log('设置的分类路径:', formData.category)
}

// 获取标签
const fetchTags = async () => {
  try {
    const res = await axios.get('/api/tags')
    existingTags.value = res.data.tags || []
  } catch (e) {
    existingTags.value = []
  }
}

// 主要操作
const handleUpload = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    if (!formData.file) {
      ElMessage.warning('请选择要上传的文件')
      return
    }
    
    if (!formData.category) {
      ElMessage.warning('请选择分类文件夹')
      return
    }

    uploading.value = true
    
    // 自动生成slug从文件名
    const fileName = formData.file.name.replace(/\.(md|markdown)$/i, '')
    const slug = fileName
      .toLowerCase()
      .replace(/[^\w\u4e00-\u9fa5]/g, '-')
      .replace(/-+/g, '-')
      .replace(/^-|-$/g, '')
    
    const uploadData = {
      title: formData.title,
      slug: slug,
      category: formData.category,
      date: formData.date,
      summary: formData.summary,
      tags: formData.tags,
      status: formData.status,
      content: formData.content
    }
    
    console.log('上传文章数据:', uploadData)

    const response = await axios.post('/api/articles', uploadData, {
      timeout: 30000,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })

    console.log('上传响应:', response.data)
    ElMessage.success('文章上传成功')

    // 上传成功后立即重置表单，避免关闭时出现警告弹窗
    resetForm()

    emit('upload-success')
    emit('update:modelValue', false)
  } catch (error) {
    console.error('上传失败:', error)

    if (error.code === 'NETWORK_ERROR' || error.message === 'Network Error') {
      ElMessage.error('网络连接失败，请检查服务器状态')
    } else if (error.response?.status === 409) {
      ElMessage.error('文章标题已存在')
    } else if (error.response?.status === 400) {
      ElMessage.error(error.response.data?.detail || '请求参数错误')
    } else if (error.response?.status === 404) {
      ElMessage.error('上传接口不可用，请联系管理员')
    } else {
      ElMessage.error('上传失败: ' + (error.response?.data?.detail || error.message))
    }
  } finally {
    uploading.value = false
  }
}

const handleClose = () => {
  // 检查是否有未保存的内容
  const hasUnsavedContent = formData.title || formData.content || formData.file ||
                           formData.summary || formData.tags.length > 0 ||
                           formData.category

  if (hasUnsavedContent) {
    ElMessageBox.confirm(
      '确定要关闭吗？未保存的内容将丢失。',
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
      // 用户取消
    })
  } else {
    resetForm()
    emit('update:modelValue', false)
  }
}

const resetForm = () => {
  Object.assign(formData, {
    title: '',
    category: '',
    date: new Date().toISOString().split('T')[0],
    summary: '',
    tags: [],
    status: 'draft',
    file: null,
    content: ''
  })
  
  if (uploadRef.value) {
    uploadRef.value.clearFiles()
  }
  
  if (formRef.value) {
    formRef.value.resetFields()
  }
}

// 文件上传处理
const handleFileChange = (file) => {
  console.log('文件变化:', file)
  if (file && file.raw) {
    formData.file = file.raw

    // 自动从文件名提取标题（如果标题为空）
    if (!formData.title) {
      const fileName = file.name.replace(/\.(md|markdown)$/i, '')
      formData.title = fileName
    }

    // 读取文件内容
    const reader = new FileReader()
    reader.onload = (e) => {
      formData.content = e.target.result
      console.log('文件内���读取完成')
    }
    reader.onerror = (e) => {
      console.error('文件读取失败:', e)
      ElMessage.error('文件读取失败')
    }
    reader.readAsText(file.raw, 'utf-8')
  }
}

const handleFileRemove = () => {
  formData.file = null
  formData.content = ''
  console.log('文件移除')
}

// 监听新分类名称变化
watch(() => newCategory.name, () => {
  // 触发预览路径更新
})

watch(() => newCategory.parent, () => {
  // 触发预览路径更新
})

// 组件挂载
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

.parent-selector-card {
  border: 1px solid #e1e8ed;
  border-radius: 6px;
  height: 200px;
}

.parent-tree-container {
  height: 150px;
  overflow-y: auto;
}

.parent-tree {
  background: transparent;
}

.no-parent {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #909399;
  font-style: italic;
}

.selected-category,
.selected-parent {
  color: #409eff;
  font-size: 12px;
  margin-top: 6px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.clear-parent {
  color: #666 !important;
  font-weight: normal !important;
  margin-left: 8px;
}

.clear-parent:hover {
  color: #f56c6c !important;
}

.summary-actions {
  margin-top: 8px;
  text-align: right;
}

.form-tip {
  color: #909399;
  font-size: 12px;
  margin-top: 4px;
}

.dialog-footer {
  text-align: right;
}

/* 禁用按钮样式 */
.el-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.category-actions .el-button:disabled {
  background-color: #f5f7fa;
  border-color: #e4e7ed;
  color: #c0c4cc;
}

.category-actions .el-button--success:disabled {
  background-color: #b3d8b3;
  border-color: #b3d8b3;
  color: #ffffff;
}

/* ...existing code for other styles... */

/* 自定义滚动条样式 */
.category-tree-container::-webkit-scrollbar,
.parent-tree-container::-webkit-scrollbar {
  width: 6px;
}

.category-tree-container::-webkit-scrollbar-track,
.parent-tree-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.category-tree-container::-webkit-scrollbar-thumb,
.parent-tree-container::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.category-tree-container::-webkit-scrollbar-thumb:hover,
.parent-tree-container::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
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
  padding: 6px 0;
  border-radius: 4px;
}

:deep(.el-tree-node__content:hover) {
  background-color: #f5f7fa;
}

:deep(.el-tree-node__label) {
  font-size: 14px;
}

:deep(.el-tree .el-tree-node.is-current > .el-tree-node__content) {
  background-color: #e8f4fd;
  color: #409eff;
}
</style>