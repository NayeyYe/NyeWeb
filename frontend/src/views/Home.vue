<template>
  <div class="home-container">
    <div class="left-column">
      <ProfileCard class="profile-card-container" />
      <TimelineEditor class="timeline-editor-container" />
    </div>
    <div class="right-column-content">
      <el-card class="content-card">
        <template #header>
          <div class="card-header">
            <span>最近文章</span>
            <router-link to="/knowledge" class="more-link">查看全部 &gt;</router-link>
          </div>
        </template>
        <div v-loading="articlesLoading" class="card-list">
          <ArticleCard
            v-for="article in recentArticles"
            :key="article.slug"
            :article="article"
            class="list-item-card"
          />
          <el-empty v-if="!articlesLoading && recentArticles.length === 0" description="暂无文章数据" :image-size="60">
          </el-empty>
        </div>
      </el-card>

      <el-card class="content-card">
        <template #header>
          <div class="card-header">
            <span>最近项目</span>
            <router-link to="/projects" class="more-link">查看全部 &gt;</router-link>
          </div>
        </template>
        <div class="card-list">
          <ProjectCard
            v-for="project in recentProjects"
            :key="project.slug"
            :project="project"
            class="list-item-card"
          />
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import ProfileCard from '@/components/ProfileCard.vue'
import TimelineEditor from '@/components/TimelineEditor.vue'
import ArticleCard from '@/components/ArticleCard.vue'
import ProjectCard from '@/components/ProjectCard.vue'
// 保留项目数据的JSON导入，因为只改文章部分
import projectsData from '@/data/projects.json'

const articlesLoading = ref(false)
const articlesFromDB = ref([])

const API_BASE_URL = 'http://localhost:8080/api'

// 获取文章数据
const fetchArticles = async () => {
  articlesLoading.value = true
  try {
    const response = await axios.get(`${API_BASE_URL}/articles`, {
      timeout: 10000,
      headers: {
        'Accept': 'application/json'
      }
    })

    if (response.data && Array.isArray(response.data)) {
      articlesFromDB.value = response.data
      console.log(`首页: 成功获取 ${articlesFromDB.value.length} 篇文章`)
    }
  } catch (error) {
    console.error('首页: 获取文章数据失败:', error)
    articlesFromDB.value = []
  } finally {
    articlesLoading.value = false
  }
}

// 最近文章（从数据库获取，取前3篇）
const recentArticles = computed(() => {
  return [...articlesFromDB.value]
    .sort((a, b) => new Date(b.date) - new Date(a.date))
    .slice(0, 3)
})

// 最近项目（暂时保持使用JSON数据）
const recentProjects = computed(() => {
  return [...projectsData]
    .sort((a, b) => new Date(b.date) - new Date(a.date))
    .slice(0, 3)
})

onMounted(() => {
  fetchArticles()
})
</script>

<style scoped>
.home-container {
  padding-top: 80px; /* 为固定的顶栏留出空间 */
  padding-bottom: 40px;
  max-width: 1280px;
  margin: 0 auto;
  display: flex;
  align-items: flex-start;
  gap: 20px;
  padding-left: 20px;
  padding-right: 20px;
}

.left-column {
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 350px; /* 您可以根据ProfileCard的宽度进行调整 */
  flex-shrink: 0;
}

.profile-card-container {
  position: sticky;
  top: 80px; /* 80px 是顶栏高度 */
  width: 100%;
}

.timeline-editor-container {
  width: 100%;
}

.right-column-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
  min-width: 0;
}

.content-card {
  width: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header span {
  font-size: 1.2em;
  font-weight: bold;
}

.more-link {
  text-decoration: none;
  color: #409eff;
  font-size: 14px;
}

.more-link:hover {
  text-decoration: underline;
}

.card-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.list-item-card {
  width: 100%;
}
</style>
