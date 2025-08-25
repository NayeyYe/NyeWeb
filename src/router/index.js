import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Knowledge from '../views/Knowledge.vue'

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
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
