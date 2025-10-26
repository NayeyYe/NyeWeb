<template>
  <div class="knowledge-container">
    <div class="header">
      <h1>知识文章</h1>
      <p>探索、学习、分享。这里是我关于技术、科学和思考的笔记。</p>
    </div>
    <div v-loading="loading" class="main-content">
      <aside class="timeline-sidebar">
        <!-- 传递筛选后的文章给时间线组件 -->
        <ArticleTimeline :articles="filteredArticles" @scroll-to-article="handleScrollToArticle"/>
      </aside>
      <main class="articles-main">
        <div v-if="!loading && filteredArticles.length === 0" class="no-articles">
          <el-empty description="暂无文章数据">
            <el-button type="primary" @click="clearFilters">清空筛选条件</el-button>
          </el-empty>
        </div>
        <div v-else class="articles-grid">
          <ArticleCard
              v-for="article in displayedArticles"
              :id="article.slug"
              :key="article.slug"
              :article="article"
          />
        </div>
        <div v-if="filteredArticles.length > pageSize" class="pagination-container">
          <el-pagination
            v-model:current-page="currentPage"
            :page-size="pageSize"
            :total="filteredArticles.length"
            layout="prev, pager, next"
            @current-change="handlePageChange"
          />
        </div>
      </main>
      <aside class="tags-sidebar">
        <ArticleCategoryTree :articles="sortedArticles" :show-articles="false" @category-selected="handleCategorySelected"/>
        <ArticleTagFilter :counts="availableTagCounts" :tags="availableTags" @tag-selected="handleTagSelected"/>
      </aside>
    </div>
  </div>
</template>

<script setup>
import {computed, onMounted, ref} from 'vue'
import axios from 'axios'
import ArticleCard from '@/components/Main/Article/ArticleCard.vue'
import ArticleTimeline from '@/components/Main/Article/ArticleTimeline.vue'
import ArticleTagFilter from '@/components/Main/Article/ArticleTagFilter.vue'
import ArticleCategoryTree from '@/components/Main/Article/ArticleCategoryTree.vue'

const loading = ref(false)
const articles = ref([])
const tags = ref([])
const tagCounts = ref({})

const API_BASE_URL = '/api'

// 取文章数据
const fetchArticles = async () => {
  loading.value = true
  try {
    const response = await axios.get(`${API_BASE_URL}/articles`, {
      timeout: 10000,
      headers: {
        'Accept': 'application/json'
      }
    })

    if (response.data && Array.isArray(response.data)) {
      articles.value = response.data
      console.log(`Knowledge: 成功获取 ${articles.value.length} 篇文章`)
    }
  } catch (error) {
    console.error('Knowledge: 获取文章数据失败:', error)
    articles.value = []
  } finally {
    loading.value = false
  }
}

