<template>
  <div class="home-container">
    <div class="left-column">
      <ProfileCard class="profile-card-container" />
      <ImageCarousel class="image-carousel-container" />
    </div>
    <el-card class="intro-card">
      <!-- 英雄区域 -->
      <div class="hero-section">
        <h1>你好，我是 [你的名字]</h1>
        <p class="subtitle">一位热情的 [你的职业，如：前端开发者]</p>
        <p>欢迎来到我的个人空间。在这里，你可以了解我的项目、技术栈和个人思考。</p>
      </div>

      <el-divider />

      <!-- 关于我 -->
      <div class="about-section">
        <h2>关于我</h2>
        <p>我专注于 [你擅长的领域]，致力于构建高质量、用户友好的 Web 应用。我对 [你感兴趣的技术或方向] 充满热情，并乐于探索新的技术和解决方案。</p>
      </div>

      <el-divider />

      <!-- 技术栈 -->
      <div class="skills-section">
        <h2>技术栈</h2>
        <el-tag type="primary" class="skill-tag">Vue.js</el-tag>
        <el-tag type="success" class="skill-tag">JavaScript</el-tag>
        <el-tag type="info" class="skill-tag">HTML5 & CSS3</el-tag>
        <el-tag type="warning" class="skill-tag">Node.js</el-tag>
        <el-tag type="danger" class="skill-tag">Element Plus</el-tag>
        <!-- 在这里添加更多技术标签 -->
      </div>

      <el-divider />

      <!-- 联系方式 -->
      <div class="contact-section">
        <h2>联系我</h2>
        <p>你可以在以下平台找到我：</p>
        <el-button type="primary" plain>GitHub</el-button>
        <el-button type="success" plain>LinkedIn</el-button>
        <el-button type="info" plain>Email</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import ProfileCard from '@/components/Main/Home/ProfileCard.vue'
import ImageCarousel from '@/components/Main/MyInfo/ImageCarousel.vue'
</script>

<style scoped>
.home-container {
  padding-top: 80px; /* 为固定的顶栏留出空间 */
  padding-bottom: 40px;
  max-width: 1280px;
  margin: 0 auto;
  display: flex;
  align-items: flex-start;
  gap: 20px;
  padding-left: 20px;
  padding-right: 20px;
}

.left-column {
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 350px; /* 您可以根据ProfileCard的宽度进行调整 */
  flex-shrink: 0;
}

.profile-card-container {
  position: sticky;
  top: 80px; /* 80px 是顶栏高度 */
  width: 100%;
}

.image-carousel-container {
  width: 100%;
}

.intro-card {
  flex: 1;
  padding: 20px;
  border-radius: 15px;
}

.hero-section h1 {
  font-size: 2.5em;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 1.5em;
  color: #606266;
  margin-bottom: 20px;
}

.about-section, .skills-section, .contact-section {
  margin-top: 30px;
}

h2 {
  font-size: 1.8em;
  margin-bottom: 15px;
  border-left: 4px solid #409eff;
  padding-left: 10px;
}

p {
  line-height: 1.8;
  color: #303133;
}

.skill-tag {
  margin: 5px;
  font-size: 14px;
}

.contact-section .el-button {
  margin: 5px;
}
</style>
