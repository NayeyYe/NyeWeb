import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Main/Home.vue'
import Knowledge from '../views/Main/Knowledge.vue'
import Article from '../views/Main/Article.vue' // 导入文章页面
import Projects from '../views/Main/Projects.vue'
import Project from '../views/Main/Project.vue'
import Tools from '../views/Main/Tools.vue'
import Resources from '../views/Main/Resources.vue'
import AboutMe from '../views/Main/AboutMe.vue'
import AdminLogin from '../views/Dashboard/AdminLogin.vue'
import HelloWorld from '../views/Dashboard/HelloWorld.vue'

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
    component: () => import('@/views/Main/Article.vue'),
    meta: { title: '文章详情' }
  },
  {
    path: '/article/:slug',
    name: 'Article',
    component: () => import('@/views/Main/Article.vue'),
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
  },
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: AdminLogin,
    meta: { title: '管理员登录' }
  },
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: HelloWorld,
    meta: { title: '管理后台' }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
