<template>
  <div>
    <!-- 汉堡按钮 (仅在小屏幕上显示) -->
    <div v-if="isMobile" class="hamburger" @click="toggleMobileMenu">
      <el-icon size="24px"><Menu /></el-icon>
    </div>

    <!-- 移动端小列表菜单 -->
    <div 
      v-if="isMobile && mobileMenuVisible" 
      class="mobile-menu-overlay" 
      @click="hideMobileMenu"
    >
      <div class="mobile-menu" @click.stop>
        <div class="mobile-menu-item" @click="navigateTo('/admin/dashboard')">
          <el-icon><House /></el-icon>
          <span>控制台</span>
        </div>
        <div class="mobile-menu-item" @click="navigateTo('/admin/projects')">
          <el-icon><Folder /></el-icon>
          <span>项目管理</span>
        </div>
        <div class="mobile-menu-item" @click="navigateTo('/admin/articles')">
          <el-icon><Document /></el-icon>
          <span>文章管理</span>
        </div>
        <div class="mobile-menu-item" @click="navigateTo('/admin/tools')">
          <el-icon><Tools /></el-icon>
          <span>工具管理</span>
        </div>
        <div class="mobile-menu-item" @click="navigateTo('/admin/resources')">
          <el-icon><Box /></el-icon>
          <span>资源管理</span>
        </div>
        <div class="mobile-menu-item" @click="goHome">
          <el-icon><HomeFilled /></el-icon>
          <span>返回首页</span>
        </div>
        <div class="mobile-menu-item logout-item" @click="logout">
          <el-icon><SwitchButton /></el-icon>
          <span>退出登录</span>
        </div>
      </div>
    </div>

    <!-- 侧边栏 (仅在非移动设备上显示) -->
    <div 
      v-if="!isMobile"
      class="admin-sidebar" 
      :class="{ 'mobile-sidebar': isMobile, 'sidebar-collapsed': isMobile && !sidebarVisible }"
    >
      <div class="sidebar-header">
        <h2>NyeWeb</h2>
        <h3>管理面板</h3>
      </div>

      <el-menu
          :default-active="activeMenu"
          class="sidebar-menu"
          router
          unique-opened
      >
        <el-menu-item class="menu-item" index="/admin/dashboard">
          <el-icon>
            <House/>
          </el-icon>
          <span>控制台</span>
        </el-menu-item>

        <el-menu-item class="menu-item" index="/admin/projects">
          <el-icon>
            <Folder/>
          </el-icon>
          <span>项目管理</span>
        </el-menu-item>

        <el-menu-item class="menu-item" index="/admin/articles">
          <el-icon>
            <Document/>
          </el-icon>
          <span>文章管理</span>
        </el-menu-item>

        <el-menu-item class="menu-item" index="/admin/tools">
          <el-icon>
            <Tools/>
          </el-icon>
          <span>工具管理</span>
        </el-menu-item>

        <el-menu-item class="menu-item" index="/admin/resources">
          <el-icon>
            <Box/>
          </el-icon>
          <span>资源管理</span>
        </el-menu-item>

      </el-menu>

      <div class="sidebar-footer">
        <el-menu class="footer-menu">
          <el-menu-item class="footer-menu-item" @click="goHome">
            <el-icon>
              <HomeFilled/>
            </el-icon>
            <span>返回首页</span>
          </el-menu-item>

          <el-menu-item class="footer-menu-item logout-item" @click="logout">
            <el-icon>
              <SwitchButton/>
            </el-icon>
            <span>退出登录</span>
          </el-menu-item>
        </el-menu>
      </div>
    </div>
  </div>
</template>

<script setup>
import {computed, ref, onMounted, onBeforeUnmount} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import {Box, Document, Folder, HomeFilled, House, SwitchButton, Tools, Menu} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

// 响应式相关
const isMobile = ref(false)
const sidebarVisible = ref(false)
const mobileMenuVisible = ref(false)

const activeMenu = computed(() => route.path)