// 获取标签数据
const fetchTags = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/tags`, {
      timeout: 10000,
      headers: {
        'Accept': 'application/json'
      }
    })

    if (response.data) {
      tags.value = response.data.tags || []
      tagCounts.value = response.data.counts || {}
      console.log(`Knowledge: 成功获取 ${tags.value.length} 个标签`)
    }
  } catch (error) {
    console.error('Knowledge: 获取标签数据失败:', error)
    tags.value = []
    tagCounts.value = {}
  }
}

// 所有文章，按日期降序排序
const sortedArticles = computed(() => {
  return [...articles.value].sort((a, b) => new Date(b.date) - new Date(a.date))
})

// 当前选择的分类和标签
const selectedCategory = ref(null)
const selectedTag = ref(null)

// 1. 根据分类筛选
const articlesByCategory = computed(() => {
  if (!selectedCategory.value) {
    return sortedArticles.value
  }
  return sortedArticles.value.filter(article =>
      article.category && article.category.startsWith(selectedCategory.value)
  )
})

// 2. 根据当前筛选后的文章计算可用标签
const availableTags = computed(() => {
  const tagSet = new Set()
  const articlesToCheck = selectedCategory.value ? articlesByCategory.value : sortedArticles.value
  articlesToCheck.forEach(article => {
    if (article.tags) {
      article.tags.forEach(tag => tagSet.add(tag))
    }
  })
  return Array.from(tagSet)
})

// 计算可用标签的计数
const availableTagCounts = computed(() => {
  const counts = {}
  const articlesToCheck = selectedCategory.value ? articlesByCategory.value : sortedArticles.value
  articlesToCheck.forEach(article => {
    if (article.tags) {
      article.tags.forEach(tag => {
        counts[tag] = (counts[tag] || 0) + 1
      })
    }
  })
  return counts
})

// 3. 最终筛选结果(分类+标签)
const filteredArticles = computed(() => {
  if (!selectedTag.value) {
    return articlesByCategory.value
  }
  return articlesByCategory.value.filter(article =>
      article.tags && article.tags.includes(selectedTag.value)
  )
})

// 分页相关
const currentPage = ref(1)
const pageSize = ref(5)

// 实际显示在页面上的文章
const displayedArticles = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredArticles.value.slice(start, end)
})

// 处理页码变化
const handlePageChange = (page) => {
  currentPage.value = page
  // 滚动到顶部
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// 处理分类选择事件
const handleCategorySelected = (category) => {
  selectedCategory.value = category
  selectedTag.value = null // 重置标签筛选
  currentPage.value = 1 // 重置到第一页
}

// 处理标签选择事件
const handleTagSelected = (tag) => {
  selectedTag.value = tag
  currentPage.value = 1 // 重置到第一页
}

// 清空筛选条件
const clearFilters = () => {
  selectedCategory.value = null
  selectedTag.value = null
  currentPage.value = 1
}

const handleScrollToArticle = (slug) => {
  const element = document.getElementById(slug)
  if (element) {
    element.scrollIntoView({behavior: 'smooth', block: 'start'})
  } else {
    window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});
  }
}

onMounted(async () => {
  await Promise.all([fetchArticles(), fetchTags()])
})
</script>

<style scoped>
.knowledge-container {
  max-width: 1200px;
  margin: 100px auto 40px; /* 从 padding 改为 margin,与 Resources/Tools 一致 */
  padding: 0 20px; /* 只保留左右 padding */
}

.header {
  text-align: center;
  margin-bottom: 40px;
}

.header h1 {
  font-size: 2.5em;
  margin-bottom: 10px;
  color: inherit; /* 移除颜色设置,使用默认 */
}

.header p {
  font-size: 1.1em;
  color: #606266;
}

.main-content {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

.timeline-sidebar {
  width: 280px;
  flex-shrink: 0;
  position: sticky;
  top: 100px;
}

.articles-main {
  flex-grow: 1;
}

.articles-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.pagination-container {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}

.tags-sidebar {
  width: 300px;
  flex-shrink: 0;
  position: sticky;
  top: 100px;
}

/* 响应式布局 */
@media (max-width: 1024px) {
  .knowledge-container {
    margin: 90px auto 30px; /* 与 Resources/Tools 一致 */
    padding: 0 15px;
  }
  
  .main-content {
    flex-direction: column;
  }

  .timeline-sidebar,
  .tags-sidebar {
    width: 100%;
    position: static;
  }

  /* 调整响应式布局时的组件顺序 */
  .timeline-sidebar {
    order: 1; /* 归档 */
  }

  .tags-sidebar {
    order: 2; /* 文件夹分类和tag分类 */
  }

  .articles-main {
    order: 3; /* 文章列表 */
  }
  
  .articles-grid {
    gap: 15px;
  }
  
  .pagination-container {
    margin-top: 20px;
  }
}

@media (max-width: 768px) {
  .knowledge-container {
    margin: 80px auto 20px; /* 与 Resources/Tools 一致 */
    padding: 0 10px;
  }

  .header {
    margin-bottom: 25px; /* 从 30px 改为 25px */
  }
  
  .header h1 {
    font-size: 2em;
  }

  .header p {
    font-size: 1em;
  }
  
  .articles-grid {
    gap: 12px;
  }
  
  .pagination-container {
    margin-top: 15px;
  }
}

@media (max-width: 480px) {
  .knowledge-container {
    margin: 70px auto 15px; /* 与 Resources/Tools 一致 */
    padding: 0 5px;
  }
  
  .header {
    margin-bottom: 20px;
  }
  
  .header h1 {
    font-size: 1.8em;
  }
  
  .header p {
    font-size: 0.9em;
  }
  
  .articles-grid {
    gap: 10px;
  }
  
  .pagination-container {
    margin-top: 10px;
  }
  
  :deep(.el-pagination) {
    --el-pagination-font-size: 12px;
  }
}
</style>
