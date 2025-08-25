<template>
  <el-card class="profile-card">
    <div class="card-content">
      <el-avatar :size="100" src="/avatar.jpg" />
      <h2 class="name">Nye Ye</h2>
      <p class="title">废物一位</p>
      <div class="social-links">
        <a href="https://github.com/your-github-username" target="_blank" class="social-link" title="GitHub">G</a>
        <a href="mailto:NayeyYe@163.com" class="social-link" title="Email">E</a>
        <a href="#" class="social-link" title="Twitter">T</a>
      </div>
      <el-divider />
      <div class="contact-info">
        <p><span class="icon">在读院校:</span> <el-link href="https://www.whu.edu.cn/" target="_blank">武汉大学</el-link></p>
        <p><span class="icon">Email:</span> <el-link href="mailto:NayeyYe@163.com">NayeyYe@163.com</el-link></p>
        <p><span class="icon">Tel:</span> <span>+86-13597646338</span></p>
      </div>
    </div>
  </el-card>
</template>
.

<script setup>
// 此组件无需脚本
</script>

<style scoped>
.profile-card {
  width: 300px;
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
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
