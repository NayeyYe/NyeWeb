<script setup lang="ts">
import { ref, computed } from 'vue'
import projectData from '@/data/projects.json'
import ProjectCard from '@/components/ProjectCard.vue'
import ProjectTimeline from '@/components/ProjectTimeline.vue'
import ProjectTagFilter from '@/components/ProjectTagFilter.vue'

const sortedProjects = computed(() => {
  return [...projectData].sort((a, b) => new Date(b.date) - new Date(a.date))
})

const selectedTag = ref(null)

const allTags = computed(() => {
  const tags = new Set()
  sortedProjects.value.forEach(project => {
    project.tags.forEach(tag => tags.add(tag))
  })
  return Array.from(tags)
})

const tagCounts = computed(() => {
  const counts = {}
  sortedProjects.value.forEach(project => {
    project.tags.forEach(tag => {
      counts[tag] = (counts[tag] || 0) + 1
    })
  })
  return counts
})

const filteredProjects = computed(() => {
  if (!selectedTag.value) {
    return sortedProjects.value
  }
  return sortedProjects.value.filter(project => project.tags.includes(selectedTag.value))
})

const displayCount = ref(5)

const displayedProjects = computed(() => {
  return filteredProjects.value.slice(0, displayCount.value)
})

const hasMoreProjects = computed(() => {
  return displayCount.value < filteredProjects.value.length
})

const loadMore = () => {
  displayCount.value += 5
}

const handleTagSelected = (tag) => {
  selectedTag.value = tag
  displayCount.value = 5
}

const handleScrollToProject = (slug) => {
  const projectElement = document.getElementById(`project-${slug}`)
  if (projectElement) {
    projectElement.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}
</script>

<template>
  <div class="page-container">
    <div class="header">
      <h1>我的项目</h1>
      <p>从代码到现实，这里是我实践和创造的结晶。</p>
    </div>
    <div class="main-content">
      <aside class="left-sidebar">
        <ProjectTimeline :projects="filteredProjects" @scroll-to-project="handleScrollToProject" />
      </aside>
      <main class="projects-main">
        <div class="projects-grid">
          <ProjectCard
            v-for="project in displayedProjects"
            :key="project.slug"
            :project="project"
            :id="`project-${project.slug}`"
          />
        </div>
        <div v-if="hasMoreProjects" class="load-more-container">
          <el-button type="primary" plain @click="loadMore">查看更多</el-button>
        </div>
      </main>
      <aside class="right-sidebar">
        <ProjectTagFilter :tags="allTags" :counts="tagCounts" @tag-selected="handleTagSelected" />
      </aside>
    </div>
  </div>
</template>

<style scoped>
.page-container {
  max-width: 1400px;
  margin: 100px auto 40px;
  padding: 0 20px;
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

.left-sidebar {
  width: 280px;
  flex-shrink: 0;
  position: sticky;
  top: 100px;
}

.projects-main {
  flex: 1;
  min-width: 0;
}

.projects-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.load-more-container {
  margin-top: 20px;
  text-align: center;
}

.right-sidebar {
  width: 300px;
  flex-shrink: 0;
  position: sticky;
  top: 100px;
}
</style>