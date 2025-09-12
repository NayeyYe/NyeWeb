<template>
  <el-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    title="文章预览"
    width="80%"
    class="article-preview-dialog"
    :before-close="handleClose"
  >
    <div v-if="article" class="preview-container">
      <!-- 文章信息 -->
      <div class="article-meta">
        <h1 class="article-title">{{ article.title }}</h1>
        <div class="meta-info">
          <el-tag v-if="article.category" type="info" class="category-tag">
            <el-icon><Folder /></el-icon>
            {{ article.category }}
          </el-tag>
          <span class="date">
            <el-icon><Calendar /></el-icon>
            {{ article.date || '未设置发布日期' }}
          </span>
          <span class="slug">
            <el-icon><Link /></el-icon>
            {{ article.slug }}
          </span>
        </div>
        <div v-if="article.tags && article.tags.length" class="tags-container">
          <el-tag
            v-for="tag in article.tags"
            :key="tag"
            size="small"
            class="tag-item"
            effect="plain"
          >
            <el-icon><Tag /></el-icon>
            {{ tag }}
          </el-tag>
        </div>
        <p v-if="article.summary" class="article-summary">{{ article.summary }}</p>
      </div>

      <!-- 加载状态 -->
      <div v-if="contentLoading" class="loading-container">
        <el-skeleton :rows="8" animated />
        <div class="loading-text">正在加载文章内容...</div>
      </div>

      <!-- 错误状态 -->
      <div v-else-if="contentError" class="error-container">
        <el-result
          icon="warning"
          title="加载失败"
          :sub-title="contentError"
        >
          <template #extra>
            <el-button type="primary" @click="loadArticleContent">
              <el-icon><Refresh /></el-icon>
              重新加载
            </el-button>
          </template>
        </el-result>
      </div>

      <!-- 文章内容 -->
      <div v-else-if="renderedContent" class="article-content">
        <div class="content-toolbar">
          <div class="toolbar-left">
            <el-button-group size="small">
              <el-button
                :type="viewMode === 'content' ? 'primary' : ''"
                @click="viewMode = 'content'"
              >
                <el-icon><Document /></el-icon>
                内容视图
              </el-button>
              <el-button
                :type="viewMode === 'source' ? 'primary' : ''"
                @click="viewMode = 'source'"
              >
                <el-icon><Edit /></el-icon>
                源码视图
              </el-button>
            </el-button-group>
          </div>
          <div class="toolbar-right">
            <el-button size="small" @click="copyContent">
              <el-icon><CopyDocument /></el-icon>
              复制内容
            </el-button>
            <el-button size="small" type="primary" @click="openInNewTab">
              <el-icon><View /></el-icon>
              新窗口打开
            </el-button>
          </div>
        </div>

        <!-- 渲染内容 -->
        <div v-show="viewMode === 'content'" class="markdown-body" v-html="renderedContent"></div>

        <!-- 源码内容 -->
        <div v-show="viewMode === 'source'" class="source-view">
          <el-input
            :model-value="rawContent"
            type="textarea"
            :rows="20"
            readonly
            class="source-textarea"
          />
        </div>
      </div>

      <!-- 无内容状态 -->
      <div v-else class="no-content">
        <el-empty description="暂无内容">
          <el-button type="primary" @click="loadArticleContent">
            <el-icon><Refresh /></el-icon>
            重新加载
          </el-button>
        </el-empty>
      </div>
    </div>

    <!-- 对话框底部 -->
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">关闭</el-button>
        <el-button type="primary" @click="editArticle" v-if="article">
          <el-icon><Edit /></el-icon>
          编辑文章
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Folder, Calendar, Link, Document, Edit,
  CopyDocument, View, Refresh
} from '@element-plus/icons-vue'
import markdownit from 'markdown-it'
import mdAnchor from 'markdown-it-anchor'
import slugify from 'slugify'
import mdKatex from '@iktakahiro/markdown-it-katex'
import hljs from 'highlight.js'
import mermaid from 'mermaid'

// CSS imports
import 'highlight.js/styles/github.css'
import 'github-markdown-css/github-markdown.css'
import 'katex/dist/katex.min.css'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  article: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['update:modelValue', 'edit'])

// 响应式数据
const contentLoading = ref(false)
const contentError = ref('')
const renderedContent = ref('')
const rawContent = ref('')
const viewMode = ref('content')

// 初始化 Mermaid
mermaid.initialize({
  startOnLoad: false,
  theme: 'default',
  securityLevel: 'loose'
})

