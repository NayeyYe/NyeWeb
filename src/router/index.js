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
    path: '/knowledge/:path+', // 使用 :path+ 匹配层级路径，如 /knowledge/category/slug
    name: 'Article',
    component: Article
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
