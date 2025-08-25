<template>
  <el-card class="timeline-card" shadow="never">
    <template #header>
      <div class="card-header">
        <span>文章归档</span>
      </div>
    </template>
    <el-timeline>
      <el-timeline-item
        v-for="article in sortedArticles"
        :key="article.slug"
        :timestamp="article.date"
        placement="top"
      >
        <a class="timeline-link" @click.prevent="onArticleClick(article.slug)">
          {{ article.title }}
        </a>
      </el-timeline-item>
    </el-timeline>
  </el-card>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  articles: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['scrollToArticle'])

const sortedArticles = computed(() => {
  return [...props.articles].sort((a, b) => new Date(b.date) - new Date(a.date))
})

const onArticleClick = (slug) => {
  emit('scrollToArticle', slug)
}
</script>

<style scoped>
.timeline-card {
  border-radius: 15px;
  position: sticky;
  top: 100px; /* Adjust based on your header height */
}

.card-header span {
  font-weight: bold;
}

.timeline-link {
  cursor: pointer;
  color: #606266;
  transition: color 0.3s;
}

.timeline-link:hover {
  color: #409eff;
}
</style>

