<template>
<el-dialog
      :before-close="handleClose"
      :close-on-click-modal="false"
      :model-value="modelValue"
      title="上传项目"
      @update:model-value="$emit('update:modelValue', $event)"
  >
    <el-form ref="formRef" :model="formData" :rules="formRules" label-width="100px">
      <!-- 文件上传 -->
      <el-form-item label="选择文件" prop="file" required>
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
          <el-button :icon="UploadIcon" type="primary">选择Markdown文件</el-button>
          <template #tip>
            <div class="el-upload__tip">
              只能上传 .md 或 .markdown 文件
            </div>
          </template>
        </el-upload>
      </el-form-item>

      <!-- 项目标题 -->
      <el-form-item label="项目标题" prop="title" required>
        <el-input
            v-model="formData.title"
            maxlength="255"
            placeholder="请输入项目标题"
            show-word-limit
        />
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

      <!-- 项目描述 -->
      <el-form-item label="项目描述" prop="summary">
        <el-input
            v-model="formData.summary"
            :rows="4"
            maxlength="500"
            placeholder="请输入项目描述"
            show-word-limit
            type="textarea"
        />
      </el-form-item>

      <!-- 项目标签 -->
      <el-form-item label="项目标签">
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

      <!-- 项目状态 -->
      <el-form-item label="项目状态" prop="status" required>
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

    <!-- 主对话框底部按钮 -->
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button :loading="uploading" type="primary" @click="handleUpload">
          <el-icon>
            <Upload/>
          </el-icon>
          上传项目
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import {onMounted, reactive, ref} from 'vue'
import {ElMessage, ElMessageBox} from 'element-plus'
import {Check, Edit, Upload, Upload as UploadIcon} from '@element-plus/icons-vue'
import axios from 'axios'

// Props和Emits
const props = defineProps({
  modelValue: Boolean
})

const emit = defineEmits(['update:modelValue', 'upload-success'])

// 响应式数据
const formData = reactive({
  title: '',
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
    {required: true, message: '请输入项目标题', trigger: 'blur'},
    {min: 1, max: 255, message: '标题长度应在1-255个字符之间', trigger: 'blur'}
  ],
  date: [
    {required: true, message: '请选择发布日期', trigger: 'change'}
  ],
  status: [
    {required: true, message: '请选择项目状态', trigger: 'change'}
  ],
  file: [
    {required: true, message: '请选择要上传的文件', trigger: 'change'}
  ]
}

// 引用
const formRef = ref(null)
const uploadRef = ref(null)

// 状态数据
const existingTags = ref([])
const uploading = ref(false)

