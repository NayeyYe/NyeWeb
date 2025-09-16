<template>
  <el-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    title="编辑图片信息"
    width="600px"
    :before-close="handleClose"
    :close-on-click-modal="false"
  >
    <el-form :model="formData" :rules="formRules" label-width="100px" ref="formRef">
      <!-- 图片标题 -->
      <el-form-item label="图片标题" prop="title" required>
        <el-input
          v-model="formData.title"
          placeholder="请输入图片标题"
          maxlength="255"
          show-word-limit
        />
      </el-form-item>

      <!-- 图片描述 -->
      <el-form-item label="图片描述" prop="description">
        <el-input
          v-model="formData.description"
          type="textarea"
          :rows="3"
          placeholder="请输入图片描述"
          maxlength="500"
          show-word-limit
        />
      </el-form-item>

      <!-- 图片URL -->
      <el-form-item label="图片URL" prop="url" required>
        <el-input
          v-model="formData.url"
          placeholder="请输入图床链接URL"
        />
        <div class="form-tip">请输入完整的图床链接URL，如：https://s21.ax1x.com/xxx.png</div>
      </el-form-item>

      <!-- 图片标签 -->
      <el-form-item label="图片标签">
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

      <!-- 图片状态 -->
      <el-form-item label="图片状态" prop="status" required>
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
        <el-button type="primary" @click="handleSave" :loading="saving">
          <el-icon><Check /></el-icon>
          保存修改
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { onMounted, reactive, ref, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Edit, 
  Check
} from '@element-plus/icons-vue'
import axios from 'axios'

// Props和Emits
const props = defineProps({
  modelValue: Boolean,
  figure: Object
})

const emit = defineEmits(['update:modelValue', 'save-success'])

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
    { required: true, message: '请输入图片标题', trigger: 'blur' },
    { min: 1, max: 255, message: '标题长度应在1-255个字符之间', trigger: 'blur' }
  ],
  url: [
    { required: true, message: '请输入图片URL', trigger: 'blur' },
    { 
      pattern: /^https?:\/\/.+\.(jpg|jpeg|png|gif|webp)(\?.*)?$/i, 
      message: '请输入有效的图片URL（支持jpg、png、gif、webp格式）', 
      trigger: 'blur' 
    }
  ],
  status: [
    { required: true, message: '请选择图片状态', trigger: 'change' }
  ]
}

// 引用
const formRef = ref(null)

// 状态数据
const existingTags = ref([])
const saving = ref(false)
const originalData = ref({})

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

// 初始化表单数据
const initFormData = () => {
  if (props.figure) {
    Object.assign(formData, {
      title: props.figure.title || '',
      description: props.figure.description || '',
      url: props.figure.url || 'https://s21.ax1x.com/2025/09/16/pVfLCfe.png',
      tags: props.figure.tags || [],
      status: props.figure.status || 'draft'
    })
    
    // 保存原始数据用于变化检测
    originalData.value = {
      title: props.figure.title || '',
      description: props.figure.description || '',
      url: props.figure.url || 'https://s21.ax1x.com/2025/09/16/pVfLCfe.png',
      tags: [...(props.figure.tags || [])],
      status: props.figure.status || 'draft'
    }
  }
}

// 检测数据是否有变化
const hasChanges = () => {
  const current = {
    title: formData.title,
    description: formData.description,
    url: formData.url,
    tags: [...formData.tags],
    status: formData.status
  }
  
  return JSON.stringify(current) !== JSON.stringify(originalData.value)
}

// 保存修改
const handleSave = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    if (!hasChanges()) {
      ElMessage.info('没有检测到任何修改')
      return
    }
    
    saving.value = true
    
    const updateData = {
      title: formData.title,
      description: formData.description,
      url: formData.url,
      tags: formData.tags,
      status: formData.status
    }
    
    console.log('保存图片修改:', updateData)
    
    const response = await axios.put(`/api/admin/figures/${props.figure.id}`, updateData, {
      timeout: 30000,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })
    
    console.log('编辑响应:', response.data)
    ElMessage.success('图片信息保存成功')
    
    emit('save-success')
    emit('update:modelValue', false)
  } catch (error) {
    console.error('保存失败:', error)
    
    if (error.code === 'NETWORK_ERROR' || error.message === 'Network Error') {
      ElMessage.error('网络连接失败，请检查服务器状态')
    } else if (error.response?.status === 400) {
      ElMessage.error(error.response.data?.detail || '请求参数错误')
    } else if (error.response?.status === 404) {
      ElMessage.error('图片不存在或已被删除')
    } else {
      ElMessage.error('保存失败: ' + (error.response?.data?.detail || error.message))
    }
  } finally {
    saving.value = false
  }
}

const handleClose = () => {
  if (hasChanges()) {
    ElMessageBox.confirm(
      '确定要关闭吗？未保存的修改将丢失。',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    ).then(() => {
      emit('update:modelValue', false)
    }).catch(() => {
      // 用户取消
    })
  } else {
    emit('update:modelValue', false)
  }
}

// 监听图片数据变化
watch(() => props.figure, (newFigure) => {
  if (newFigure && props.modelValue) {
    initFormData()
  }
}, { deep: true, immediate: true })

// 监听对话框打开
watch(() => props.modelValue, (isOpen) => {
  if (isOpen && props.figure) {
    initFormData()
  }
})

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
