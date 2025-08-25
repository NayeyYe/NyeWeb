<template>
  <el-card class="article-card" :id="id">
    <h2 class="article-title">{{ article.title }}</h2>
    <p class="article-summary">{{ article.summary }}</p>
    <div class="article-tags">
      <el-tag v-for="tag in article.tags" :key="tag" class="article-tag">{{ tag }}</el-tag>
    </div>
  </el-card>
</template>

<script setup>
defineProps({
  article: {
    type: Object,
    required: true
  },
  id: {
    type: String,
    required: true
  }
})
</script>

<style scoped>
.article-card {
  margin-bottom: 20px;
}

.article-title {
  font-size: 1.5em;
  margin-bottom: 10px;
}

.article-summary {
  color: #666;
}

.article-tags {
  margin-top: 10px;
}

.article-tag {
  margin-right: 5px;
}
</style>
