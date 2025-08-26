<template>
  <router-link :to="projectLink" class="card-link">
    <el-card class="project-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span>{{ project.title }}</span>
        </div>
      </template>
      <div class="card-summary">
        <p>{{ project.summary }}</p>
      </div>
      <div class="card-footer">
        <div class="project-tags">
          <el-tag
            v-for="tag in project.tags"
            :key="tag"
            type="info"
            size="small"
            effect="plain"
            round
          >
            {{ tag }}
          </el-tag>
        </div>
        <div class="project-date">{{ project.date }}</div>
      </div>
    </el-card>
  </router-link>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  project: {
    type: Object,
    required: true
  }
})

const projectLink = computed(() => {
  return `/projects/${props.project.slug}`
})
</script>

<style scoped>
.project-card {
  height: 100%;
  display: flex;
  flex-direction: column;
  border-radius: 15px;
  border: 1px solid var(--el-border-color-lighter);
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
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
  overflow: hidden;
  text-overflow: ellipsis;
  min-height: 63px; /* 3 lines * 1.5 line-height * 14px font-size */
}

.card-footer {
  margin-top: 15px;
  padding-top: 10px;
  border-top: 1px solid #ebeef5;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.project-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.project-date {
  color: #909399;
  font-size: 14px;
  white-space: nowrap;
}
</style>
