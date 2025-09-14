<template>
  <el-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    :title="mode === 'create' ? '新建文章' : '编辑文章'"
    width="90%"
    :before-close="handleClose"
    class="article-editor-dialog"
  >
    <div class="editor-container">
      <!-- 文章信息表单 -->
      <div class="article-info">
        <el-form :model="formData" label-width="80px">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="标题" required>
                <el-input
                  v-model="formData.title"
                  placeholder="请输入文章标题"
                  @input="generateSlug"
                />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="Slug">
                <el-input
                  v-model="formData.slug"
                  placeholder="URL标识符，自动生成"
                />
              </el-form-item>
            </el-col>
          </el-row>
          
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="分类">
                <el-select
                  v-model="formData.category"
                  placeholder="选择或输入分类"
                  allow-create
                  filterable
                  style="width: 100%"
                >
                  <el-option
                    v-for="category in categories"
                    :key="category"
                    :label="category"
                    :value="category"
                  />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="发布日期">
                <el-date-picker
                  v-model="formData.date"
                  type="date"
                  placeholder="选择发布日期"
                  style="width: 100%"
                  format="YYYY-MM-DD"
                  value-format="YYYY-MM-DD"
                />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="状态">
                <el-select v-model="formData.status" style="width: 100%">
                  <el-option label="草稿" value="draft" />
                  <el-option label="已发布" value="published" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>

          <el-form-item label="摘要">
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
        </el-form>
      </div>

      <!-- Markdown编辑器 -->
      <div class="editor-section">
        <div class="editor-header">
          <div class="editor-tabs">
            <el-button
              :type="activeTab === 'edit' ? 'primary' : ''"
              size="small"
              @click="activeTab = 'edit'"
            >
              编辑
            </el-button>
            <el-button
              :type="activeTab === 'preview' ? 'primary' : ''"
              size="small"
              @click="activeTab = 'preview'"
            >
              预览
            </el-button>
            <el-button
              :type="activeTab === 'split' ? 'primary' : ''"
              size="small"
              @click="activeTab = 'split'"
            >
              分屏
            </el-button>
          </div>
          <div class="editor-actions">
            <el-button size="small" @click="autoSave" :loading="autoSaving">
              {{ autoSaving ? '保存中...' : '保存草稿' }}
            </el-button>
            <span class="save-status">{{ saveStatus }}</span>
          </div>
        </div>

        <div class="editor-content" :class="{ 'split-view': activeTab === 'split' }">
          <!-- 编辑区域 -->
          <div v-show="activeTab === 'edit' || activeTab === 'split'" class="edit-area">
            <textarea
              ref="markdownEditor"
              v-model="formData.content"
              class="markdown-editor"
              placeholder="在这里编写Markdown内容..."
              @input="handleContentChange"
            />
          </div>

          <!-- 预览区域 -->
          <div v-show="activeTab === 'preview' || activeTab === 'split'" class="preview-area">
            <div class="markdown-body" v-html="previewContent"></div>
          </div>
        </div>
      </div>
    </div>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" @click="handleSave" :loading="saving">
          {{ mode === 'create' ? '创建文章' : '保存更改' }}
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import {computed, onMounted, reactive, ref, watch} from 'vue'
import {ElMessage, ElMessageBox} from 'element-plus'
import axios from 'axios'
import markdownit from 'markdown-it'
import mdAnchor from 'markdown-it-anchor'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'
import 'github-markdown-css/github-markdown.css'

// Props和Emits
const props = defineProps({
  modelValue: Boolean,
  article: Object,
  mode: {
    type: String,
    default: 'create' // 'create' | 'edit'
  }
})

const emit = defineEmits(['update:modelValue', 'save', 'close'])

// 响应式数据
const formData = reactive({
  title: '',
  slug: '',
  category: '',
  date: '',
  summary: '',
  content: '',
  status: 'draft'
})

const categories = ref([])
const activeTab = ref('edit')
const saving = ref(false)
const autoSaving = ref(false)
const summaryLoading = ref(false)
const saveStatus = ref('')
const markdownEditor = ref(null)

// Markdown渲染器
const md = markdownit({
  html: true,
  linkify: true,
  typographer: true,
  highlight: function (str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return '<pre class="hljs"><code>' +
               hljs.highlight(str, { language: lang, ignoreIllegals: true }).value +
               '</code></pre>';
      } catch (__) {}
    }
    return '<pre class="hljs"><code>' + md.utils.escapeHtml(str) + '</code></pre>';
  }
}).use(mdAnchor)

// 计算属性 - 预览内容
const previewContent = computed(() => {
  if (!formData.content) return '<p>暂无内容</p>'
  return md.render(formData.content)
})

