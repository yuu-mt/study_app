<template>
  <div class="login-container">
    <div class="logo">
      <h1>📚 StudyTracker</h1>
      <p>学習を記録して、友達と競おう</p>
    </div>

    <div class="card">
      <div class="form-group">
        <label>メールアドレス</label>
        <input v-model="email" type="email" placeholder="example@email.com" />
      </div>

      <div class="form-group">
        <label>パスワード</label>
        <input v-model="password" type="password" placeholder="パスワードを入力" />
      </div>

      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

      <button class="btn-login" @click="login" :disabled="isLoading">
        {{ isLoading ? 'ログイン中...' : 'ログイン' }}
      </button>

      <div class="register-link">
        アカウントをお持ちでない方は
        <a @click="router.push('/register')">新規登録</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const email = ref('')
const password = ref('')
const errorMessage = ref('')
const isLoading = ref(false)

const login = async () => {
  errorMessage.value = ''
  isLoading.value = true

  try {
    const response = await axios.post('http://127.0.0.1:8000/api/accounts/login/', {
      email: email.value,
      password: password.value
    })

    // トークンをlocalStorageに保存
    localStorage.setItem('access_token', response.data.access)
    localStorage.setItem('refresh_token', response.data.refresh)

    // トップページへ遷移（後で作る）
    router.push('/home')

  } catch (error) {
    errorMessage.value = 'メールアドレスまたはパスワードが違います'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #f8faff;
  padding: 24px;
}

.logo {
  text-align: center;
  margin-bottom: 32px;
}

.logo h1 {
  font-size: 28px;
  font-weight: 800;
  color: #2563eb;
  margin-bottom: 6px;
}

.logo p {
  font-size: 14px;
  color: #64748b;
}

.card {
  background: white;
  border-radius: 16px;
  padding: 28px 24px;
  width: 100%;
  max-width: 400px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 20px rgba(37, 99, 235, 0.08);
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 6px;
}

.form-group input {
  width: 100%;
  padding: 12px 14px;
  border: 1.5px solid #e2e8f0;
  border-radius: 10px;
  font-size: 15px;
  outline: none;
  box-sizing: border-box;
  transition: border-color 0.2s;
}

.form-group input:focus {
  border-color: #2563eb;
}

.error-message {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 13px;
  margin-bottom: 16px;
}

.btn-login {
  width: 100%;
  padding: 13px;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: opacity 0.2s;
}

.btn-login:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.register-link {
  text-align: center;
  margin-top: 20px;
  font-size: 13px;
  color: #64748b;
}

.register-link a {
  color: #2563eb;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
}
</style>