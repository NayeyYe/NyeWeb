<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

// 判断是否为管理员页面
const isAdminPage = computed(() => {
  return route.path.startsWith('/admin')
})

// 判断是否为管理员登录页面（只在登录页显示Header）
const isAdminLogin = computed(() => {
  return route.path === '/admin/login'
})
</script>

<template>
  <!--  这是我的网站的顶栏  -->
  <el-header class="fixed-header" v-if="!isAdminPage || isAdminLogin">
    <!-- 管理员登录页面的简化Header -->
    <div v-if="isAdminLogin" class="admin-header">
      <!-- 左侧Logo -->
      <div class="admin-logo-section">
        <router-link to="/" class="admin-logo-link" title="转跳到首页">
          <span class="admin-logo-text">Nye Web</span>
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
    <el-row v-else justify="space-between" align="middle" style="height: 100%; width: 100%;">
      <!-- 左侧 Logo/Icon -->
      <el-col :span="4">
        <div class="logo-section">
          <router-link to="/" class="logo-link">
            <span class="logo-text">Nye Web</span>
          </router-link>
        </div>
      </el-col>

      <!-- 中间导航选项 -->
      <el-col :span="16">
        <div class="nav-center">
          <el-menu mode="horizontal" class="nav-menu" :ellipsis="false" router>
            <el-menu-item index="/">首页</el-menu-item>
            <el-menu-item index="/projects">项目</el-menu-item>
            <el-menu-item index="/knowledge">知识</el-menu-item>
            <el-menu-item index="/tools">小工具</el-menu-item>
            <el-menu-item index="/resources">资源</el-menu-item>
          </el-menu>
        </div>
      </el-col>

      <!-- 右侧头像和关于我 -->
      <el-col :span="4">
        <div class="user-section">
          <router-link to="/about" class="user-info-link">
            <span class="about-me">关于我</span>
          </router-link>
          <router-link to="/admin/login" class="avatar-link">
            <el-avatar size="small" class="user-avatar">
              <img src="/avatar.jpg" alt="用户头像" />
            </el-avatar>
          </router-link>
        </div>
      </el-col>
    </el-row>
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
</style>
