<template>
<el-dialog
      :before-close="handleClose"
      :close-on-click-modal="false"
      :model-value="modelValue"
      title="上传图书"
      @update:model-value="$emit('update:modelValue', $event)"
  >
    <el-form ref="formRef" :model="formData" :rules="formRules" label-width="100px">
      <!-- 图书标题 -->
      <el-form-item label="图书标题" prop="title" required>
        <el-input
            v-model="formData.title"
            maxlength="255"
            placeholder="请输入图书标题"
            show-word-limit
        />
      </el-form-item>

      <!-- 图书描述 -->
      <el-form-item label="图书描述" prop="description">
        <el-input
            v-model="formData.description"
            :rows="4"
            maxlength="1000"
            placeholder="请输入图书描述"
            show-word-limit
            type="textarea"
        />
      </el-form-item>

      <!-- 网盘URL -->
      <el-form-item label="网盘链接" prop="filename" required>
        <el-input
            v-model="formData.filename"
            placeholder="请输入网盘下载链接，如：https://pan.baidu.com/xxx 或 https://drive.google.com/xxx"
        />
        <div class="form-tip">请输入完整的网盘分享链接，用户点击下载时将跳转到此链接</div>
      </el-form-item>

      <!-- 图书封面 -->
      <el-form-item label="图书封面" prop="cover">
        <el-input
            v-model="formData.cover"
            placeholder="请输入图床链接URL，如：https://s21.ax1x.com/xxx.png"
        />
        <div class="form-tip">请输入完整的图床链接URL，支持JPG、PNG等格式</div>
      </el-form-item>

      <!-- 图书标签 -->
      <el-form-item label="图书标签">
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

      <!-- 图书状态 -->
      <el-form-item label="图书状态" prop="status" required>
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

    <!-- 对话框底部按钮 -->
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button :loading="uploading" type="primary" @click="handleUpload">
          <el-icon>
            <Upload/>
          </el-icon>
          创建图书
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import {onMounted, reactive, ref} from 'vue'
import {ElMessage, ElMessageBox} from 'element-plus'
import {Check, Edit, Upload} from '@element-plus/icons-vue'
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
  cover: 'https://ooo.0x0.ooo/2025/09/18/OlGAw6.jpg',  // 使用图床URL作为默认封面
  tags: [],
  status: 'draft',
  filename: ''  // 改为存储网盘URL
})

// 表单验证规则
const formRules = {
  title: [
    {required: true, message: '请输入图书标题', trigger: 'blur'},
    {min: 1, max: 255, message: '标题长度应在1-255个字符之间', trigger: 'blur'}
  ],
  cover: [
    {required: true, message: '请输入封面URL', trigger: 'blur'},
    {
      pattern: /^https?:\/\/.+\.(jpg|jpeg|png|gif|webp)(\?.*)?$/i,
      message: '请输入有效的图片URL（支持jpg、png、gif、webp格式）',
      trigger: 'blur'
    }
  ],
  status: [
    {required: true, message: '请选择图书状态', trigger: 'change'}
  ],
  filename: [
    {required: true, message: '请输入网盘链接', trigger: 'blur'},
    {
      pattern: /^https?:\/\/.+/,
      message: '请输入有效的网盘链接（以http://或https://开头）',
      trigger: 'blur'
    }
  ]
}

// 引用
const formRef = ref(null)

// 状态数据
const existingTags = ref([])
const uploading = ref(false)

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
  }
}

// 主要操作
const handleUpload = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()

    uploading.value = true

    const bookData = {
      title: formData.title,
      description: formData.description,
      cover: formData.cover,
      tags: formData.tags,
      status: formData.status,
      filename: formData.filename  // 现在存储的是网盘URL
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
    ElMessage.success('图书创建成功')

    resetForm()
    emit('upload-success')
    emit('update:modelValue', false)
  } catch (error) {
    console.error('创建失败:', error)

    if (error.code === 'NETWORK_ERROR' || error.message === 'Network Error') {
      ElMessage.error('网络连接失败，请检查服务器状态')
    } else if (error.response?.status === 400) {
      ElMessage.error(error.response.data?.detail || '请求参数错误')
    } else if (error.response?.status === 404) {
      ElMessage.error('创建接口不可用，请联系管理员')
    } else {
      ElMessage.error('创建失败: ' + (error.response?.data?.detail || error.message))
    }
  } finally {
    uploading.value = false
  }
}

const handleClose = () => {
  const hasUnsavedContent = formData.title || formData.description || formData.filename ||
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
    cover: 'https://ooo.0x0.ooo/2025/09/18/OlGAw6.jpg',
    tags: [],
    status: 'draft',
    filename: ''
  })

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
.form-tip {
  color: #909399;
  font-size: 12px;
  margin-top: 4px;
}

.dialog-footer {
  text-align: right;
}

:deep(.el-textarea .el-input__count) {
  color: #909399;
  font-size: 12px;
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
}
</style>
