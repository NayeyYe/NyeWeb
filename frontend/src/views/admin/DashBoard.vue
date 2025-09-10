<!-- filepath: /d:/Nayey/Code/Vue/nyeweb/frontend/src/views/HelloWorld.vue -->
<template>
  <div class="dashboard-layout">
    <AdminSidebar />
    <div class="main-content">
      <router-view v-if="$route.path !== '/admin/dashboard'" />
      <div v-else class="welcome-panel">
        <div class="welcome-container">
          <h1>欢迎来到管理后台!</h1>
          <p>您已成功登录管理员系统。</p>
          <div class="admin-info">
            <h3>管理功能:</h3>
            <ul>
              <li>项目管理 - 管理网站展示的项目信息</li>
              <li>文章管理 - 管理知识分享文章</li>
              <li>工具管理 - 管理小工具功能</li>
              <li>资源管理 - 管理下载资源</li>
              <li>自我信息管理 - 管理个人信息展示</li>
            </ul>
          </div>
          <p class="tip">请从左侧侧边栏选择要管理的功能模块。</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import AdminSidebar from '@/components/Admin/AdminSidebar.vue'
</script>

<style scoped>
.dashboard-layout {
  display: flex;
  height: 100vh;
}

.main-content {
  flex: 1;
  margin-left: 250px;
  padding: 20px;
  background-color: #fafbfc;
  overflow-y: auto;
}

.welcome-panel {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.welcome-container {
  background: #ffffff;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  max-width: 600px;
  text-align: center;
  border: 1px solid #f0f0f0;
}

h1 {
  color: #409eff;
  margin-bottom: 20px;
}

.admin-info {
  background-color: #f8f9fa;
  padding: 30px;
  border-radius: 8px;
  margin: 30px 0;
  border: 1px solid #e9ecef;
}

.admin-info h3 {
  color: #2c3e50;
  margin-bottom: 20px;
}

ul {
  text-align: left;
  display: inline-block;
}

li {
  margin: 10px 0;
  color: #666;
}

.tip {
  color: #909399;
  font-style: italic;
  margin-top: 20px;
}
</style>