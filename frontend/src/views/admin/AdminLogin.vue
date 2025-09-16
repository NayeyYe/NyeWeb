<!-- filepath: /d:/Nayey/Code/Vue/nyeweb/frontend/src/views/AdminLogin.vue -->
<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <h2>管理员登录</h2>
        <p>请输入您的凭据以访问管理后台</p>
      </div>

      <el-form
        :model="loginForm"
        class="login-form"
        @submit.prevent="handleLogin"
      >
        <el-form-item>
          <el-input
            v-model="loginForm.username"
            placeholder="用户名"
            prefix-icon="User"
            size="large"
          />
        </el-form-item>

        <el-form-item>
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="密码"
            prefix-icon="Lock"
            size="large"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            size="large"
            class="login-button"
            :loading="loading"
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const router = useRouter()
const loading = ref(false)

const loginForm = reactive({
  username: '',
  password: ''
})

const handleLogin = async () => {
  if (!loginForm.username || !loginForm.password) {
    ElMessage.error('请输入用户名和密码')
    return
  }

  loading.value = true

  try {
    const response = await axios.post('/api/admin/login', {
      username: loginForm.username,
      password: loginForm.password
    })

    if (response.data && response.data.token) {
      // 保存登录信息
      localStorage.setItem('admin_token', response.data.token)
      localStorage.setItem('admin_logged_in', 'true')
      localStorage.setItem('admin_username', response.data.username)

      ElMessage.success('登录成功')

      // 获取重定向地址
      const redirect = router.currentRoute.value.query.redirect || '/admin/dashboard'
      router.push(redirect)
    } else {
      ElMessage.error('登录失败')
    }
  } catch (error) {
    console.error('登录失败:', error)
    if (error.response && error.response.status === 401) {
      ElMessage.error('用户名或密码错误')
    } else {
      ElMessage.error('登录失败，请稍后重试')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #ffffff;
  padding: 20px;
}

.login-box {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 1px solid #e1e8ed;
  width: 100%;
  max-width: 400px;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h2 {
  color: #333;
  margin-bottom: 8px;
  font-weight: 600;
}

.login-header p {
  color: #666;
  font-size: 14px;
}

.login-form {
  width: 100%;
}

.login-button {
  width: 100%;
}

:deep(.el-input__wrapper) {
  border-radius: 8px;
}

:deep(.el-button) {
  border-radius: 8px;
}
</style>