// 配置 markdown-it
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
}).use(mdKatex)
  .use(mdAnchor, {
    permalink: mdAnchor.permalink.ariaHidden({
      placement: 'before',
      symbol: '¶'
    }),
    level: [1, 2, 3, 4, 5, 6],
    slugify: s => slugify(s, { lower: true, strict: true })
  })

// 自定义代码块渲染，支持 Mermaid
const defaultFenceRenderer = md.renderer.rules.fence;
md.renderer.rules.fence = (tokens, idx, options, env, self) => {
  const token = tokens[idx];
  const language = token.info.trim().split(/\s+/)[0];
  if (language === 'mermaid') {
    return `<div class="mermaid">${token.content}</div>`;
  }
  return defaultFenceRenderer(tokens, idx, options, env, self);
};

// 修复图片相对路径问题
const defaultImageRenderer = md.renderer.rules.image
md.renderer.rules.image = function (tokens, idx, options, env, self) {
  const token = tokens[idx]
  const src = token.attrGet('src')
  if (src && src.startsWith('./')) {
    const articlePath = env.articlePath || ''
    const basePath = articlePath ? `/articles/knowledge/${articlePath}` : '/articles/knowledge'
    token.attrSet('src', `${basePath}/${src.substring(2)}`)
  }
  return defaultImageRenderer(tokens, idx, options, env, self)
}

// 加载文章内容
const loadArticleContent = async () => {
  if (!props.article) {
    renderedContent.value = ''
    rawContent.value = ''
    return
  }

  contentLoading.value = true
  contentError.value = ''
  
  try {
    const categoryPath = props.article.category
    const fullPath = categoryPath ? `${categoryPath}/${props.article.slug}` : props.article.slug

    const response = await fetch(`/articles/knowledge/${fullPath}.md`)
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }
    
    const markdownText = await response.text()
    rawContent.value = markdownText

    // 渲染Markdown，并传入分类路径用于图片解析
    const env = { articlePath: categoryPath }
    renderedContent.value = md.render(markdownText, env)

    // DOM更新后渲染 Mermaid 图表
    await nextTick()
    try {
      const mermaidElements = document.querySelectorAll('.article-preview-dialog .mermaid')
      if (mermaidElements.length > 0) {
        await mermaid.run()
      }
    } catch (mermaidError) {
      console.warn('Mermaid 渲染失败:', mermaidError)
    }

  } catch (error) {
    console.error('加载文章内容失败:', error)
    contentError.value = `加载文章内容失败: ${error.message}`
    rawContent.value = ''
    renderedContent.value = ''
  } finally {
    contentLoading.value = false
  }
}

// 复制内容
const copyContent = async () => {
  const content = viewMode.value === 'content'
    ? document.querySelector('.article-preview-dialog .markdown-body')?.innerText || ''
    : rawContent.value

  if (!content) {
    ElMessage.warning('暂无内容可复制')
    return
  }

  try {
    await navigator.clipboard.writeText(content)
    ElMessage.success('内容已复制到剪贴板')
  } catch (error) {
    console.error('复制失败:', error)
    ElMessage.error('复制失败，请手动选择复制')
  }
}

// 在新窗口打开
const openInNewTab = () => {
  if (!props.article) return

  const categoryPath = props.article.category
  const url = categoryPath
    ? `/knowledge/${categoryPath}/${props.article.slug}`
    : `/knowledge/${props.article.slug}`

  window.open(url, '_blank')
}

// 编辑文章
const editArticle = () => {
  emit('edit', props.article)
  handleClose()
}

// 处理关闭
const handleClose = () => {
  emit('update:modelValue', false)
  // 重置状态
  contentError.value = ''
  renderedContent.value = ''
  rawContent.value = ''
  viewMode.value = 'content'
}

// 监听文章变化
watch(() => props.article, () => {
  if (props.modelValue && props.article) {
    loadArticleContent()
  }
}, { immediate: true })

// 监听对话框打开状态
watch(() => props.modelValue, (newVal) => {
  if (newVal && props.article) {
    loadArticleContent()
  } else if (!newVal) {
    handleClose()
  }
})
</script>

<style scoped>
.article-preview-dialog :deep(.el-dialog) {
  border-radius: 12px;
  overflow: hidden;
  max-height: 90vh;
}

.article-preview-dialog :deep(.el-dialog__body) {
  padding: 0;
  max-height: calc(90vh - 120px);
  overflow-y: auto;
}

