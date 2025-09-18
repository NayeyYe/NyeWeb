<template>
  <el-dialog
      :before-close="handleClose"
      :close-on-click-modal="false"
      :model-value="modelValue"
      title="上传图片"
      width="600px"
      @update:model-value="$emit('update:modelValue', $event)"
  >
    <el-form ref="formRef" :model="formData" :rules="formRules" label-width="100px">
      <!-- 图片标题 -->
      <el-form-item label="图片标题" prop="title" required>
        <el-input
            v-model="formData.title"
            maxlength="255"
            placeholder="请输入图片标题"
            show-word-limit
        />
      </el-form-item>

      <!-- 图片描述 -->
      <el-form-item label="图片描述" prop="description">
        <el-input
            v-model="formData.description"
            :rows="3"
            maxlength="500"
            placeholder="请输入图片描述"
            show-word-limit
            type="textarea"
        />
      </el-form-item>

      <!-- 图片URL -->
      <el-form-item label="图片URL" prop="url" required>
        <el-input
            v-model="formData.url"
            placeholder="请输入图床链接URL，如：https://s21.ax1x.com/xxx.png"
        />
        <div class="form-tip">请输入完整的图床链接URL，支持JPG、PNG、GIF、WebP格式</div>
      </el-form-item>

      <!-- 图片标签 -->
      <el-form-item label="图片标签">
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

      <!-- 图片状态 -->
      <el-form-item label="图片状态" prop="status" required>
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
          上传图片
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
  url: 'https://s21.ax1x.com/2025/09/16/pVfLCfe.png',
  tags: [],
  status: 'draft'
})

// 表单验证规则
const formRules = {
  title: [
    {required: true, message: '请输入图片标题', trigger: 'blur'},
    {min: 1, max: 255, message: '标题长度应在1-255个字符之间', trigger: 'blur'}
  ],
  url: [
    {required: true, message: '请输入图片URL', trigger: 'blur'},
    {
      pattern: /^https?:\/\/.+\.(jpg|jpeg|png|gif|webp)(\?.*)?$/i,
      message: '请输入有效的图片URL（支持jpg、png、gif、webp格式）',
      trigger: 'blur'
    }
  ],
  status: [
    {required: true, message: '请选择图片状态', trigger: 'change'}
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
    console.log('开始获取图片标签数据...')
    const response = await axios.get('/api/figure-tags')
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

    uploading.value = true

    const figureData = {
      title: formData.title,
      description: formData.description,
      url: formData.url,
      tags: formData.tags,
      status: formData.status
    }

    console.log('上传图片数据:', figureData)

    const response = await axios.post('/api/admin/figures', figureData, {
      timeout: 30000,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })

    console.log('图片上传响应:', response.data)
    ElMessage.success('图片上传成功')

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
  const hasUnsavedContent = formData.title || formData.description ||
      formData.url !== 'https://s21.ax1x.com/2025/09/16/pVfLCfe.png' ||
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
    url: 'https://s21.ax1x.com/2025/09/16/pVfLCfe.png',
    tags: [],
    status: 'draft'
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
</style>
