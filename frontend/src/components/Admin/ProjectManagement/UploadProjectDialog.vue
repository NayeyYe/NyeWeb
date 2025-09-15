<template>
  <el-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    title="上传项目"
    width="700px"
    :before-close="handleClose"
    :close-on-click-modal="false"
  >
    <el-form :model="formData" :rules="formRules" label-width="100px" ref="formRef">
      <!-- 项目标题 -->
      <el-form-item label="项目标题" prop="title" required>
        <el-input
          v-model="formData.title"
          placeholder="请输入项目标题"
          maxlength="255"
          show-word-limit
        />
      </el-form-item>

      <!-- 项目描述 -->
      <el-form-item label="项目描述" prop="summary">
        <el-input
          v-model="formData.summary"
          type="textarea"
          :rows="4"
          placeholder="请输入项目描述"
          maxlength="500"
          show-word-limit
        />
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

      <!-- 项目标签 -->
      <el-form-item label="项目标签">
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

      <!-- 项目状态 -->
      <el-form-item label="项目状态" prop="status" required>
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
          上传项目
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
  Check
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
  summary: '',
  date: new Date().toISOString().split('T')[0],
  tags: [],
  status: 'draft'
})

// 表单验证规则
const formRules = {
  title: [
    { required: true, message: '请输入项目标题', trigger: 'blur' },
    { min: 1, max: 255, message: '标题长度应在1-255个字符之间', trigger: 'blur' }
  ],
  date: [
    { required: true, message: '请选择发布日期', trigger: 'change' }
  ],
  status: [
    { required: true, message: '请选择项目状态', trigger: 'change' }
  ]
}

// 引用
const formRef = ref(null)

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

    uploading.value = true

    // 自动生成slug从标题
    const slug = formData.title
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
      status: formData.status
    }

    console.log('上传项目数据:', uploadData)

    // TODO: 实现项目上传API
    // const response = await axios.post('/api/projects', uploadData, {
    //   timeout: 30000,
    //   headers: {
    //     'Accept': 'application/json',
    //     'Content-Type': 'application/json'
    //   }
    // })

    // 模拟上传成功
    await new Promise(resolve => setTimeout(resolve, 1000))
    ElMessage.success('项目上传成功')

    // 上传成功后立即重置表单，避免关闭时出现警告弹窗
    resetForm()

    emit('upload-success')
    emit('update:modelValue', false)
  } catch (error) {
    console.error('上传失败:', error)
    ElMessage.error('项目上传功能开发中，敬请期待！')
  } finally {
    uploading.value = false
  }
}

const handleClose = () => {
  // 检查是否有未保存的内容
  const hasUnsavedContent = formData.title || formData.summary ||
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
    summary: '',
    date: new Date().toISOString().split('T')[0],
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
</style>