.preview-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.article-meta {
  padding: 24px 32px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-bottom: 1px solid #ebeef5;
}

.article-title {
  margin: 0 0 16px 0;
  font-size: 28px;
  font-weight: 700;
  line-height: 1.2;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.meta-info {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.meta-info > span {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  opacity: 0.9;
}

.category-tag {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
}

.category-tag :deep(.el-icon) {
  margin-right: 4px;
}

.tags-container {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 12px;
}

.tag-item {
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
}

.tag-item :deep(.el-icon) {
  margin-right: 4px;
}

.article-summary {
  margin: 0;
  font-size: 16px;
  line-height: 1.6;
  opacity: 0.95;
  font-style: italic;
}

.loading-container {
  padding: 32px;
}

.loading-text {
  text-align: center;
  color: #909399;
  margin-top: 16px;
}

.error-container {
  padding: 32px;
}

.no-content {
  padding: 60px 32px;
  text-align: center;
}

.article-content {
  flex: 1;
  background: #fff;
  display: flex;
  flex-direction: column;
}

.content-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 24px;
  background: #f8f9fa;
  border-bottom: 1px solid #ebeef5;
}

.toolbar-left, .toolbar-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.markdown-body {
  flex: 1;
  padding: 32px;
  line-height: 1.8;
  color: #333;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  overflow-y: auto;
}

.source-view {
  flex: 1;
  padding: 16px;
}

.source-textarea :deep(.el-textarea__inner) {
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 13px;
  line-height: 1.5;
  border: 1px solid #dcdfe6;
  border-radius: 8px;
}

.dialog-footer {
  text-align: right;
}

/* Markdown 样式增强 */
:deep(.markdown-body h1),
:deep(.markdown-body h2),
:deep(.markdown-body h3),
:deep(.markdown-body h4),
:deep(.markdown-body h5),
:deep(.markdown-body h6) {
  padding-left: 1rem;
  border-left: 4px solid #409eff;
  margin-top: 2rem;
  margin-bottom: 1rem;
  font-weight: 600;
  position: relative;
}

:deep(.markdown-body h1) { font-size: 2em; }
:deep(.markdown-body h2) { font-size: 1.6em; }
:deep(.markdown-body h3) { font-size: 1.3em; }

:deep(.markdown-body pre) {
  background-color: #f6f8fa;
  border-radius: 8px;
  padding: 16px;
  margin: 16px 0;
  overflow-x: auto;
  border: 1px solid #e1e4e8;
}

:deep(.markdown-body code) {
  background-color: #f0f2f5;
  color: #c7254e;
  padding: 2px 6px;
  margin: 0 2px;
  font-size: 90%;
  border-radius: 4px;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
}

:deep(.markdown-body blockquote) {
  padding: 1em 1.5em;
  color: #6a737d;
  border-left: 0.3em solid #409eff;
  margin: 1.5em 0;
  background-color: #f6f8fa;
  border-radius: 0 8px 8px 0;
}

:deep(.markdown-body table) {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5rem 0;
  border-radius: 8px;
  border: 1px solid #d0d7de;
  overflow: hidden;
}

:deep(.markdown-body th),
:deep(.markdown-body td) {
  padding: 0.75rem 1rem;
  border: 1px solid #d0d7de;
  text-align: left;
}

:deep(.markdown-body th) {
  font-weight: 600;
  background-color: #f6f8fa;
}

:deep(.markdown-body tr:nth-child(2n)) {
  background-color: #f8f9fa;
}

:deep(.header-anchor) {
  opacity: 0;
  position: absolute;
  left: -0.7em;
  text-decoration: none;
  transition: opacity 0.2s;
  color: #409eff;
}

:deep(h1:hover .header-anchor),
:deep(h2:hover .header-anchor),
:deep(h3:hover .header-anchor),
:deep(h4:hover .header-anchor),
:deep(h5:hover .header-anchor),
:deep(h6:hover .header-anchor) {
  opacity: 1;
}

/* Mermaid 图表样式 */
:deep(.mermaid) {
  margin: 1.5em 0;
  text-align: center;
  background: #fafafa;
  padding: 1em;
  border-radius: 8px;
  border: 1px solid #eee;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .article-meta {
    padding: 16px 20px;
  }

  .article-title {
    font-size: 24px;
  }

  .meta-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .content-toolbar {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }

  .markdown-body {
    padding: 20px;
  }
}
</style>
