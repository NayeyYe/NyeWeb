<script setup>
</script>

<template>
  <!--  这是我的网站的顶栏  -->
  <el-header class="fixed-header">
    <el-row justify="space-between" align="middle" style="height: 100%; width: 100%;">
      <!-- 左侧 Logo/Icon -->
      <el-col :span="4">
        <div class="logo-section">
          <span class="logo-text">Nye Web</span>
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
            <div class="user-info">
              <span class="about-me">关于我</span>
              <el-avatar size="small" class="user-avatar">
                <img src="/avatar.jpg" alt="用户头像" />
              </el-avatar>
            </div>
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
  box-shadow: 0 2px 8px #f0f1f2;
  border-radius: 20px;
  background: #fff;
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

.user-section {
  display: flex;
  justify-content: flex-end;
  align-items: center;
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
</style>
