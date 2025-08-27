<template>
  <el-card class="timeline-card" shadow="never">
    <template #header>
      <div class="card-header">
        <span>项目归档</span>
        <el-icon class="collapse-icon" @click="isCollapsed = !isCollapsed" :title="isCollapsed ? '展开' : '收起'">
          <arrow-up-bold v-if="!isCollapsed" />
          <arrow-down-bold v-else />
        </el-icon>
      </div>
    </template>
    <el-collapse-transition>
      <el-timeline v-show="!isCollapsed">
        <el-timeline-item
          v-for="project in sortedProjects"
          :key="project.slug"
          :timestamp="project.date"
          placement="top"
        >
          <a class="timeline-link" @click.prevent="onProjectClick(project.slug)">
            {{ project.title }}
          </a>
        </el-timeline-item>
      </el-timeline>
    </el-collapse-transition>
  </el-card>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ArrowUpBold, ArrowDownBold } from '@element-plus/icons-vue'

interface Project {
  slug: string;
  date: string;
  title: string;
}

interface Props {
  projects: Project[];
}

const props = defineProps<Props>()

const emit = defineEmits(['scrollToProject'])

const isCollapsed = ref(false)

const sortedProjects = computed(() => {
  return [...props.projects].sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
})

const onProjectClick = (slug: string) => {
  emit('scrollToProject', slug)
}
</script>

<style scoped>
.timeline-card {
  border-radius: 15px;
  border: 1px solid var(--el-border-color-lighter);
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
  color: var(--el-text-color-primary);
  text-decoration: none;
}

.timeline-link:hover {
  color: var(--el-color-primary);
}
</style>