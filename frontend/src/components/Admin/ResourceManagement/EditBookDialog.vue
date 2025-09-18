<template>
  <el-dialog
      :before-close="handleClose"
      :close-on-click-modal="false"
      :model-value="modelValue"
      title="编辑图书信息"
      width="600px"
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

      <!-- 图书封面 -->
      <el-form-item label="图书封面" prop="cover">
        <el-input
            v-model="formData.cover"
            placeholder="请输入图床链接URL"
        />
        <div class="form-tip">请输入完整的图床链接URL，如：https://s21.ax1x.com/xxx.png</div>
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

      <!-- 文件信息(只读) -->
      <el-form-item label="文件信息">
        <el-input
            :value="book?.filename || '暂无文件'"
            placeholder="PDF文件名"
            readonly
        />
        <div class="form-tip">文件信息只读，如需更换文件请重新上传</div>
      </el-form-item>
    </el-form>

    <!-- 对话框底部按钮 -->
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button :loading="saving" type="primary" @click="handleSave">
          <el-icon>
            <Check/>
          </el-icon>
          保存修改
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import {onMounted, reactive, ref, watch} from 'vue'
import {ElMessage, ElMessageBox} from 'element-plus'
import {Check, Edit} from '@element-plus/icons-vue'
import axios from 'axios'

// Props和Emits
const props = defineProps({
  modelValue: Boolean,
  book: Object
})

const emit = defineEmits(['update:modelValue', 'save-success'])

// 响应式数据
const formData = reactive({
  title: '',
  description: '',
  cover: 'https://ooo.0x0.ooo/2025/09/18/OlGAw6.jpg',  // 默认图床封面
  tags: [],
  status: 'draft'
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

// 初始化表单数据
const initFormData = () => {
  if (props.book) {
    Object.assign(formData, {
      title: props.book.title || '',
      description: props.book.description || '',
      cover: props.book.cover || 'https://ooo.0x0.ooo/2025/09/18/OlGAw6.jpg',  // 使用图床URL
      tags: props.book.tags || [],
      status: props.book.status || 'draft'
    })

    // 保存原始数据用于变化检测
    originalData.value = {
      title: props.book.title || '',
      description: props.book.description || '',
      cover: props.book.cover || 'https://ooo.0x0.ooo/2025/09/18/OlGAw6.jpg',
      tags: [...(props.book.tags || [])],
      status: props.book.status || 'draft'
    }
  }
}

// 检测数据是否有变化
const hasChanges = () => {
  const current = {
    title: formData.title,
    description: formData.description,
    cover: formData.cover,
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
      cover: formData.cover,
      tags: formData.tags,
      status: formData.status
    }

    console.log('保存图书修改:', updateData)

    const response = await axios.put(`/api/admin/books/${props.book.id}`, updateData, {
      timeout: 30000,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })

    console.log('编辑响应:', response.data)
    ElMessage.success('图书信息保存成功')

    emit('save-success')
    emit('update:modelValue', false)
  } catch (error) {
    console.error('保存失败:', error)

    if (error.code === 'NETWORK_ERROR' || error.message === 'Network Error') {
      ElMessage.error('网络连接失败，请检查服务器状态')
    } else if (error.response?.status === 400) {
      ElMessage.error(error.response.data?.detail || '请求参数错误')
    } else if (error.response?.status === 404) {
      ElMessage.error('图书不存在或已被删除')
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

// 监听书籍数据变化
watch(() => props.book, (newBook) => {
  if (newBook && props.modelValue) {
    initFormData()
  }
}, {deep: true, immediate: true})

// 监听对话框打开
watch(() => props.modelValue, (isOpen) => {
  if (isOpen && props.book) {
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
