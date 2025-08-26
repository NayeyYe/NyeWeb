<template>
  <el-card class="timeline-card" shadow="never">
    <template #header>
      <div class="card-header">
        <span>文章归档</span>
        <el-icon class="collapse-icon" @click="isCollapsed = !isCollapsed" :title="isCollapsed ? '展开' : '收起'">
          <arrow-up-bold v-if="!isCollapsed" />
          <arrow-down-bold v-else />
        </el-icon>
      </div>
    </template>
    <el-collapse-transition>
      <el-timeline v-show="!isCollapsed">
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
    </el-collapse-transition>
  </el-card>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ArrowUpBold, ArrowDownBold } from '@element-plus/icons-vue'

const props = defineProps({
  articles: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['scrollToArticle'])

const isCollapsed = ref(false)

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

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
}

.collapse-icon {
  cursor: pointer;
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
