<template>
  <div class="knowledge-container">
    <div class="header">
      <h1>知识文章</h1>
      <p>探索、学习、分享。这里是我关于技术、科学和思考的笔记。</p>
    </div>
    <div class="main-content">
      <aside class="timeline-sidebar">
        <ArticleTimeline :articles="filteredArticles" @scroll-to-article="handleScrollToArticle" />
      </aside>
      <main class="articles-main">
        <TagFilter :tags="allTags" @tag-selected="handleTagSelected" />
        <div class="articles-grid">
          <ArticleCard
            v-for="article in displayedArticles"
            :id="article.slug"
            :key="article.slug"
            :article="article"
          />
        </div>
        <div v-if="hasMoreArticles" class="load-more-container">
          <el-button type="primary" plain @click="loadMore">查看更多</el-button>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import articleData from '@/data/articles.json'
import ArticleCard from '@/components/ArticleCard.vue'
import ArticleTimeline from '@/components/ArticleTimeline.vue'
import TagFilter from '@/components/TagFilter.vue'

// 所有文章，按日期降序排序
const sortedArticles = computed(() => {
  return [...articleData].sort((a, b) => new Date(b.date) - new Date(a.date))
})

// 所有唯一的标签
const allTags = computed(() => {
  const tags = new Set()
  articleData.forEach(article => {
    article.tags.forEach(tag => tags.add(tag))
  })
  return Array.from(tags)
})

// 当前选择的标签
const selectedTag = ref(null)

// 根据标签筛选后的文章
const filteredArticles = computed(() => {
  if (!selectedTag.value) {
    return sortedArticles.value
  }
  return sortedArticles.value.filter(article => article.tags.includes(selectedTag.value))
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

// 处理标签选择事件
const handleTagSelected = (tag) => {
  selectedTag.value = tag
  displayCount.value = 5 // 重置显示数量
}

const handleScrollToArticle = (slug) => {
  const element = document.getElementById(slug)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }else {
    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
  }
}
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
</style>
