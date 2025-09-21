<script setup>
import {computed, ref, onMounted, onUnmounted} from 'vue'
import {useRoute} from 'vue-router'
import {Menu as IconMenu} from '@element-plus/icons-vue'

const route = useRoute()

// 判断是否为管理员页面
const isAdminPage = computed(() => {
  return route.path.startsWith('/admin')
})

// 判断是否为管理员登录页面(只在登录页显示Header)
const isAdminLogin = computed(() => {
  return route.path === '/admin/login'
})

// 滚动显示/隐藏Header逻辑
const isHeaderVisible = ref(true)
let lastScrollTop = 0

const handleScroll = () => {
  const scrollTop = window.pageYOffset || document.documentElement.scrollTop
  
  if (scrollTop > lastScrollTop && scrollTop > 100) {
    // 向下滚动超过100px，隐藏Header
    isHeaderVisible.value = false
  } else if (scrollTop < lastScrollTop) {
    // 向上滚动，显示Header
    isHeaderVisible.value = true
  }
  
  lastScrollTop = scrollTop
}

// 响应式菜单相关
const isMenuOpen = ref(false)

// 切换菜单开关
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

// 关闭菜单
const closeMenu = () => {
  isMenuOpen.value = false
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  
  // 点击其他地方关闭菜单
  const handleClickOutside = (event) => {
    const menu = document.querySelector('.mobile-menu')
    const hamburger = document.querySelector('.hamburger')
    if (menu && !menu.contains(event.target) && hamburger && !hamburger.contains(event.target)) {
      closeMenu()
    }
  }
  
  window.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<template>
  <!--  这是我的网站的顶栏  -->
  <el-header v-if="!isAdminPage || isAdminLogin" :class="['fixed-header', { 'header-hidden': !isHeaderVisible }]">
    <!-- 管理员登录页面的简化Header -->
    <div v-if="isAdminLogin" class="admin-header">
      <!-- 左侧Logo -->
      <div class="admin-logo-section">
        <router-link class="admin-logo-link" title="转跳到首页" to="/">
          <span class="admin-logo-text">NyeWeb</span>
        </router-link>
      </div>

      <!-- 中间标题 -->
      <div class="admin-title">
        <span class="admin-title-text">管理员登录</span>
      </div>

      <!-- 右侧占位，保持布局平衡 -->
      <div class="admin-placeholder"></div>
    </div>

<!-- 普通页面的完整Header -->
    <div v-else class="main-header">
      <!-- 左侧 Logo/Icon 和 汉堡菜单 -->
      <div class="header-left">
        <router-link class="logo-link" to="/">
          <span class="logo-text">NyeWeb</span>
        </router-link>
        <el-icon class="hamburger" @click="toggleMenu">
          <IconMenu/>
        </el-icon>
      </div>

      <!-- 中间导航选项 (大屏幕) -->
      <div class="nav-center">
        <el-menu :ellipsis="false" class="nav-menu" mode="horizontal" router>
          <el-menu-item index="/">首页</el-menu-item>
          <el-menu-item index="/projects">项目</el-menu-item>
          <el-menu-item index="/knowledge">知识</el-menu-item>
          <el-menu-item index="/tools">小工具</el-menu-item>
          <el-menu-item index="/resources">资源</el-menu-item>
        </el-menu>
      </div>

      <!-- 右侧头像和关于我 -->
      <div class="header-right">
        <router-link class="user-info-link" to="/about">
          <span class="about-me">关于我</span>
        </router-link>
        <router-link class="avatar-link" to="/admin/login">
          <el-avatar class="user-avatar" size="small">
            <img alt="用户头像" src="/avatar.jpg"/>
          </el-avatar>
        </router-link>
      </div>
    </div>

    <!-- 移动端菜单 -->
    <div v-if="isMenuOpen" class="mobile-menu">
      <router-link @click="closeMenu" class="mobile-menu-item" to="/">首页</router-link>
      <router-link @click="closeMenu" class="mobile-menu-item" to="/projects">项目</router-link>
      <router-link @click="closeMenu" class="mobile-menu-item" to="/knowledge">知识</router-link>
      <router-link @click="closeMenu" class="mobile-menu-item" to="/tools">小工具</router-link>
      <router-link @click="closeMenu" class="mobile-menu-item" to="/resources">资源</router-link>
    </div>
  </el-header>
</template>

<style scoped>
.fixed-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  height: 55px;
  display: flex;
  align-items: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border-radius: 0;
  background: #ffffff;
  border-bottom: 1px solid #f0f0f0;
}

/* Header显示/隐藏动画 */
.fixed-header {
  transition: transform 0.3s ease-in-out;
}

.header-hidden {
  transform: translateY(-100%);
}

/* 管理员页面Header样式 */
.admin-header {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
  padding: 0 60px;
  background: #ffffff;
}

.admin-logo-section {
  flex: 1;
  display: flex;
  justify-content: flex-start;
}

.admin-logo-link {
  text-decoration: none;
  color: inherit;
  position: relative;
}

.admin-logo-text {
  font-size: 20px;
  font-weight: bold;
  color: #409eff;
  cursor: pointer;
}

.admin-logo-link:hover .admin-logo-text {
  color: #337ecc;
}

.admin-title {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.admin-title-text {
  font-size: 20px;
  font-weight: bold;
  color: #409eff;
}

.admin-placeholder {
  flex: 1;
}

.logo-section {
  display: flex;
  align-items: center;
  padding-left: 60px;
}

.logo-text {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
}

.nav-center {
  display: flex;
  justify-content: center;
  height: 100%;
}

.nav-menu {
  height: 100%;
  border-bottom: none !important;
  background: transparent !important;
}

.nav-menu .el-menu-item {
  height: 100%;
  display: flex;
  align-items: center;
}

.nav-menu .el-menu-item:hover {
  background-color: transparent !important;
  border-bottom: 2px solid #409eff;
}

.logo-link {
  text-decoration: none;
  color: inherit;
}

.logo-link:hover .logo-text {
  color: #337ecc;
}

.user-section {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 15px;
  padding-right: 100px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 20px;
}

.about-me {
  font-size: 14px;
  color: #666;
  cursor: pointer;
}

.about-me:hover {
  color: #409eff;
}

.user-avatar {
  cursor: pointer;
}

.user-info-link {
  text-decoration: none;
  color: inherit;
  display: inline-block;
}

.avatar-link {
  text-decoration: none;
  display: inline-block;
}

.avatar-link:hover .user-avatar {
  transform: scale(1.1);
  transition: transform 0.2s ease;
}

/* 新增的响应式样式 */
.main-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  height: 100%;
  padding: 0 40px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.hamburger {
  display: none;
  font-size: 24px;
  cursor: pointer;
  color: #409eff;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 15px;
}

/* 移动端菜单样式 */
.mobile-menu {
  position: absolute;
  top: 55px;
  left: 0;
  right: 0;
  background: #ffffff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  z-index: 999;
  display: none;
  flex-direction: column;
  padding: 10px 0;
}

.mobile-menu-item {
  padding: 15px 20px;
  text-decoration: none;
  color: #333;
  font-size: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.mobile-menu-item:last-child {
  border-bottom: none;
}

.mobile-menu-item:hover {
  background-color: #f5f7fa;
  color: #409eff;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .hamburger {
    display: block;
  }
  
  .nav-center {
    display: none;
  }
  
  .mobile-menu {
    display: flex;
  }
  
  .main-header {
    padding: 0 20px;
  }
  
  .header-right {
    gap: 10px;
  }
}

@media (min-width: 769px) {
  .mobile-menu {
    display: none !important;
  }
}
</style>
