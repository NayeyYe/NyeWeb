import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Knowledge from '../views/Knowledge.vue'
import Article from '../views/Article.vue' // 导入文章页面
import Projects from '../views/Projects.vue'
import Project from '../views/Project.vue'
import Tools from '../views/Tools.vue'
import Resources from '../views/Resources.vue'
import AboutMe from '../views/AboutMe.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'AboutMe',
    component: AboutMe
  },
  {
    path: '/knowledge',
    name: 'Knowledge',
    component: Knowledge
  },
  {
    path: '/article/:category+/:slug',
    name: 'ArticleWithCategory',
    component: () => import('@/views/Article.vue'),
    meta: { title: '文章详情' }
  },
  {
    path: '/article/:slug',
    name: 'Article',
    component: () => import('@/views/Article.vue'),
    meta: { title: '文章详情' }
  },
  {
    path: '/projects',
    name: 'Projects',
    component: Projects
  },
  {
    path: '/projects/:slug',
    name: 'Project',
    component: Project
  },
  {
    path: '/tools',
    name: 'Tools',
    component: Tools
  },
  {
    path: '/resources',
    name: 'Resources',
    component: Resources
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
