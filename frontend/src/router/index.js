import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Main/Home.vue'
import Knowledge from '../views/Main/Knowledge.vue'
import Article from '../views/Main/Article.vue' // 导入文章页面
import Projects from '../views/Main/Projects.vue'
import Project from '../views/Main/Project.vue'
import Tools from '../views/Main/Tools.vue'
import Resources from '../views/Main/Resources.vue'
import AboutMe from '../views/Main/AboutMe.vue'
import AdminLogin from '@/views/admin/AdminLogin.vue'
import DashBoard from '@/views/admin/DashBoard.vue'
import ProjectManagement from '@/views/admin/ProjectManagement.vue'
import ArticleManagement from '@/views/admin/ArticleManagement.vue'
import ToolManagement from '@/views/admin/ToolManagement.vue'
import ResourceManagement from '@/views/admin/ResourceManagement.vue'
import ProfileManagement from '@/views/admin/ProfileManagement.vue'

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
    path: '/admin',
    component: DashBoard,
    meta: { title: '管理后台' },
    children: [
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: () => import('@/views/admin/DashBoard.vue'),
        meta: { title: '管理后台控制台' }
      },
      {
        path: 'projects',
        name: 'ProjectManagement',
        component: ProjectManagement,
        meta: { title: '项目管理' }
      },
      {
        path: 'articles',
        name: 'ArticleManagement',
        component: ArticleManagement,
        meta: { title: '文章管理' }
      },
      {
        path: 'tools',
        name: 'ToolManagement',
        component: ToolManagement,
        meta: { title: '工具管理' }
      },
      {
        path: 'resources',
        name: 'ResourceManagement',
        component: ResourceManagement,
        meta: { title: '资源管理' }
      },
      {
        path: 'profile',
        name: 'ProfileManagement',
        component: ProfileManagement,
        meta: { title: '自我信息管理' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
