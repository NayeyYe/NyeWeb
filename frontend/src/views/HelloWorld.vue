<!-- filepath: /d:/Nayey/Code/Vue/nyeweb/frontend/src/views/HelloWorld.vue -->
<template>
  <div class="hello-world">
    <div class="container">
      <h1>欢迎来到管理后台!</h1>
      <p>您已成功登录管理员系统。</p>
      <div class="admin-info">
        <h3>管理功能（即将开发）:</h3>
        <ul>
          <li>文章管理</li>
          <li>项目管理</li>
          <li>用户管理</li>
          <li>系统设置</li>
        </ul>
      </div>
      <button @click="logout" class="logout-btn">退出登录</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  methods: {
    logout() {
      localStorage.removeItem('adminToken');
      this.$router.push('/admin/login');
    }
  }
}
</script>

<style scoped>
.hello-world {
  padding: 40px;
  text-align: center;
}

.container {
  max-width: 800px;
  margin: 0 auto;
}

h1 {
  color: #2c3e50;
  margin-bottom: 20px;
}

.admin-info {
  background-color: #f8f9fa;
  padding: 30px;
  border-radius: 8px;
  margin: 30px 0;
}

ul {
  text-align: left;
  display: inline-block;
}

li {
  margin: 10px 0;
}

.logout-btn {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.logout-btn:hover {
  background-color: #c82333;
}
</style>