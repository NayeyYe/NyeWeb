import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Knowledge from '../views/Knowledge.vue'
import Article from '../views/Article.vue' // 导入文章页面

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/knowledge',
    name: 'Knowledge',
    component: Knowledge
  },
  {
    path: '/knowledge/:slug', // 使用简洁的 slug 作为文章路由
    name: 'Article',
    component: Article
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
