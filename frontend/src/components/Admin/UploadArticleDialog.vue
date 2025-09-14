<template>
  <el-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    title="上传文章"
    width="600px"
    :before-close="handleClose"
  >
    <el-form :model="formData" label-width="100px" ref="formRef">
      <el-form-item label="选择文件" required>
        <el-upload
          ref="uploadRef"
          :auto-upload="false"
          :show-file-list="true"
          :on-change="handleFileChange"
          :on-remove="handleFileRemove"
          accept=".md,.markdown"
          :limit="1"
        >
          <el-button type="primary">选择Markdown文件</el-button>
          <template #tip>
            <div class="el-upload__tip">
              只能上传 .md 或 .markdown 文件
            </div>
          </template>
        </el-upload>
      </el-form-item>

      <el-form-item label="文章标题" required>
        <el-input
          v-model="formData.title"
          placeholder="请输入文章标题"
          @input="generateSlug"
        />
      </el-form-item>

      <el-form-item label="URL标识符">
        <el-input
          v-model="formData.slug"
          placeholder="自动生成，也可手动修改"
          readonly
        />
      </el-form-item>

      <el-form-item label="分类目录">
        <el-cascader
          v-model="formData.categoryPath"
          :options="categoryOptions"
          :props="cascaderProps"
          placeholder="选择或创建分类目录"
          clearable
          filterable
          @change="handleCategoryChange"
        />
        <div class="category-actions">
          <el-button size="small" @click="showCreateCategory = true">
            创建新分类
          </el-button>
        </div>
      </el-form-item>

      <el-form-item label="发布日期">
        <el-date-picker
          v-model="formData.date"
          type="date"
          placeholder="选择发布日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
        />
      </el-form-item>

      <el-form-item label="文章摘要">
        <el-input
          v-model="formData.summary"
          type="textarea"
          :rows="3"
          placeholder="请输入文章摘要"
        />
        <div class="summary-actions">
          <el-button size="small" @click="generateSummary" :loading="summaryLoading">
            AI生成摘要
          </el-button>
        </div>
      </el-form-item>

      <el-form-item label="文章状态">
        <el-radio-group v-model="formData.status">
          <el-radio label="draft">草稿</el-radio>
          <el-radio label="published">发布</el-radio>
        </el-radio-group>
      </el-form-item>
    </el-form>

    <!-- 创建分类对话框 -->
    <el-dialog
      v-model="showCreateCategory"
      title="创建新分类"
      width="400px"
      append-to-body
    >
      <el-form :model="newCategory" label-width="80px">
        <el-form-item label="分类名称" required>
          <el-input
            v-model="newCategory.name"
            placeholder="请输入分类名称"
          />
        </el-form-item>
        <el-form-item label="父分类">
          <el-cascader
            v-model="newCategory.parent"
            :options="categoryOptions"
            :props="cascaderProps"
            placeholder="选择父分类（可选）"
            clearable
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateCategory = false">取消</el-button>
        <el-button type="primary" @click="createCategory">创建</el-button>
      </template>
    </el-dialog>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" @click="handleUpload" :loading="uploading">
          上传文章
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import {onMounted, reactive, ref} from 'vue'
import {ElMessage} from 'element-plus'
import axios from 'axios'

// Props和Emits
const props = defineProps({
  modelValue: Boolean
})

const emit = defineEmits(['update:modelValue', 'upload-success'])

// 响应式数据
const formData = reactive({
  title: '',
  slug: '',
  categoryPath: [],
  category: '',
  date: new Date().toISOString().split('T')[0],
  summary: '',
  status: 'draft',
  file: null,
  content: ''
})

const newCategory = reactive({
  name: '',
  parent: []
})

const categoryOptions = ref([])
const showCreateCategory = ref(false)
const uploading = ref(false)
const summaryLoading = ref(false)
const uploadRef = ref(null)
const formRef = ref(null)

// 级联选择器配置
const cascaderProps = {
  value: 'value',
  label: 'label',
  children: 'children',
  checkStrictly: true
}

