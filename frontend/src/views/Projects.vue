<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import ProjectCard from '@/components/ProjectCard.vue'
import ProjectTimeline from '@/components/ProjectTimeline.vue'
import ProjectTagFilter from '@/components/ProjectTagFilter.vue'

const loading = ref(false)
const projects = ref([])
const tags = ref([])
const tagCounts = ref({})

const API_BASE_URL = 'http://localhost:8080/api'

// 获取项目数据
const fetchProjects = async () => {
  loading.value = true
  try {
    const response = await axios.get(`${API_BASE_URL}/projects`, {
      timeout: 10000,
      headers: {
        'Accept': 'application/json'
      }
    })

    if (response.data && Array.isArray(response.data)) {
      projects.value = response.data
      console.log(`项目页面: 成功获取 ${projects.value.length} 个项目`)
    }
  } catch (error) {
    console.error('项目页面: 获取项目数据失败:', error)
    projects.value = []
  } finally {
    loading.value = false
  }
}

// 获取项目标签数据
const fetchProjectTags = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/project-tags`, {
      timeout: 10000,
      headers: {
        'Accept': 'application/json'
      }
    })

    if (response.data) {
      tags.value = response.data.tags || []
      tagCounts.value = response.data.counts || {}
      console.log(`项目页面: 成功获取 ${tags.value.length} 个项目标签`)
    }
  } catch (error) {
    console.error('项目页面: 获取项目标签数据失败:', error)
    tags.value = []
    tagCounts.value = {}
  }
}

// 所有项目，按日期降序排序
const sortedProjects = computed(() => {
  return [...projects.value].sort((a, b) => new Date(b.date) - new Date(a.date))
})

// 当前选择的标签
const selectedTag = ref(null)

// 根据标签筛选项目
const filteredProjects = computed(() => {
  if (!selectedTag.value) {
    return sortedProjects.value
  }
  return sortedProjects.value.filter(project =>
    project.tags && project.tags.includes(selectedTag.value)
  )
})

// 计算可用标签
const allTags = computed(() => {
  const tagSet = new Set()
  projects.value.forEach(project => {
    if (project.tags) {
      project.tags.forEach(tag => tagSet.add(tag))
    }
  })
  return Array.from(tagSet)
})

// 要显示的项目数量
const displayCount = ref(6)

// 实际显示在页面上的项目
const displayedProjects = computed(() => {
  return filteredProjects.value.slice(0, displayCount.value)
})

// 检查是否还有更多项目可以加载
const hasMoreProjects = computed(() => {
  return displayCount.value < filteredProjects.value.length
})

// 加载更多项目
const loadMore = () => {
  displayCount.value += 6
}

// 处理标签选择事件
const handleTagSelected = (tag) => {
  selectedTag.value = tag
  displayCount.value = 6 // 重置显示数量
}

// 清空筛选条件
const clearFilters = () => {
  selectedTag.value = null
  displayCount.value = 6
}

const handleScrollToProject = (slug) => {
  const element = document.getElementById(slug)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' })
  } else {
    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
  }
}

onMounted(async () => {
  await Promise.all([fetchProjects(), fetchProjectTags()])
})
</script>

<template>
  <div class="projects-container">
    <div class="header">
      <h1>项目展示</h1>
      <p>这里是我参与和完成的项目集合。</p>
    </div>
    <div v-loading="loading" class="main-content">
      <aside class="timeline-sidebar">
        <ProjectTimeline :projects="filteredProjects" @scroll-to-project="handleScrollToProject" />
      </aside>
      <main class="projects-main">
        <div v-if="!loading && filteredProjects.length === 0" class="no-projects">
          <el-empty description="暂无项目数据">
            <el-button type="primary" @click="clearFilters">清空筛选条件</el-button>
          </el-empty>
        </div>
        <div v-else class="projects-grid">
          <ProjectCard
            v-for="project in displayedProjects"
            :id="project.slug"
            :key="project.slug"
            :project="project"
          />
        </div>
        <div v-if="hasMoreProjects" class="load-more-container">
          <el-button type="primary" plain @click="loadMore">查看更多</el-button>
        </div>
      </main>
      <aside class="tags-sidebar">
        <ProjectTagFilter :tags="allTags" :counts="tagCounts" @tag-selected="handleTagSelected" />
      </aside>
    </div>
  </div>
</template>

<style scoped>
.projects-container {
  max-width: 1200px;
  margin: 80px auto 40px;
  padding: 20px;
}

.header {
  text-align: center;
  margin-bottom: 40px;
}

.header h1 {
  font-size: 2.5em;
  color: #2c3e50;
  margin-bottom: 10px;
}

.header p {
  font-size: 1.2em;
  color: #7f8c8d;
}

.main-content {
  display: flex;
  gap: 30px;
  align-items: flex-start;
}

.timeline-sidebar {
  flex: 0 0 280px;
}

.projects-main {
  flex: 1;
  min-width: 0;
}

.tags-sidebar {
  flex: 0 0 280px;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 25px;
}

.no-projects {
  text-align: center;
  padding: 60px 20px;
}

.load-more-container {
  text-align: center;
  margin-top: 30px;
}

@media (max-width: 768px) {
  .main-content {
    flex-direction: column;
  }

  .timeline-sidebar,
  .tags-sidebar {
    flex: none;
    width: 100%;
  }

  .projects-grid {
    grid-template-columns: 1fr;
  }
}
</style>