<template>
  <div class="project-container">
    <div v-if="projectNotFound" class="not-found">
      <h1>404 - 项目未找到</h1>
      <p>抱歉，您要查找的项目不存在或链接已更改。</p>
      <router-link to="/projects">返回项目列表</router-link>
    </div>
    <article v-else class="markdown-body" v-html="projectContent"></article>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import projectsData from '@/data/projects.json'

// Markdown-it and plugins
import markdownit from 'markdown-it'
import mdKatex from '@iktakahiro/markdown-it-katex'
import hljs from 'highlight.js'

// CSS imports
import 'highlight.js/styles/github.css'
import 'github-markdown-css/github-markdown.css'
import 'katex/dist/katex.min.css'

const route = useRoute()
const projectContent = ref('')
const projectNotFound = ref(false)

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
    // 项目文件中的图片相对于 /articles/projects/ 目录
    token.attrSet('src', `/articles/projects/${src.substring(2)}`)
  }
  return defaultImageRenderer(tokens, idx, options, env, self)
}

const fetchProject = async () => {
  projectNotFound.value = false
  projectContent.value = ''

  const slug = route.params.slug
  if (!slug) {
    projectNotFound.value = true
    return
  }

  // 1. 在JSON数据中通过slug查找项目
  const projectData = projectsData.find(p => p.slug === slug)

  if (projectData) {
    try {
      // 2. 使用 fetch 从 public/articles/projects 目录获取项目内容
      const response = await fetch(`/articles/projects/${projectData.slug}.md`)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const markdownText = await response.text()

      // 3. 渲染Markdown
      projectContent.value = md.render(markdownText)
    } catch (e) {
      console.error(`加载项目内容失败: ${projectData.slug}.md`, e)
      projectNotFound.value = true
    }
  } else {
    console.error('在JSON数据中未找到项目:', { slug })
    projectNotFound.value = true
  }
}

onMounted(fetchProject)
watch(() => route.params.slug, fetchProject)
</script>

<style scoped>
.project-container {
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