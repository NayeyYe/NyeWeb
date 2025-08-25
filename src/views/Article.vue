<template>
  <div class="article-container">
    <el-card class="article-card">
      <div v-html="articleContent" class="markdown-body"></div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import MarkdownIt from 'markdown-it'
import mdKatex from '@iktakahiro/markdown-it-katex'
import hljs from 'markdown-it-highlightjs'

// 导入所需样式
import 'katex/dist/katex.min.css'
import 'highlight.js/styles/github.css'
import 'github-markdown-css/github-markdown.css'

// 初始化 markdown-it 并使用插件
const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true
})
  .use(mdKatex)
  .use(hljs)

// 保存原始的图片渲染规则
const defaultImageRenderer = md.renderer.rules.image
// 重写图片渲染规则以处理相对路径
md.renderer.rules.image = function (tokens, idx, options, env, self) {
  const token = tokens[idx]
  const srcIndex = token.attrIndex('src')
  const src = token.attrGet('src')

  // 检查是否为相对路径
  if (src && src.startsWith('./')) {
    // 将相对路径转换为基于 /articles/knowledge/ 的绝对路径
    // 例如：'./assets/img.png' -> '/articles/knowledge/assets/img.png'
    const newSrc = `/articles/knowledge/${src.substring(2)}`
    token.attrSet('src', newSrc)
  }

  // 调用原始的渲染器来渲染 <img> 标签
  return defaultImageRenderer(tokens, idx, options, env, self)
}

const route = useRoute()
const articleContent = ref('')

const fetchArticle = async (slug) => {
  if (!slug) return
  try {
    // 注意：路径是相对于 public 文件夹的
    const response = await fetch(`/articles/knowledge/${slug}.md`)

    if (!response.ok) {
      throw new Error(`服务器响应错误: ${response.status}`)
    }

    const markdownText = await response.text()

    // 检查返回的是否是HTML（SPA回退机制可能导致此问题）
    if (markdownText.trim().toLowerCase().startsWith('<!doctype html>') || markdownText.trim().startsWith('<script')) {
      throw new Error('获取到的是HTML文件，而不是Markdown。请检查文章文件路径是否正确。')
    }

    articleContent.value = md.render(markdownText)
  } catch (error) {
    console.error('获取文章失败:', error)
    articleContent.value = `<h1>文章加载失败</h1><p><strong>原因:</strong> ${error.message}</p><p>请确认 <code>public/articles/knowledge/${slug}.md</code> 文件存在且路径正确。</p>`
  }
}

onMounted(() => {
  fetchArticle(route.params.slug)
})

// 监听路由变化，以便在同一页面切换文章时重新加载
watch(
  () => route.params.slug,
  (newSlug) => {
    fetchArticle(newSlug)
  }
)
</script>

<style scoped>
.article-container {
  padding: 100px 20px 20px;
  max-width: 900px;
  margin: 0 auto;
}
.article-card {
  padding: 20px;
  border-radius: 15px;
}
.markdown-body {
  /* 确保背景透明以适应卡片背景 */
  background-color: transparent;
  padding: 1rem; /* 为内容提供一些内边距 */
}
</style>
