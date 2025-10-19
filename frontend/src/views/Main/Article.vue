<template>
  <div class="page-container">
    <div v-if="articleNotFound" class="not-found">
      <h1>404 - 文章未找到</h1>
      <p>抱歉，您要查找的文章不存在或链接已更改。</p>
      <router-link to="/knowledge">返回文章列表</router-link>
    </div>
    <div v-else class="content-layout">
      <!-- 左侧展开按钮 -->
      <el-button 
        v-if="leftCollapsed" 
        class="expand-btn expand-btn-left" 
        circle 
        @click="toggleLeft"
      >
        <el-icon>
          <ArrowRight />
        </el-icon>
      </el-button>

      <!-- 左侧文章分类树 -->
      <aside class="sidebar sidebar-left" :class="{ collapsed: leftCollapsed }">
        <div v-show="!leftCollapsed" class="sidebar-content">
          <ArticleCategoryTree 
            :articles="[]" 
            :show-collapse-button="true"
            :show-articles="true"
            @category-selected="handleCategorySelected"
            @article-selected="handleArticleSelected"
            @collapse="toggleLeft"
          />
        </div>
      </aside>

      <!-- 主内容区 -->
      <main class="main-content">
        <article class="markdown-body">
          <div v-html="articleContent"></div>
        </article>
      </main>

      <!-- 右侧文章大纲 -->
      <aside class="sidebar sidebar-right" :class="{ collapsed: rightCollapsed }">
        <div v-show="!rightCollapsed" class="sidebar-content">
          <Outline 
            v-if="headings.length" 
            :active-id="activeHeadingId" 
            :outline="headings"
            :show-collapse-button="true"
            @collapse="toggleRight"
          />
          <el-empty v-else description="暂无大纲" />
        </div>
      </aside>

      <!-- 右侧展开按钮 -->
      <el-button 
        v-if="rightCollapsed" 
        class="expand-btn expand-btn-right" 
        circle 
        @click="toggleRight"
      >
        <el-icon>
          <ArrowLeft />
        </el-icon>
      </el-button>
    </div>
  </div>
</template>

<script setup>
import {nextTick, onMounted, onUnmounted, ref, watch} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import axios from 'axios'
import Outline from '@/components/Main/Outline.vue'
import ArticleCategoryTree from '@/components/Main/Article/ArticleCategoryTree.vue'
import mermaid from 'mermaid'
import {ArrowLeft, ArrowRight} from '@element-plus/icons-vue'

// Markdown-it and plugins
import markdownit from 'markdown-it'
import mdAnchor from 'markdown-it-anchor'
import slugify from 'slugify'
import mdKatex from '@iktakahiro/markdown-it-katex'
import hljs from 'highlight.js'
import mdTable from 'markdown-it-multimd-table'

// CSS imports
import 'highlight.js/styles/github.css'
import 'github-markdown-css/github-markdown.css'
import 'katex/dist/katex.min.css'

// 初始化 Mermaid
mermaid.initialize({startOnLoad: false, theme: 'default'})

const route = useRoute()
const router = useRouter()
const articleContent = ref('')
const articleTitle = ref('')
const articleNotFound = ref(false)
const headings = ref([])
const activeHeadingId = ref('')
const leftCollapsed = ref(false)
const rightCollapsed = ref(false)
let observer = null

const API_BASE_URL = '/api'

const toggleLeft = () => {
  leftCollapsed.value = !leftCollapsed.value
}

const toggleRight = () => {
  rightCollapsed.value = !rightCollapsed.value
}

const handleCategorySelected = (path) => {
  console.log('分类选择:', path)
  // 这里可以添加分类选择后的逻辑，比如筛选文章列表等
}

const handleArticleSelected = (articleInfo) => {
  console.log('文章选择:', articleInfo)
  // 跳转到选中的文章
  if (articleInfo.category) {
    router.push(`/article/${articleInfo.category}/${articleInfo.slug}`)
  } else {
    router.push(`/article/${articleInfo.slug}`)
  }
}

