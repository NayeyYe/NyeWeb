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
        <div class="card-list">
          <ArticleCard
            v-for="article in recentArticles"
            :key="article.slug"
            :article="article"
            class="list-item-card"
          />
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
import { computed } from 'vue'
import ProfileCard from '@/components/ProfileCard.vue'
import TimelineEditor from '@/components/TimelineEditor.vue'
import ArticleCard from '@/components/ArticleCard.vue'
import ProjectCard from '@/components/ProjectCard.vue'
import articlesData from '@/data/articles.json'
import projectsData from '@/data/projects.json'

const recentArticles = computed(() => {
  return [...articlesData]
    .sort((a, b) => new Date(b.date) - new Date(a.date))
    .slice(0, 3)
})

const recentProjects = computed(() => {
  return [...projectsData]
    .sort((a, b) => new Date(b.date) - new Date(a.date))
    .slice(0, 3)
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