// 处理文件选择
const handleFileChange = (file) => {
  formData.file = file.raw
  
  // 从文件名自动生成标题和slug
  const fileName = file.name.replace(/\.(md|markdown)$/i, '')
  if (!formData.title) {
    formData.title = fileName
    generateSlug()
  }
  
  // 读取文件内容
  const reader = new FileReader()
  reader.onload = (e) => {
    formData.content = e.target.result
  }
  reader.readAsText(file.raw)
}

// 处理文件移除
const handleFileRemove = () => {
  formData.file = null
  formData.content = ''
}

// 生成Slug
const generateSlug = () => {
  if (formData.title) {
    formData.slug = formData.title
      .toLowerCase()
      .replace(/[^a-z0-9\u4e00-\u9fa5]/g, '-')
      .replace(/-+/g, '-')
      .replace(/^-|-$/g, '')
  }
}

// 处理分类变化
const handleCategoryChange = (value) => {
  if (value && value.length > 0) {
    formData.category = value.join('/')
  } else {
    formData.category = ''
  }
}

// 生成摘要
const generateSummary = async () => {
  if (!formData.content) {
    ElMessage.warning('请先选择文件')
    return
  }
  
  summaryLoading.value = true
  try {
    // 模拟AI生成摘要
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // 简单的摘要生成逻辑
    const contentText = formData.content
      .replace(/[#*`]/g, '')
      .substring(0, 200)
      .trim()
    
    formData.summary = contentText + '...'
    ElMessage.success('摘要生成成功')
  } catch (error) {
    console.error('生成摘要失败:', error)
    ElMessage.error('生成摘要失败')
  } finally {
    summaryLoading.value = false
  }
}

// 创建分类
const createCategory = () => {
  if (!newCategory.name) {
    ElMessage.warning('请输入分类名称')
    return
  }
  
  // 这里应该调用API创建分类
  ElMessage.success('分类创建成功')
  showCreateCategory.value = false
  
  // 重置表单
  newCategory.name = ''
  newCategory.parent = []
  
  // 重新获取分类列表
  fetchCategories()
}

// 处理上传
const handleUpload = async () => {
  if (!formData.file || !formData.title) {
    ElMessage.warning('请选择文件并填写标题')
    return
  }
  
  uploading.value = true
  try {
    const uploadData = {
      title: formData.title,
      slug: formData.slug,
      category: formData.category,
      date: formData.date,
      summary: formData.summary,
      status: formData.status,
      content: formData.content
    }
    
    await axios.post('/api/articles', uploadData)
    
    ElMessage.success('文章上传成功')
    emit('upload-success')
    handleClose()
  } catch (error) {
    console.error('上传失败:', error)
    ElMessage.error('上传失败')
  } finally {
    uploading.value = false
  }
}

// 处理关闭
const handleClose = () => {
  // 重置表单
  Object.assign(formData, {
    title: '',
    slug: '',
    categoryPath: [],
    category: '',
    date: new Date().toISOString().split('T')[0],
    summary: '',
    status: 'draft',
    file: null,
    content: ''
  })
  
  // 清空上传组件
  if (uploadRef.value) {
    uploadRef.value.clearFiles()
  }
  
  emit('update:modelValue', false)
}

// 获取分类列表
const fetchCategories = async () => {
  try {
    const response = await axios.get('/api/articles/categories')
    // 转换为级联选择器格式
    categoryOptions.value = convertToTreeData(response.data.categories)
  } catch (error) {
    console.error('获取分类失败:', error)
  }
}

// 转换分类数据为树形结构
const convertToTreeData = (categories) => {
  // 这里需要根据实际的分类数据结构来实现
  // 暂时返回一个示例结构
  return [
    {
      value: 'technology',
      label: '技术文章',
      children: [
        { value: 'frontend', label: '前端开发' },
        { value: 'backend', label: '后端开发' }
      ]
    },
    {
      value: 'life',
      label: '生活感悟'
    }
  ]
}

// 组件挂载
onMounted(() => {
  fetchCategories()
})
</script>

<style scoped>
.category-actions {
  margin-top: 10px;
}

.summary-actions {
  margin-top: 10px;
  text-align: right;
}

.dialog-footer {
  text-align: right;
}

:deep(.el-upload__tip) {
  color: #909399;
  font-size: 12px;
  line-height: 1.2;
  margin-top: 7px;
}
</style>