// 监听文章数据变化
watch(() => props.article, (newArticle) => {
  if (newArticle) {
    Object.assign(formData, {
      title: newArticle.title || '',
      slug: newArticle.slug || '',
      category: newArticle.category || '',
      date: newArticle.date || '',
      summary: newArticle.summary || '',
      content: newArticle.content || '',
      status: newArticle.status || 'draft'
    })
  } else {
    // 重置表单
    Object.assign(formData, {
      title: '',
      slug: '',
      category: '',
      date: new Date().toISOString().split('T')[0],
      summary: '',
      content: '',
      status: 'draft'
    })
  }
}, { immediate: true })

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

// 处理内容变化
const handleContentChange = () => {
  // 标记内容已修改
  saveStatus.value = '有未保存的更改'
  
  // 延迟自动保存
  clearTimeout(window.autoSaveTimer)
  window.autoSaveTimer = setTimeout(() => {
    if (props.mode === 'edit') {
      autoSave()
    }
  }, 30000) // 30秒后自动保存
}

// 自动保存
const autoSave = async () => {
  if (!formData.title || !formData.content) return
  
  autoSaving.value = true
  try {
    // 这里实现自动保存逻辑
    await new Promise(resolve => setTimeout(resolve, 1000)) // 模拟API调用
    saveStatus.value = '已自动保存'
    setTimeout(() => {
      saveStatus.value = ''
    }, 3000)
  } catch (error) {
    console.error('自动保存失败:', error)
    saveStatus.value = '自动保存失败'
  } finally {
    autoSaving.value = false
  }
}

// 生成摘要
const generateSummary = async () => {
  if (!formData.content) {
    ElMessage.warning('请先输入文章内容')
    return
  }
  
  summaryLoading.value = true
  try {
    // 模拟AI生成摘要
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // 简单的摘要生成逻辑（实际应该调用AI API）
    const contentText = formData.content.replace(/[#*`]/g, '').substring(0, 200)
    formData.summary = contentText + '...'
    
    ElMessage.success('摘要生成成功')
  } catch (error) {
    console.error('生成摘要失败:', error)
    ElMessage.error('生成摘要失败')
  } finally {
    summaryLoading.value = false
  }
}

// 处理保存
const handleSave = async () => {
  if (!formData.title || !formData.content) {
    ElMessage.warning('请填写标题和内容')
    return
  }
  
  saving.value = true
  try {
    const articleData = { ...formData }
    
    if (props.mode === 'create') {
      await axios.post('/api/articles', articleData)
    } else {
      await axios.put(`/api/articles/${props.article.id}`, articleData)
    }
    
    emit('save', articleData)
  } catch (error) {
    console.error('保存文章失败:', error)
    ElMessage.error('保存文章失败')
  } finally {
    saving.value = false
  }
}

// 处理关闭
const handleClose = async () => {
  if (saveStatus.value === '有未保存的更改') {
    try {
      await ElMessageBox.confirm(
        '有未保存的更改，确定要关闭吗？',
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        }
      )
    } catch {
      return
    }
  }
  
  emit('close')
}

// 获取分类列表
const fetchCategories = async () => {
  try {
    const response = await axios.get('/api/articles/categories')
    categories.value = response.data.categories.map(cat => cat.path)
  } catch (error) {
    console.error('获取分类失败:', error)
  }
}

// 组件挂载
onMounted(() => {
  fetchCategories()
})
</script>

<style scoped>
.article-editor-dialog {
  margin-top: 5vh !important;
}

.editor-container {
  height: 70vh;
  display: flex;
  flex-direction: column;
}

.article-info {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.summary-actions {
  margin-top: 10px;
  text-align: right;
}

.editor-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  overflow: hidden;
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  background: #f5f7fa;
  border-bottom: 1px solid #dcdfe6;
}

.editor-tabs {
  display: flex;
  gap: 5px;
}

.editor-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.save-status {
  font-size: 12px;
  color: #909399;
}

.editor-content {
  flex: 1;
  display: flex;
  min-height: 0;
}

.editor-content.split-view {
  display: flex;
}

.edit-area,
.preview-area {
  flex: 1;
  min-height: 0;
}

.split-view .edit-area {
  border-right: 1px solid #dcdfe6;
}

.markdown-editor {
  width: 100%;
  height: 100%;
  border: none;
  outline: none;
  padding: 20px;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.6;
  resize: none;
  background: #fff;
}

.preview-area {
  overflow-y: auto;
  background: #fff;
}

.markdown-body {
  padding: 20px;
  max-width: none;
}

.dialog-footer {
  text-align: right;
}

:deep(.el-dialog) {
  border-radius: 15px;
}

:deep(.el-dialog__body) {
  padding: 20px;
}
</style>

