<template>
  <div class="article-container">
    <div v-if="articleNotFound" class="not-found">
      <h1>404 - 文章未找到</h1>
      <p>抱歉，您要查找的文章不存在或链接已更改。</p>
      <router-link to="/knowledge">返回文章列表</router-link>
    </div>
    <article v-else class="markdown-body">
      <h1>{{ articleTitle }}</h1>
      <div v-html="articleContent"></div>
    </article>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import articlesData from '@/data/articles.json'

// Markdown-it and plugins
import markdownit from 'markdown-it'
import mdKatex from '@iktakahiro/markdown-it-katex'
import hljs from 'highlight.js'

// CSS imports
import 'highlight.js/styles/github.css'
import 'github-markdown-css/github-markdown.css'
import 'katex/dist/katex.min.css'

const route = useRoute()
const articleContent = ref('')
const articleTitle = ref('')
const articleNotFound = ref(false)

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

// 修复图片相对路径问题
const defaultImageRenderer = md.renderer.rules.image
md.renderer.rules.image = function (tokens, idx, options, env, self) {
  const token = tokens[idx]
  const src = token.attrGet('src')
  if (src && src.startsWith('./')) {
    const articlePath = env.articlePath || ''
    // 确保路径正确拼接，即使分类为空
    const basePath = articlePath ? `/articles/knowledge/${articlePath}` : '/articles/knowledge'
    token.attrSet('src', `${basePath}/${src.substring(2)}`)
  }
  return defaultImageRenderer(tokens, idx, options, env, self)
}

const fetchArticle = async () => {
  articleNotFound.value = false
  articleContent.value = ''
  articleTitle.value = ''

  const slug = route.params.slug
  if (!slug) {
    articleNotFound.value = true
    return
  }

  // 1. 在JSON数据中通过slug查找文章
  const articleData = articlesData.find(a => a.slug === slug)

  if (articleData) {
    articleTitle.value = articleData.title
    const categoryPath = articleData.category
    // 2. 根据分类和slug构建文件���公共URL路径
    const fullPath = categoryPath ? `${categoryPath}/${articleData.slug}` : articleData.slug

    try {
      // 3. 使用 fetch 从 public 目录获取文章内容
      const response = await fetch(`/articles/knowledge/${fullPath}.md`)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const markdownText = await response.text()

      // 4. 渲染Markdown，并传入分类路径用于图片解析
      const env = { articlePath: categoryPath }
      articleContent.value = md.render(markdownText, env)
    } catch (e) {
      console.error(`加载文章内容失败: ${fullPath}.md`, e)
      articleNotFound.value = true
    }
  } else {
    console.error('在JSON数据中未找到文章:', { slug })
    articleNotFound.value = true
  }
}

onMounted(fetchArticle)
watch(() => route.params.slug, fetchArticle)
</script>

<style scoped>
.article-container {
  max-width: 800px;
  margin: 100px auto 40px;
  padding: 20px;
}

.markdown-body {
  padding: 2em;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.not-found {
  text-align: center;
  padding: 40px;
  color: #606266;
}
</style>
