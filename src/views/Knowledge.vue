<template>
  <div class="knowledge-container">
    <el-card class="list-card">
      <template #header>
        <div class="card-header">
          <span>知识文章</span>
        </div>
      </template>
      <div v-for="article in articles" :key="article.slug" class="article-item">
        <router-link :to="`/knowledge/${article.slug}`" class="article-link">
          {{ article.title }}
        </router-link>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// 请将这里的 title 和 slug 替换为您 public/articles/knowledge 文件夹中实际的文件名。
// slug 的值必须是您的文件名（不包含 .md 后缀）。
const articles = ref([
  { title: 'Logistic Regression 笔记', slug: 'Logistic' }, // 对应 public/articles/knowledge/Logistic.md
  { title: 'SVM 学习笔记', slug: 'SVM' }  // 对应 public/articles/knowledge/SVM.md
])
</script>

<style scoped>
.knowledge-container {
  padding: 100px 20px 20px;
  max-width: 900px;
  margin: 0 auto;
}

.list-card {
  border-radius: 15px;
}

.card-header {
  font-size: 18px;
  font-weight: bold;
}

.article-item {
  padding: 15px 0;
  border-bottom: 1px solid #ebeef5;
}

.article-item:last-child {
  border-bottom: none;
}

.article-link {
  text-decoration: none;
  color: #303133;
  font-size: 16px;
  transition: color 0.3s;
}

.article-link:hover {
  color: #409eff;
}
</style>