// Markdown-it 配置
const md = markdownit({
  html: true,
  linkify: true,
  typographer: true,
  tables: true, // 启用表格支持
  breaks: true, // 启用换行符转换
  highlight: function (str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return '<pre class="hljs"><code>' +
            hljs.highlight(str, {language: lang, ignoreIllegals: true}).value +
            '</code></pre>';
      } catch (__) {
      }
    }
    return '<pre class="hljs"><code>' + md.utils.escapeHtml(str) + '</code></pre>';
  }
}).use(mdKatex, {
  throwOnError: false,
  errorColor: '#cc0000',
  delimiters: [
    {left: '$$', right: '$$', display: true},
    {left: '$', right: '$', display: false},
    {left: '\\(', right: '\\)', display: false},
    {left: '\\[', right: '\\]', display: true}
  ]
})
    .use(mdAnchor, {
      permalink: true,
      level: [1, 2, 3, 4, 5, 6],
      slugify: s => {
        let slug = slugify(s, {lower: true, locale: 'zh'});
        // 如果slug为空或以减号开头，生成正数ID
        if (!slug || slug.startsWith('-')) {
          slug = 'heading-' + Math.abs(Math.floor(Math.random() * 1000000));
        }
        return slug;
      },
      permalinkSymbol: '',
      permalinkBefore: true,
      permalinkClass: 'header-anchor'
    })
    .use(mdTable, {
      multiline: true,
      rowspan: true,
      headerless: true
    })

// 自定义代码块渲染，支持 Mermaid
const defaultFenceRenderer = md.renderer.rules.fence;
md.renderer.rules.fence = (tokens, idx, options, env, self) => {
  const token = tokens[idx];
  const language = token.info.trim().split(/\s+/)[0];
  if (language === 'mermaid') {
    return `<div class="mermaid">${token.content}</div>`;
  }
  const rawCode = defaultFenceRenderer(tokens, idx, options, env, self);

  return `
    <div class="code-block-wrapper">
      <div class="code-block-header">
        <div class="mac-dots">
          <span class="dot red"></span>
          <span class="dot yellow"></span>
          <span class="dot green"></span>
        </div>
        <span class="language-name">${language}</span>
        <button class="copy-code-btn" title="复制">复制</button>
      </div>
      ${rawCode}
    </div>
  `;
};

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

const setupCopyButtons = () => {
  document.querySelectorAll('.copy-code-btn').forEach(button => {
    button.addEventListener('click', () => {
      const wrapper = button.closest('.code-block-wrapper');
      const code = wrapper.querySelector('code');
      if (code) {
        navigator.clipboard.writeText(code.innerText).then(() => {
          button.textContent = '成功复制!';
          setTimeout(() => {
            button.textContent = '复制';
          }, 2000);
        }).catch(err => {
          console.error('复制失败: ', err);
          button.textContent = '失败';
        });
      }
    });
  });
};

const setupIntersectionObserver = () => {
  // 清理旧的观察者
  if (observer) {
    observer.disconnect();
  }

  const headingElements = document.querySelectorAll('.markdown-body h1, .markdown-body h2, .markdown-body h3, .markdown-body h4, .markdown-body h5, .markdown-body h6');

  observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        activeHeadingId.value = entry.target.id;
      }
    });
  }, {
    rootMargin: '0px 0px -80% 0px', // 当标题进入视口顶部20%时触发
    threshold: 0
  });

  headingElements.forEach(el => observer.observe(el));
};

