<template>
  <div class="knowledge-container">
    <div class="header">
      <h1>知识文章</h1>
      <p>探索、学习、分享。这里是我关于技术、科学和思考的笔记。</p>
    </div>
    <div class="articles-grid">
      <ArticleCard v-for="article in articles" :key="article.slug" :article="article" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import articleData from '@/data/articles.json'
import ArticleCard from '@/components/ArticleCard.vue'

// todo: 这里应该加入数据库内容
const articles = ref(articleData)
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

.articles-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
</style>
