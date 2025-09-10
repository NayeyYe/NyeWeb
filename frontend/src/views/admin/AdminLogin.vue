<!-- filepath: /d:/Nayey/Code/Vue/nyeweb/frontend/src/views/AdminLogin.vue -->
<template>
  <div class="admin-login">
    <div class="login-container">
      <h2>管理员登录</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">用户名:</label>
          <input
            type="text"
            id="username"
            v-model="loginForm.username"
            required
            placeholder="请输入用户名"
          />
        </div>
        <div class="form-group">
          <label for="password">密码:</label>
          <input
            type="password"
            id="password"
            v-model="loginForm.password"
            required
            placeholder="请输入密码"
          />
        </div>
        <button type="submit" :disabled="loading">
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminLogin',
  data() {
    return {
      loginForm: {
        username: '',
        password: ''
      },
      loading: false,
      errorMessage: ''
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true;
      this.errorMessage = '';
      
      try {
        const response = await fetch('/api/admin/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.loginForm)
        });
        
        const data = await response.json();
        
        if (response.ok) {
          // 保存token到localStorage
          localStorage.setItem('adminToken', data.token);
          // 跳转到管理后台
          this.$router.push('/admin/dashboard');
        } else {
          this.errorMessage = data.detail || '管理员登录错误';
        }
      } catch (error) {
        console.error('登录请求失败:', error);
        this.errorMessage = '登录失败，请检查网络连接';
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.admin-login {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
  padding-top: 55px; /* 为固定Header留出空间 */
}

.login-container {
  background: white;
  padding: 40px;
  border-radius: 20px; /* 更圆润的边角，与Header保持一致 */
  box-shadow: 0 2px 8px #f0f1f2; /* 与Header统一的阴影效果 */
  width: 100%;
  max-width: 400px;
}

h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 5px;
  color: #555;
}

input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px; /* 输入框也使用圆润边角 */
  box-sizing: border-box;
}

button {
  width: 100%;
  padding: 12px;
  background-color: #409eff; /* 使用与网站主题色一致的蓝色 */
  color: white;
  border: none;
  border-radius: 8px; /* 按钮圆润边角 */
  cursor: pointer;
  font-size: 16px;
}

button:hover {
  background-color: #337ecc; /* hover颜色与Logo保持一致 */
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.error-message {
  color: #dc3545;
  text-align: center;
  margin-top: 15px;
}
</style>