// 检查是否为移动设备
const checkIsMobile = () => {
  isMobile.value = window.innerWidth <= 768
  if (!isMobile.value) {
    sidebarVisible.value = true
  }
}

// 切换侧边栏显示状态
const toggleSidebar = () => {
  sidebarVisible.value = !sidebarVisible.value
}

// 切换移动端菜单显示状态
const toggleMobileMenu = () => {
  mobileMenuVisible.value = !mobileMenuVisible.value
}

// 隐藏移动端菜单
const hideMobileMenu = () => {
  mobileMenuVisible.value = false
}

// 导航到指定路径
const navigateTo = (path) => {
  router.push(path)
  // 在移动设备上，点击菜单项后隐藏菜单
  hideMobileMenu()
}

const goHome = () => {
  router.push('/')
  // 在移动设备上，点击菜单项后隐藏侧边栏或菜单
  if (isMobile.value) {
    sidebarVisible.value = false
    hideMobileMenu()
  }
}

const logout = () => {
  localStorage.removeItem('adminToken')
  router.push('/admin/login')
  // 在移动设备上，点击菜单项后隐藏侧边栏或菜单
  if (isMobile.value) {
    sidebarVisible.value = false
    hideMobileMenu()
  }
}

// 组件挂载时检查屏幕尺寸
onMounted(() => {
  checkIsMobile()
  window.addEventListener('resize', checkIsMobile)
})

// 组件卸载前移除事件监听器
onBeforeUnmount(() => {
  window.removeEventListener('resize', checkIsMobile)
})
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
  transition: transform 0.3s ease;
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

/* 汉堡按钮样式 */
.hamburger {
  position: fixed;
  top: 15px;
  left: 15px;
  z-index: 101;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #409eff;
  color: white;
  border-radius: 5px;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

/* 移动端菜单样式 */
.mobile-menu-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1000;
}

.mobile-menu {
  position: fixed;
  top: 60px;
  left: 15px;
  width: 200px;
  background: #ffffff;
  border-radius: 5px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1001;
}

.mobile-menu-item {
  display: flex;
  align-items: center;
  padding: 12px 15px;
  cursor: pointer;
  border-bottom: 1px solid #f0f0f0;
}

.mobile-menu-item:last-child {
  border-bottom: none;
}

.mobile-menu-item:hover {
  background-color: #f8f9fa;
}

.mobile-menu-item.logout-item:hover {
  background-color: #fef0f0;
  color: #f56c6c;
}

.mobile-menu-item .el-icon {
  margin-right: 10px;
  font-size: 18px;
}

/* 移动端侧边栏样式 */
.mobile-sidebar {
  transform: translateX(-100%);
}

.mobile-sidebar:not(.sidebar-collapsed) {
  transform: translateX(0);
}

/* 平板及以下设备的额外样式调整 */
@media (max-width: 768px) {
  .admin-sidebar {
    width: 220px;
  }
  
  .sidebar-header {
    padding: 20px 15px 15px 15px;
  }
  
  .sidebar-header h2 {
    font-size: 20px;
  }
  
  .sidebar-header h3 {
    font-size: 14px;
  }
  
  .menu-item {
    height: 50px !important;
    line-height: 50px !important;
    padding-left: 15px !important;
  }
  
  .footer-menu-item {
    height: 45px !important;
    line-height: 45px !important;
    padding-left: 15px !important;
  }
}

@media (max-width: 480px) {
  .admin-sidebar {
    width: 200px;
  }
  
  .sidebar-header {
    padding: 15px 10px 10px 10px;
  }
  
  .sidebar-header h2 {
    font-size: 18px;
  }
  
  .sidebar-header h3 {
    font-size: 12px;
  }
  
  .menu-item {
    height: 45px !important;
    line-height: 45px !important;
    padding-left: 10px !important;
    font-size: 14px;
  }
  
  .footer-menu-item {
    height: 40px !important;
    line-height: 40px !important;
    padding-left: 10px !important;
    font-size: 14px;
  }
}
</style>
