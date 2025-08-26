<script setup>
import '@/assets/styles/header.css';
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
            <el-menu-item index="/Dailylife">日常和随笔</el-menu-item>
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
.user-info-link {
  text-decoration: none;
  color: inherit;
  display: inline-block;
}
</style>
