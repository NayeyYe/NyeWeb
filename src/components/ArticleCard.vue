<template>
  <router-link :to="`/knowledge/${article.slug}`" class="card-link">
    <el-card class="article-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span>{{ article.title }}</span>
        </div>
      </template>
      <div class="card-summary">
        <p>{{ article.summary }}</p>
      </div>
      <div class="card-footer">
        <div class="article-tags">
          <el-tag
            v-for="tag in article.tags"
            :key="tag"
            type="info"
            size="small"
            effect="plain"
            round
          >
            {{ tag }}
          </el-tag>
        </div>
        <div class="article-date">{{ article.date }}</div>
      </div>
    </el-card>
  </router-link>
</template>

<script setup>
defineProps({
  article: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>
.article-card {
  height: 100%;
  display: flex;
  flex-direction: column;
  border-radius: 15px;
}

.card-link {
  text-decoration: none;
}

.card-header span {
  font-weight: bold;
  font-size: 1.1em;
  color: #303133;
}

.card-summary {
  flex-grow: 1;
  color: #606266;
  font-size: 0.9em;
  line-height: 1.5;
  /* Multi-line ellipsis */
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
  overflow: hidden;
  text-overflow: ellipsis;
  min-height: 63px; /* 0.9em * 1.5 * 3 lines */
}

.card-footer {
  margin-top: 15px;
  padding-top: 10px;
  border-top: 1px solid #ebeef5;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.article-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.article-date {
  color: #909399;
  font-size: 14px;
  white-space: nowrap;
}
</style>

