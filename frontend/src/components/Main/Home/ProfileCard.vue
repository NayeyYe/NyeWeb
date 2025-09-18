<template>
  <el-card class="profile-card">
    <div class="card-content">
      <el-avatar :size="100" src="/avatar.jpg"/>
      <h2 class="name">卟瓿钚</h2>
      <p class="title">一名普通大学生</p>
      <div class="social-links">
        <a class="social-link" href="https://github.com/NayeyYe" target="_blank" title="GitHub">
          <img :src="githubIcon" alt="GitHub" class="social-icon"/>
        </a>
        <a class="social-link" href="https://blog.csdn.net/2302_77222155?type=blog" target="_blank" title="CSDN">
          <img :src="csdnIcon" alt="CSDN" class="social-icon"/>
        </a>
        <a class="social-link" href="https://x.com/NayeyYeX" target="_blank" title="Twitter">
          <img :src="twitterIcon" alt="Twitter" class="social-icon"/>
        </a>
      </div>
      <el-divider/>
      <div class="contact-info">
        <p><span class="icon">在读院校:</span>
          <el-link href="https://www.whu.edu.cn/" target="_blank">武汉大学</el-link>
        </p>
        <p><span class="icon">Email:</span>
          <el-link href="mailto:Nayey.Ye@outlook.com">NayeyYe@163.com</el-link>
        </p>
        <p><span class="icon">Tel:</span> <span>+86-13597646338</span></p>
      </div>
    </div>
  </el-card>
</template>

<script setup>
// 导入SVG图标
import githubIcon from '/github.svg'
import csdnIcon from '/csdn.svg'
import twitterIcon from '/twitter.svg'
</script>

<style scoped>
.profile-card {
  width: 350px;
  box-sizing: border-box; /* 确保宽度包含内边距和边框 */
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
  padding: 20px;
  background-color: #fff;
}

.card-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.name {
  margin-top: 20px;
  font-size: 1.5em;
  font-weight: bold;
  color: #303133;
}

.title {
  color: #606266;
  margin-top: 5px;
}

.social-links {
  margin-top: 20px;
}

.social-link {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  width: 40px;
  height: 40px;
  margin: 0 10px;
  border-radius: 50%;
  background-color: #f0f2f5;
  color: #303133;
  text-decoration: none;
  font-weight: bold;
  font-size: 1.2em;
  transition: all 0.3s ease;
}

.social-link:hover {
  background-color: #409eff;
  color: #fff;
  transform: translateY(-2px);
}

.social-icon {
  width: 20px;
  height: 20px;
  transition: all 0.3s ease;
  filter: brightness(0) saturate(100%) invert(20%) sepia(6%) saturate(1007%) hue-rotate(194deg) brightness(94%) contrast(89%);
}

.social-link:hover .social-icon {
  filter: brightness(0) saturate(100%) invert(100%) sepia(0%) saturate(7500%) hue-rotate(109deg) brightness(105%) contrast(105%);
}

.el-divider {
  margin: 20px 0;
}

.contact-info {
  text-align: left;
  width: 100%;
  color: #606266;
  font-size: 0.9em;
}

.contact-info p {
  margin: 10px 0;
  display: flex;
  align-items: center;
}

.contact-info .el-link {
  font-size: 1em;
  position: relative;
  top: -1px;
}

.contact-info .icon {
  margin-right: 10px;
  font-style: normal;
}
</style>