const fetchArticle = async () => {
  articleNotFound.value = false
  articleContent.value = ''
  articleTitle.value = ''
  headings.value = []

  const slug = route.params.slug
  if (!slug) {
    articleNotFound.value = true
    return
  }

  try {
    let articleData = null

    // 检查是否有分类参数
    if (route.params.category) {
      // 如果URL包含分类，使用带分类的API
      const category = Array.isArray(route.params.category)
          ? route.params.category.join('/')
          : route.params.category

      const response = await axios.get(`${API_BASE_URL}/articles/${category}/${slug}`, {
        timeout: 10000,
        headers: {
          'Accept': 'application/json'
        }
      })
      articleData = response.data
    } else {
      // 如果URL不包含分类，使用普通的API
      const response = await axios.get(`${API_BASE_URL}/articles/${slug}`, {
        timeout: 10000,
        headers: {
          'Accept': 'application/json'
        }
      })
      articleData = response.data
    }

    if (articleData) {
      articleTitle.value = articleData.title
      const categoryPath = articleData.category

      // 根据分类和slug构建文件路径
      const fullPath = categoryPath ? `${categoryPath}/${articleData.slug}` : articleData.slug

      try {
        // 使用 fetch 从 dist 目录获取文章内容
        const response = await fetch(`/articles/knowledge/${fullPath}.md`)
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        const markdownText = await response.text()

        // 渲染Markdown，并传入分类路径用于图片解析
        const env = {articlePath: categoryPath}
        articleContent.value = md.render(markdownText, env)

        // DOM更新后提取标题、设置复制按钮和滚动监听
        await nextTick()
        
        // 从DOM中提取标题，确保ID与实际渲染的ID一致
        const headingElements = document.querySelectorAll('.markdown-body h1, .markdown-body h2, .markdown-body h3, .markdown-body h4, .markdown-body h5, .markdown-body h6')
        const extractedHeadings = []
        headingElements.forEach((element, index) => {
          let id = element.id
          // 如果ID为空或为负数，使用基于索引的确定性ID
          if (!id || id.startsWith('-')) {
            id = 'heading-' + index
            element.id = id // 确保DOM中的ID也被更新
          }
          extractedHeadings.push({
            level: parseInt(element.tagName.substring(1), 10),
            text: element.textContent.replace('¶', '').trim(), // 移除锚点符号
            id: id
          })
        })
        headings.value = extractedHeadings

        setupCopyButtons()
        setupIntersectionObserver()
        // 渲染 Mermaid 图表
        mermaid.init(undefined, document.querySelectorAll('.mermaid'))

        console.log(`成功加载文章: ${articleData.title}`)
      } catch (e) {
        console.error(`加载文章内容失败: ${fullPath}.md`, e)
        articleNotFound.value = true
      }
    } else {
      articleNotFound.value = true
    }
  } catch (error) {
    console.error('获取文章信息失败:', error)
    articleNotFound.value = true
  }
}

onMounted(fetchArticle)
watch(() => route.params.slug, fetchArticle)

onUnmounted(() => {
  if (observer) {
    observer.disconnect();
  }
});
</script>

<style scoped>
.page-container {
  max-width: 1400px;
  margin: 100px auto 40px;
  padding: 20px 28px;
}

.content-layout {
  display: flex;
  gap: 24px;
  align-items: flex-start;
}

.sidebar {
  position: relative;
  transition: width 0.3s ease;
  overflow: hidden; /* 防止外部容器产生滚动条 */
  height: calc(100vh - 140px); /* 固定高度，防止外部滚动 */
}

.sidebar-left {
  width: 300px;
}

.sidebar-right {
  width: 280px;
}

.sidebar.collapsed {
  width: 0;
  overflow: hidden;
}

.sidebar-content {
  position: fixed;
  top: 100px;
  bottom: 20px;
  overflow-y: auto;
  overflow-x: hidden;
  z-index: 50;
  height: calc(100vh - 120px);
}

.sidebar-left .sidebar-content {
  left: calc(50vw - 720px + 20px);
  width: 300px;
}

.sidebar-right .sidebar-content {
  right: calc(50vw - 720px + 20px);
  width: 280px;
}

.main-content {
  flex: 1;
  min-width: 0;
}

.markdown-body {
  padding: 2em 2.5em;
  background-color: #fff;
  border-radius: 15px;
  box-shadow: 0 4px 12px 0 rgba(0, 0, 0, 0.05);
  position: relative;
  line-height: 1.8;
  color: #333;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
}

.not-found {
  text-align: center;
  padding: 40px;
  color: #606266;
}

/* 隐藏默认的锚点符号，因为我们只关心ID的生成 */
:deep(.header-anchor) {
  opacity: 0;
  position: absolute;
  left: -0.7em;
  text-decoration: none;
  transition: opacity 0.2s;
}

:deep(h1:hover .header-anchor),
:deep(h2:hover .header-anchor),
:deep(h3:hover .header-anchor),
:deep(h4:hover .header-anchor),
:deep(h5:hover .header-anchor),
:deep(h6:hover .header-anchor) {
  opacity: 1;
}

/* --- 美化样式 --- */

/* 标题美化 */
:deep(h1),
:deep(h2),
:deep(h3),
:deep(h4),
:deep(h5),
:deep(h6) {
  padding-left: 1rem;
  border-left: 5px solid #409eff;
  margin-top: 2.4rem;
  margin-bottom: 1.4rem;
  font-weight: 600;
}

