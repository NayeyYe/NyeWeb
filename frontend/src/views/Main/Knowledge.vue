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
        <div v-if="hasMoreArticles" class="load-more-container">
          <el-button plain type="primary" @click="loadMore">查看更多</el-button>
        </div>
      </main>
      <aside class="tags-sidebar">
        <ArticleCategoryTree :articles="sortedArticles" @category-selected="handleCategorySelected"/>
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

// 获取文章数据
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

// 要显示的文章数量
const displayCount = ref(5)

// 实际显示在页面上的文章
const displayedArticles = computed(() => {
  return filteredArticles.value.slice(0, displayCount.value)
})

// 检查是否还有更多文章可以加载
const hasMoreArticles = computed(() => {
  return displayCount.value < filteredArticles.value.length
})

// 加载更多文章
const loadMore = () => {
  displayCount.value += 5
}

// 处理分类选择事件
const handleCategorySelected = (category) => {
  selectedCategory.value = category
  selectedTag.value = null // 重置标签筛选
  displayCount.value = 5 // 重置显示数量
}

// 处理标签选择事件
const handleTagSelected = (tag) => {
  selectedTag.value = tag
  displayCount.value = 5 // 重置显示数量
}

// 清空筛选条件
const clearFilters = () => {
  selectedCategory.value = null
  selectedTag.value = null
  displayCount.value = 5
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
  padding: 100px 20px 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  text-align: center;
  margin-bottom: 40px;
}

.header h1 {
  font-size: 2.5em;
  margin-bottom: 10px;
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

.load-more-container {
  margin-top: 20px;
  text-align: center;
}

.tags-sidebar {
  width: 300px;
  flex-shrink: 0;
  position: sticky;
  top: 100px;
}

/* 响应式布局 */
@media (max-width: 1024px) {
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
}

@media (max-width: 768px) {
  .knowledge-container {
    padding: 100px 10px 10px;
  }

  .header h1 {
    font-size: 2em;
  }

  .header p {
    font-size: 1em;
  }
}
</style>
