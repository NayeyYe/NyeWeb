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
    // 假设资源文件夹位于 `src/articles/knowledge/assets`
    // 将 './assets/image.png' 转换为 Vite 在开发时能理解的绝对路径
    token.attrSet('src', `/articles/knowledge/${src.substring(2)}`)
  }
  return defaultImageRenderer(tokens, idx, options, env, self)
}

const fetchArticle = async () => {
  articleNotFound.value = false
  articleContent.value = ''
  articleTitle.value = ''

  const pathParts = route.params.path || []

  if (pathParts.length > 0) {
    const slug = pathParts[pathParts.length - 1]
    const category = pathParts.slice(0, -1).join('/')

    // 在JSON数据中查找匹配的文章
    const articleData = articlesData.find(a => a.slug === slug && a.category === category)

    if (articleData) {
      articleTitle.value = articleData.title
      try {
        // 假设所有Markdown文件都平铺在 'src/articles/knowledge' 目录下
        const module = await import(`../../articles/knowledge/${slug}.md?raw`)
        articleContent.value = md.render(module.default)
      } catch (e) {
        console.error(`加载文章内容失败: ${slug}.md`, e)
        articleNotFound.value = true
      }
    } else {
      articleNotFound.value = true
    }
  } else {
    articleNotFound.value = true
  }
}

onMounted(fetchArticle)
watch(() => route.params.path, fetchArticle)
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