:deep(h1) {
  font-size: 2em;
}

:deep(h2) {
  font-size: 1.6em;
}

:deep(h3) {
  font-size: 1.3em;
}

/* 代码块容器 */
:deep(.code-block-wrapper) {
  position: relative;
  margin: 1.5rem 0;
  border-radius: 8px;
  overflow: hidden;
  background-color: #f8f9fa; /* 浅色背景 */
  border: 1px solid #dee2e6;
  box-shadow: none;
}

/* 代码块头部 */
:deep(.code-block-header) {
  display: flex;
  align-items: center;
  padding: 0.4em 1em; /* 减小垂直内边距 */
  background-color: #e9ecef; /* 稍暗的头部背景 */
  border-bottom: 1px solid #dee2e6;
}

:deep(.mac-dots) {
  display: flex;
  gap: 8px;
  margin-right: 1em;
}

:deep(.dot) {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

:deep(.dot.red) {
  background-color: #ff5f56;
}

:deep(.dot.yellow) {
  background-color: #ffbd2e;
}

:deep(.dot.green) {
  background-color: #27c93f;
}

:deep(.language-name) {
  flex-grow: 1;
  text-align: left;
  font-size: 13px;
  font-family: sans-serif;
  color: #6c757d; /* 深色文字以适应浅色背景 */
  text-transform: uppercase;
}

/* 复制按钮 */
:deep(.copy-code-btn) {
  padding: 4px 10px;
  font-size: 12px;
  background-color: #f8f9fa;
  border: 1px solid #ced4da;
  border-radius: 5px;
  cursor: pointer;
  color: #495057;
  transition: all 0.2s;
}

:deep(.copy-code-btn:hover) {
  background-color: #e9ecef;
  color: #212529;
}

/* 代码块 */
:deep(pre) {
  background-color: transparent;
  padding: 1em 1.5em; /* 调整内边距 */
  margin: 0;
  border-radius: 0;
  overflow-x: auto;
  border: none;
  /* 确保代码块在窄屏幕上可以横向滚动 */
  white-space: pre;
  word-wrap: normal;
}

/* 行内代码 */
:deep(:not(pre) > code) {
  background-color: #f0f2f5;
  color: #c7254e;
  padding: .2em .4em;
  margin: 0 2px;
  font-size: 90%;
  border-radius: 4px;
}

/* 引用 */
:deep(blockquote) {
  padding: 0.5em 1.2em;
  color: #6a737d;
  border-left: 0.3em solid #d0d7de;
  margin-left: 0;
  background-color: #f6f8fa;
  border-radius: 0 8px 8px 0;
}

/* 链接 */
:deep(.markdown-body a) {
  color: #0969da;
  text-decoration: none;
  font-weight: 500;
}

:deep(.markdown-body a:hover) {
  text-decoration: underline;
}

/* 表格 */
:deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5rem 0;
  display: block;
  overflow: auto;
  border-spacing: 0;
  border-radius: 8px;
  border: 1px solid #d0d7de;
}

:deep(th),
:deep(td) {
  padding: 0.75rem 1rem;
  border: 1px solid #d0d7de;
}

:deep(th) {
  font-weight: 600;
  background-color: #f6f8fa;
}

:deep(tr:nth-child(2n)) {
  background-color: #f6f8fa;
}
/* 数学公式样式 */
:deep(.katex) {
  font: normal 1.21em KaTeX_Main, Times New Roman, serif;
  line-height: 1.2;
}

:deep(.katex-display) {
  margin: 1em 0;
  overflow-x: auto;
  overflow-y: hidden;
}

:deep(.katex-display > .katex) {
  display: inline-block;
  white-space: nowrap;
}

:deep(.katex .boldsymbol) {
  font-weight: bold;
}

:deep(.katex .amsrm) {
  font-family: KaTeX_AMS;
}

:deep(.katex .mathscr) {
  font-family: KaTeX_Script;
}

:deep(.katex .mathfrak) {
  font-family: KaTeX_Fraktur;
}

:deep(.katex .mathbb) {
  font-family: KaTeX_AMS;
}

:deep(.katex .mathcal) {
  font-family: KaTeX_Caligraphic;
}

