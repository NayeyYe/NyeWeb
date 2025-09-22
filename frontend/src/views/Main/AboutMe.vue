<template>
  <div class="home-container">
    <div class="left-column">
      <ProfileCard class="profile-card-container"/>
      <ImageCarousel class="image-carousel-container"/>
    </div>
    <el-card class="intro-card">
<!-- 英雄区域 -->
      <div class="hero-section">
        <h1>你好，我是 卟瓿钚</h1>
        <p class="subtitle">目前是 <a href="https://www.whu.edu.cn/" class="whu-link">武汉大学</a> 在读本科生</p>
        <p>欢迎来到我的个人空间。在这里，你可以了解我的项目、技术栈和个人思考。</p>
      </div>

<el-divider/>

<!-- 就读经历 -->
      <div class="education-section">
        <h2>就读经历</h2>
        <a href="https://maths.whu.edu.cn/" target="_blank" style="text-decoration: none; color: inherit;">
          <el-card class="education-card" shadow="hover">
            <div class="education-content">
              <h3>武汉大学数学与统计学院</h3>
              <p class="education-period">2022.9 - 2026.6</p>
              <p class="education-description">本科在读</p>
            </div>
          </el-card>
        </a>
      </div>

      <el-divider/>

      <!-- 关于我 -->
      <div class="about-section">
        <h2>关于我</h2>
        <p>破大专的数学系，妄想指染机器学习的圣域，拼尽全力无法战胜</p>
      </div>

      <el-divider/>

<!-- 技术栈 -->
      <div class="skills-section">
        <h2>技术栈</h2>
        <h3>基本技能</h3>
        <el-tag class="skill-tag" type="primary">Linux</el-tag>
        <el-tag class="skill-tag" type="success">Git</el-tag>
        <el-tag class="skill-tag" type="info">Docker</el-tag>
        
        <h3 style="margin-top: 15px;">编程语言</h3>
        <el-tag class="skill-tag" type="primary">C</el-tag>
        <el-tag class="skill-tag" type="success">C++</el-tag>
        <el-tag class="skill-tag" type="info">Java</el-tag>
        <el-tag class="skill-tag" type="warning">Node.js</el-tag>
        <el-tag class="skill-tag" type="danger">Python</el-tag>
        <el-tag class="skill-tag" type="primary">Vue3</el-tag>
        
        <h3 style="margin-top: 15px;">机器学习</h3>
        <el-tag class="skill-tag" type="primary">TensorFlow</el-tag>
        <el-tag class="skill-tag" type="success">PyTorch</el-tag>
      </div>

<el-divider/>

      <!-- 兴趣爱好 -->
      <div class="hobbies-section">
        <h2>兴趣爱好</h2>
        <p>二次元（bushi）、游戏、技术宅</p>
      </div>

      <el-divider/>

<!-- 联系方式 -->
      <div class="contact-section">
        <h2>联系我</h2>
        <p>你可以在以下平台找到我：</p>
        <a href="https://github.com/NayeyYe" target="_blank" style="text-decoration: none;">
          <el-button plain type="primary">GitHub</el-button>
        </a>
        <a href="https://x.com/NayeyYeX" target="_blank" style="text-decoration: none;">
          <el-button plain type="success">X</el-button>
        </a>
        <a href="https://space.bilibili.com/68134624?spm_id_from=333.1007.0.0" target="_blank" style="text-decoration: none;">
          <el-button plain type="info">Bilibili</el-button>
        </a>
        <a href="https://blog.csdn.net/2302_77222155?spm=1000.2115.3001.5343" target="_blank" style="text-decoration: none;">
          <el-button plain type="warning">CSDN</el-button>
        </a>
        <a href="https://gitee.com/NayeyYe" target="_blank" style="text-decoration: none;">
          <el-button plain type="danger">Gitee</el-button>
        </a>
        <p style="margin-top: 15px;">个人网站: <a href="https://nyeweb.fun" target="_blank">nyeweb.fun</a></p>
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

.whu-link {
  color: #606266;
  text-decoration: none;
  transition: color 0.3s ease;
}

.whu-link:hover {
  color: #28a745; /* WHU绿色 */
}

.education-card {
  margin-top: 15px;
}

.education-content h3 {
  margin: 0 0 10px 0;
  color: #303133;
}

.education-period {
  font-weight: bold;
  color: #409eff;
  margin: 5px 0;
}

.education-description {
  color: #606266;
  margin: 5px 0;
}

.hobbies-section p {
  font-size: 16px;
  color: #303133;
}

/* 响应式布局 */
@media (max-width: 1024px) {
  .home-container {
    flex-direction: column;
  }

  .left-column {
    width: 100%;
    order: 1; /* ProfileCard 和 ImageCarousel */
  }

  .intro-card {
    order: 2; /* 个人介绍 */
  }
}

@media (max-width: 768px) {
  .home-container {
    padding: 80px 10px 20px;
  }

  .left-column {
    gap: 15px;
  }
  
  .hero-section h1 {
    font-size: 2em;
  }
  
  .subtitle {
    font-size: 1.2em;
  }
  
  h2 {
    font-size: 1.5em;
  }
}
</style>
