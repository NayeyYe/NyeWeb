<template>
  <el-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    title="上传图书"
    width="600px"
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
          accept=".pdf"
          :limit="1"
          class="upload-section"
        >
          <el-button type="primary" :icon="UploadIcon">选择PDF文件</el-button>
          <template #tip>
            <div class="el-upload__tip">
              只能上传 PDF 文件
            </div>
          </template>
        </el-upload>
      </el-form-item>

      <!-- 图书标题 -->
      <el-form-item label="图书标题" prop="title" required>
        <el-input
          v-model="formData.title"
          placeholder="请输入图书标题"
          maxlength="255"
          show-word-limit
        />
      </el-form-item>

      <!-- 图书描述 -->
      <el-form-item label="图书描述" prop="description">
        <el-input
          v-model="formData.description"
          type="textarea"
          :rows="4"
          placeholder="请输入图书描述"
          maxlength="1000"
          show-word-limit
        />
      </el-form-item>

      <!-- 图书封面 -->
      <el-form-item label="图书封面" prop="cover">
        <el-input
          v-model="formData.cover"
          placeholder="封面图片URL（暂时使用默认封面）"
          disabled
        />
        <div class="form-tip">封面功能开发中，当前使用默认封面</div>
      </el-form-item>

      <!-- 图书标签 -->
      <el-form-item label="图书标签">
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

      <!-- 图书状态 -->
      <el-form-item label="图书状态" prop="status" required>
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

    <!-- 对话框底部按钮 -->
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" @click="handleUpload" :loading="uploading">
          <el-icon><Upload /></el-icon>
          上传图书
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Upload, 
  Edit, 
  Check, 
  Upload as UploadIcon
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
  description: '',
  cover: '/avatar.jpg',
  tags: [],
  status: 'draft',
  file: null,
  filename: ''
})

// 表单验证规则
const formRules = {
  title: [
    { required: true, message: '请输入图书标题', trigger: 'blur' },
    { min: 1, max: 255, message: '标题长度应在1-255个字符之间', trigger: 'blur' }
  ],
  status: [
    { required: true, message: '请选择图书状态', trigger: 'change' }
  ],
  file: [
    { required: true, message: '请选择要上传的PDF文件', trigger: 'change' }
  ]
}

// 引用
const formRef = ref(null)
const uploadRef = ref(null)

// 状态数据
const existingTags = ref([])
const uploading = ref(false)

// 文件处理
const handleFileChange = (file) => {
  console.log('文件变化:', file)
  if (file && file.raw) {
    formData.file = file.raw
    
    // 如果标题为空，从文件名提取标题，正确处理中文编码
    if (!formData.title) {
      let fileName = file.name.replace(/\.pdf$/i, '')
      
      // 确保文件名正确解码中文字符
      try {
        // 如果文件名已经是正确编码，直接使用
        fileName = decodeURIComponent(fileName)
      } catch (e) {
        // 如果解码失败，使用原文件名
        console.warn('文件名解码失败，使用原文件名:', e)
      }
      
      formData.title = fileName
    }
    
    console.log('文件选择完成:', file.name, '提取标题:', formData.title)
  }
}

const handleFileRemove = () => {
  formData.file = null
  formData.filename = ''
  console.log('文件已移除')
}

// 获取标签数据
const fetchTags = async () => {
  try {
    console.log('开始获取图书标签数据...')
    const response = await axios.get('/api/book-tags')
    console.log('标签数据响应:', response.data)
    
    if (response.data?.tags && Array.isArray(response.data.tags)) {
      existingTags.value = response.data.tags
      console.log('成功获取标签:', existingTags.value)
    } else {
      console.warn('标签数据格式异常或为空:', response.data)
      existingTags.value = []
    }
  } catch (error) {
    console.error('获取标签失败:', error)
    existingTags.value = []
    // 不显示错误消息，静默失败
  }
}

// 主要操作
const handleUpload = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    if (!formData.file) {
      ElMessage.warning('请选择要上传的PDF文件')
      return
    }
    
    uploading.value = true
    
    // 第一步：上传文件
    const fileFormData = new FormData()
    fileFormData.append('file', formData.file)
    
    console.log('开始上传文件...')
    const fileResponse = await axios.post('/api/admin/books/upload', fileFormData, {
      timeout: 300000, // 5分钟超时，适应大文件上传
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    
    console.log('文件上传响应:', fileResponse.data)
    formData.filename = fileResponse.data.filename
    
    // 第二步：创建图书记录
    const bookData = {
      title: formData.title,
      description: formData.description,
      cover: formData.cover,
      tags: formData.tags,
      status: formData.status,
      filename: formData.filename
    }
    
    console.log('创建图书记录:', bookData)
    
    const bookResponse = await axios.post('/api/admin/books', bookData, {
      timeout: 30000,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })
    
    console.log('图书创建响应:', bookResponse.data)
    ElMessage.success('图书上传成功')
    
    // 上传成功后立即重置表单
    resetForm()
    
    emit('upload-success')
    emit('update:modelValue', false)
  } catch (error) {
    console.error('上传失败:', error)
    
    if (error.code === 'NETWORK_ERROR' || error.message === 'Network Error') {
      ElMessage.error('网络连接失败，请检查服务器状态')
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
  const hasUnsavedContent = formData.title || formData.description || formData.file ||
                           formData.tags.length > 0

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
    description: '',
    cover: '/avatar.jpg',
    tags: [],
    status: 'draft',
    file: null,
    filename: ''
  })
  
  if (uploadRef.value) {
    uploadRef.value.clearFiles()
  }
  
  if (formRef.value) {
    formRef.value.resetFields()
  }
}

// 组件挂载
onMounted(() => {
  fetchTags()
})
</script>

<style scoped>
.upload-section {
  width: 100%;
}

.form-tip {
  color: #909399;
  font-size: 12px;
  margin-top: 4px;
}

.dialog-footer {
  text-align: right;
}

:deep(.el-upload__tip) {
  margin-top: 8px;
  color: #666;
  font-size: 12px;
}

:deep(.el-textarea .el-input__count) {
  color: #909399;
  font-size: 12px;
}
</style>