:deep(.katex .mathdefault) {
  font-family: KaTeX_Math;
}

/* 确保希腊字母等数学符号使用正确的字体 */
:deep(.katex .mathnormal) {
  font-family: KaTeX_Math;
  font-style: italic;
}

:deep(.katex .mathrm) {
  font-family: KaTeX_Main;
  font-style: normal;
}

:deep(.katex .mathit) {
  font-family: KaTeX_Main;
  font-style: italic;
}

:deep(.katex .mathbf) {
  font-family: KaTeX_Main;
  font-weight: bold;
}

:deep(.katex .mathsf) {
  font-family: KaTeX_SansSerif;
}

:deep(.katex .mathtt) {
  font-family: KaTeX_Typewriter;
}

/* 行内数学公式的间距调整 */
:deep(.katex-inline) {
  margin: 0 0.1em;
}

/* 错误提示样式 */
:deep(.katex-error) {
  color: #cc0000;
  background-color: #ffeeee;
  padding: 2px 4px;
  border-radius: 3px;
  border: 1px solid #ffcccc;
}

/* 确保大纲组件不产生额外滚动条 */
.sidebar-content :deep(.outline-container) {
  overflow: visible !important;
  max-height: none !important;
  height: auto !important;
}

.sidebar-content :deep(.el-scrollbar) {
  height: auto !important;
}

.sidebar-content :deep(.el-scrollbar__wrap) {
  overflow: visible !important;
  max-height: none !important;
}

.sidebar-content :deep(.el-scrollbar__view) {
  overflow: visible !important;
}

/* 重新启用内部滚动条，但只对 sidebar-content 生效 */
.sidebar-content {
  overflow-y: auto !important;
  overflow-x: hidden !important;
  scrollbar-width: thin;
}

.sidebar-content::-webkit-scrollbar {
  width: 6px !important;
  display: block !important;
}

.sidebar-content::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar-content::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}

.sidebar-content::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.3);
}

/* 禁用子元素的滚动条，但保留 sidebar-content 的滚动 */
.sidebar-content > * {
  overflow: visible !important;
  max-height: none !important;
}

.sidebar-content :deep(div:not(.sidebar-content)) {
  scrollbar-width: none !important;
}

.sidebar-content :deep(div:not(.sidebar-content)::-webkit-scrollbar) {
  display: none !important;
}

/* 响应式布局 */
@media (max-width: 1024px) {
  .content-layout {
    flex-direction: column;
  }
  
  .sidebar,
  .sidebar.collapsed {
    width: 100%;
  }
  
  .sidebar-content {
    position: static;
    max-height: none;
  }
  
  .expand-btn {
    position: relative;
    top: auto;
    transform: none;
    margin: 12px auto;
  }
}

@media (max-width: 768px) {
  .page-container {
    margin: 90px auto 20px;
    padding: 15px;
  }
  
  .markdown-body {
    padding: 1.5em;
  }
}

@media (max-width: 480px) {
  .page-container {
    margin: 80px auto 15px;
    padding: 10px;
  }
  
  .markdown-body {
    padding: 1em;
  }
  
  :deep(h1) {
    font-size: 1.8em;
  }
  
  :deep(h2) {
    font-size: 1.5em;
  }
  
  :deep(h3) {
    font-size: 1.2em;
  }
}

/* 展开按钮样式 */
.expand-btn {
  position: fixed;
  top: 50vh;
  transform: translateY(-50%);
  z-index: 100;
  width: 36px;
  height: 36px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.15);
  background-color: var(--el-color-primary);
  color: white;
  border: none;
}

.expand-btn:hover {
  background-color: var(--el-color-primary-dark-2);
}

.expand-btn-left {
  left: 20px;
}

.expand-btn-right {
  right: 20px;
}

@media (max-width: 1400px) {
  .sidebar {
    height: auto; /* 响应式时重置高度 */
  }
  
  .sidebar-content {
    position: sticky;
    top: 100px;
    bottom: auto;
    left: auto !important;
    right: auto !important;
    width: auto !important;
    height: auto; /* 响应式时重置高度 */
    max-height: calc(100vh - 120px);
    overflow-y: auto;
    overflow-x: hidden;
    z-index: auto;
  }
}
</style>
