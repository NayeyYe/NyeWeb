<template>
  <el-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    title="编辑项目"
    width="700px"
    :before-close="handleClose"
    :close-on-click-modal="false"
  >
    <el-form :model="formData" :rules="formRules" label-width="100px" ref="formRef">
      <!-- 重新上传文件 -->
      <el-form-item label="重新上传" prop="file">
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
          <el-button type="primary" :icon="UploadIcon">重新选择Markdown文件</el-button>
          <template #tip>
            <div class="el-upload__tip">
              留空则保持原文件内容不变
            </div>
          </template>
        </el-upload>
      </el-form-item>

      <!-- 项目标题 -->
      <el-form-item label="项目标题" prop="title" required>
        <el-input
          v-model="formData.title"
          placeholder="请输入项目标题"
          maxlength="255"
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

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" @click="handleUpdate" :loading="updating">
          <el-icon><Check /></el-icon>
          更新项目
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { onMounted, reactive, ref, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Check, Edit, Upload as UploadIcon } from '@element-plus/icons-vue'
import axios from 'axios'

const props = defineProps({
  modelValue: Boolean,
  project: Object
})

const emit = defineEmits(['update:modelValue', 'update-success'])

const formData = reactive({
  title: '',
  date: '',
  summary: '',
  tags: [],
  status: 'draft',
  file: null,
  content: ''
})

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

const formRef = ref(null)
const uploadRef = ref(null)
const existingTags = ref([])
const updating = ref(false)
const hasChanges = ref(false)

// 监听项目数据变化，初始化表单
watch(() => props.project, (newProject) => {
  if (newProject && props.modelValue) {
    initializeForm(newProject)
  }
}, { immediate: true })

const initializeForm = (project) => {
  Object.assign(formData, {
    title: project.title || '',
    date: project.date || '',
    summary: project.summary || '',
    tags: Array.isArray(project.tags) ? [...project.tags] : [],
    status: project.status || 'draft',
    file: null,
    content: ''
  })
  hasChanges.value = false
}

// 监听表单数据变化
watch(() => [formData.title, formData.date, formData.summary, formData.tags, formData.status], () => {
  hasChanges.value = true
}, { deep: true })

const fetchTags = async () => {
  try {
    const res = await axios.get('/api/project-tags')
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
      response = await axios.put(`/api/projects/${props.project.id}`, updateData, {
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
          response = await axios.patch(`/api/projects/${props.project.id}`, updateData, {
            timeout: 30000,
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json'
            }
          })
        } catch (patchError) {
          // 如果PATCH也不支持，尝试POST到更新端点
          if (patchError.response?.status === 405) {
            response = await axios.post(`/api/projects/${props.project.id}/edit`, updateData, {
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

    ElMessage.success('项目更新成功')
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
    ElMessage.error('项目标题已存在')
  } else if (error.response?.status === 400) {
    ElMessage.error(error.response.data?.detail || '请求参数错误')
  } else if (error.response?.status === 404) {
    ElMessage.error('项目不存在或已被删除')
  } else if (error.response?.status === 405) {
    ElMessage.error('服务器不支持此操作，请联系管理员')
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
    }).catch(() => {})
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
</style>
