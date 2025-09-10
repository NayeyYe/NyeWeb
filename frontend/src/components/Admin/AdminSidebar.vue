<template>
  <div class="admin-sidebar">
    <div class="sidebar-header">
      <h2>Nye Web</h2>
      <h3>管理面板</h3>
    </div>

    <el-menu
      :default-active="activeMenu"
      class="sidebar-menu"
      router
      unique-opened
    >
      <el-menu-item index="/admin/dashboard" class="menu-item">
        <el-icon><House /></el-icon>
        <span>控制台</span>
      </el-menu-item>

      <el-menu-item index="/admin/projects" class="menu-item">
        <el-icon><Folder /></el-icon>
        <span>项目管理</span>
      </el-menu-item>

      <el-menu-item index="/admin/articles" class="menu-item">
        <el-icon><Document /></el-icon>
        <span>文章管理</span>
      </el-menu-item>

      <el-menu-item index="/admin/tools" class="menu-item">
        <el-icon><Tools /></el-icon>
        <span>工具管理</span>
      </el-menu-item>

      <el-menu-item index="/admin/resources" class="menu-item">
        <el-icon><Box /></el-icon>
        <span>资源管理</span>
      </el-menu-item>

      <el-menu-item index="/admin/profile" class="menu-item">
        <el-icon><User /></el-icon>
        <span>自我信息管理</span>
      </el-menu-item>
    </el-menu>

    <div class="sidebar-footer">
      <el-menu class="footer-menu">
        <el-menu-item @click="goHome" class="footer-menu-item">
          <el-icon><HomeFilled /></el-icon>
          <span>返回首页</span>
        </el-menu-item>

        <el-menu-item @click="logout" class="footer-menu-item logout-item">
          <el-icon><SwitchButton /></el-icon>
          <span>退出登录</span>
        </el-menu-item>
      </el-menu>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { House, Folder, Document, Tools, Box, User, SwitchButton, HomeFilled } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

const activeMenu = computed(() => route.path)

const goHome = () => {
  router.push('/')
}

const logout = () => {
  localStorage.removeItem('adminToken')
  router.push('/admin/login')
}
</script>

<style scoped>
.admin-sidebar {
  position: fixed;
  left: 0;
  top: 0;
  width: 250px;
  height: 100vh;
  background: #ffffff;
  border-right: 1px solid #f0f0f0;
  display: flex;
  flex-direction: column;
  box-shadow: 4px 0 12px rgba(0, 0, 0, 0.05);
  z-index: 100;
}

.sidebar-header {
  padding: 30px 20px 20px 20px;
  border-bottom: 1px solid #f0f0f0;
  text-align: center;
  background: #ffffff;
}

.sidebar-header h2 {
  margin: 0 0 8px 0;
  color: #409eff;
  font-size: 24px;
  font-weight: bold;
}

.sidebar-header h3 {
  margin: 0;
  color: #666;
  font-size: 16px;
  font-weight: normal;
}

.sidebar-menu {
  flex: 1;
  border: none !important;
  background: #ffffff;
}

.menu-item {
  height: 56px !important;
  line-height: 56px !important;
}

.menu-item:hover {
  background-color: #f8f9fa !important;
}

.sidebar-footer {
  border-top: 1px solid #f0f0f0;
  background: #ffffff;
}

.footer-menu {
  border: none !important;
  background: #ffffff;
}

.footer-menu-item {
  height: 50px !important;
  line-height: 50px !important;
}

.footer-menu-item:hover {
  background-color: #f8f9fa !important;
}

.logout-item:hover {
  background-color: #fef0f0 !important;
  color: #f56c6c !important;
}
</style>