// 获取标签
const fetchTags = async () => {
  try {
    const res = await axios.get('/api/project-tags')
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

    uploading.value = true

    // 自动生成slug从文件名或标题
    const fileName = formData.file.name.replace(/\.(md|markdown)$/i, '')
    const slug = (fileName || formData.title)
        .toLowerCase()
        .replace(/[^\w\u4e00-\u9fa5]/g, '-')
        .replace(/-+/g, '-')
        .replace(/^-|-$/g, '')

    const uploadData = {
      title: formData.title,
      slug: slug,
      summary: formData.summary,
      date: formData.date,
      tags: formData.tags,
      status: formData.status,
      content: formData.content
    }

    console.log('上传项目数据:', uploadData)

    const response = await axios.post('/api/projects', uploadData, {
      timeout: 30000,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })

    console.log('上传响应:', response.data)
    ElMessage.success('项目上传成功')

    // 上传成功后立即重置表单，避免关闭时出现警告弹窗
    resetForm()

    emit('upload-success')
    emit('update:modelValue', false)
  } catch (error) {
    console.error('上传失败:', error)

    if (error.code === 'NETWORK_ERROR' || error.message === 'Network Error') {
      ElMessage.error('网络连接失败，请检查服务器状态')
    } else if (error.response?.status === 409) {
      ElMessage.error('项目标题已存在')
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
      formData.summary || formData.tags.length > 0

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

    // 自动从文件名提取标题(如果标题为空)
    if (!formData.title) {
      const fileName = file.name.replace(/\.(md|markdown)$/i, '')
      formData.title = fileName
    }

    // 读取文件内容
    const reader = new FileReader()
    reader.onload = (e) => {
      formData.content = e.target.result
      console.log('文件内容读取完成')
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

.el-button {
  border-radius: 6px;
  font-weight: 500;
}

.el-button--primary {
  background: #409eff;
  border-color: #409eff;
}

:deep(.el-form-item__label) {
  font-weight: 500;
}

:deep(.el-input__inner) {
  border-radius: 6px;
}

:deep(.el-textarea__inner) {
  border-radius: 6px;
}

:deep(.el-select .el-input__inner) {
  border-radius: 6px;
}

/* 响应式布局优化 */
@media (max-width: 768px) {
  :deep(.el-dialog) {
    width: 95% !important;
    max-width: none !important;
  }
  
  :deep(.el-dialog__body) {
    padding: 15px 20px;
  }
  
  :deep(.el-form-item__label) {
    width: 80px !important;
  }
  
  :deep(.el-form-item__content) {
    margin-left: 80px !important;
  }
  
  :deep(.el-input__inner),
  :deep(.el-textarea__inner),
  :deep(.el-select .el-input__inner) {
    padding: 8px 12px;
  }
}

@media (max-width: 480px) {
  :deep(.el-dialog) {
    width: 95% !important;
    max-width: none !important;
  }
  
  :deep(.el-dialog__body) {
    padding: 10px 15px;
  }
  
  :deep(.el-form-item) {
    margin-bottom: 15px;
    display: flex;
    flex-direction: column;
  }
  
  :deep(.el-form-item__label) {
    width: 100% !important;
    font-size: 13px;
    margin-bottom: 5px;
    text-align: left !important;
    padding-bottom: 0;
  }
  
  :deep(.el-form-item__content) {
    margin-left: 0 !important;
    width: 100%;
  }
  
  :deep(.el-input__inner),
  :deep(.el-textarea__inner),
  :deep(.el-select .el-input__inner) {
    font-size: 13px;
    padding: 8px 10px;
  }
  
  :deep(.el-button) {
    font-size: 13px;
    padding: 8px 12px;
  }
  
  .form-tip {
    font-size: 11px;
  }
}

/* 针对小屏幕的额外优化 */
@media (max-width: 375px) {
  :deep(.el-dialog) {
    width: 95% !important;
    max-width: none !important;
  }
  
  :deep(.el-dialog__body) {
    padding: 8px 12px;
  }
  
  :deep(.el-form-item) {
    margin-bottom: 12px;
    display: flex;
    flex-direction: column;
  }
  
  :deep(.el-form-item__label) {
    width: 100% !important;
    font-size: 12px;
    margin-bottom: 5px;
    text-align: left !important;
    padding-bottom: 0;
  }
  
  :deep(.el-form-item__content) {
    margin-left: 0 !important;
    width: 100%;
  }
  
  :deep(.el-input__inner),
  :deep(.el-textarea__inner),
  :deep(.el-select .el-input__inner) {
    font-size: 12px;
    padding: 6px 8px;
  }
  
  :deep(.el-button) {
    font-size: 12px;
    padding: 6px 10px;
  }
  
  :deep(.el-radio) {
    margin-right: 15px;
  }
  
  :deep(.el-radio__label) {
    font-size: 12px;
  }
  
  .form-tip {
    font-size: 10px;
  }
  
  :deep(.el-date-editor .el-input__inner) {
    font-size: 12px;
    padding: 0 8px;
  }
  
  :deep(.el-radio) {
    margin-right: 15px;
  }
  
  :deep(.el-radio__label) {
    font-size: 12px;
  }
}
</style>
