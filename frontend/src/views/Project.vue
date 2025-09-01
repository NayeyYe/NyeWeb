<template>
  <div class="page-container">
    <div v-if="projectNotFound" class="not-found">
      <h1>404 - 项目未找到</h1>
      <p>抱歉，您要查找的项目不存在或链接已更改。</p>
      <router-link to="/projects">返回项目列表</router-link>
    </div>
    <div v-else class="content-wrapper">
      <aside class="outline-sidebar">
        <div class="outline-fixed-container">
          <Outline v-if="headings.length" :outline="headings" :active-id="activeHeadingId" />
        </div>
      </aside>
      <main class="main-content">
        <article class="markdown-body">
          <h1>{{ projectTitle }}</h1>
          <div v-html="projectContent"></div>
        </article>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import Outline from '@/components/Outline.vue'
import mermaid from 'mermaid'

// Markdown-it and plugins
import markdownit from 'markdown-it'
import mdAnchor from 'markdown-it-anchor'
import slugify from 'slugify'
import mdKatex from '@iktakahiro/markdown-it-katex'
import hljs from 'highlight.js'

// CSS imports
import 'highlight.js/styles/github.css'
import 'github-markdown-css/github-markdown.css'
import 'katex/dist/katex.min.css'

// 初始化 Mermaid
mermaid.initialize({ startOnLoad: false, theme: 'default' })

const route = useRoute()
const projectContent = ref('')
const projectTitle = ref('')
const projectNotFound = ref(false)
const headings = ref([])
const activeHeadingId = ref('')
let observer = null

const API_BASE_URL = 'http://localhost:8080/api'

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
    permalink: true, // 强制为所有层级应用permalink，从而确保生成ID
    level: [1, 2, 3, 4, 5, 6],
    slugify: s => slugify(s, { lower: true, strict: true }),
    permalinkSymbol: '¶', // 你可以自定义这个符号，或者设为空字符串''来隐藏它
    permalinkBefore: true,
    permalinkClass: 'header-anchor'
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
    // 项目文件中的图片相对于 /articles/projects/ 目录
    token.attrSet('src', `/articles/projects/${src.substring(2)}`)
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
          button.textContent = '已复制!';
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
    rootMargin: '0px 0px -80% 0px',
    threshold: 0
  });

  headingElements.forEach(el => observer.observe(el));
};

const fetchProject = async () => {
  projectNotFound.value = false
  projectContent.value = ''
  projectTitle.value = ''
  headings.value = []

  const slug = route.params.slug
  if (!slug) {
    projectNotFound.value = true
    return
  }

  try {
    // 1. 从数据库API获取项目信息
    const response = await axios.get(`${API_BASE_URL}/projects/${slug}`, {
      timeout: 10000,
      headers: {
        'Accept': 'application/json'
      }
    })

    if (response.data) {
      const projectData = response.data
      projectTitle.value = projectData.title

      try {
        // 2. 根据slug从dist目录获取项目内容
        const markdownResponse = await fetch(`/articles/projects/${projectData.slug}.md`)
        if (!markdownResponse.ok) {
          throw new Error(`HTTP error! status: ${markdownResponse.status}`)
        }
        const markdownText = await markdownResponse.text()

        // 提取标题
        const tokens = md.parse(markdownText, {})
        const extractedHeadings = []
        tokens.forEach((token, i) => {
          if (token.type === 'heading_open') {
            const textToken = tokens[i + 1]
            const id = token.attrGet('id')
            if (textToken && textToken.type === 'inline' && id) {
              extractedHeadings.push({
                level: parseInt(token.tag.substring(1), 10),
                text: textToken.content,
                id: id
              })
            }
          }
        })
        headings.value = extractedHeadings

        // 3. 渲染Markdown
        projectContent.value = md.render(markdownText)

        // DOM更新后设置复制按钮和滚动监听
        await nextTick()
        setupCopyButtons()
        setupIntersectionObserver()
        // 渲染 Mermaid 图表
        mermaid.init(undefined, document.querySelectorAll('.mermaid'))

        console.log(`成功加载项目: ${projectData.title}`)
      } catch (e) {
        console.error(`加载项目内容失败: ${projectData.slug}.md`, e)
        projectNotFound.value = true
      }
    } else {
      projectNotFound.value = true
    }
  } catch (error) {
    console.error('获取项目信息失败:', error)
    projectNotFound.value = true
  }
}

onMounted(fetchProject)
watch(() => route.params.slug, fetchProject)

onUnmounted(() => {
  if (observer) {
    observer.disconnect();
  }
});
</script>

<style scoped>

.page-container {
  max-width: 1200px;
  margin: 100px auto 40px;
  padding: 20px;
}

.content-wrapper {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

.outline-sidebar {
  flex: 0 0 250px;
  width: 250px;
}

.outline-fixed-container {
  position: fixed;
  top: 100px;
  width: 250px;
  height: calc(100vh - 120px); /* 确保容器有明确的高度 */
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
  position: relative; /* 为锚点定位提供上下文 */
  line-height: 1.8;
  color: #333;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
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

.not-found {
  text-align: center;
  padding: 40px;
  color: #606266;
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
:deep(h1) { font-size: 2em; }
:deep(h2) { font-size: 1.6em; }
:deep(h3) { font-size: 1.3em; }

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

:deep(.dot.red) { background-color: #ff5f56; }
:deep(.dot.yellow) { background-color: #ffbd2e; }
:deep(.dot.green) { background-color: #27c93f; }

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
</style>