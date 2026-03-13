<template>
  <div class="register-container">
    <div class="logo">
      <h1>📚 StudyTracker</h1>
      <p>アカウントを作成して始めよう</p>
    </div>

    <div class="card">
      <div class="form-group">
        <label>ユーザー名</label>
        <input v-model="username" type="text" placeholder="ユーザー名を入力" />
      </div>

      <div class="form-group">
        <label>メールアドレス</label>
        <input v-model="email" type="email" placeholder="example@email.com" />
      </div>

      <div class="form-group">
        <label>パスワード（8文字以上）</label>
        <input v-model="password" type="password" placeholder="パスワードを入力" />
      </div>

      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

      <button class="btn-register" @click="register" :disabled="isLoading">
        {{ isLoading ? '登録中...' : '新規登録' }}
      </button>

      <div class="login-link">
        すでにアカウントをお持ちの方は
        <a @click="router.push('/login')">ログイン</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const username = ref('')
const email = ref('')
const password = ref('')
const errorMessage = ref('')
const successMessage = ref('')
const isLoading = ref(false)

const register = async () => {
  errorMessage.value = ''
  successMessage.value = ''
  isLoading.value = true

  try {
    await axios.post('http://127.0.0.1:8000/api/accounts/register/', {
      username: username.value,
      email: email.value,
      password: password.value
    })

    successMessage.value = '登録完了！ログイン画面に移動します...'

    // 2秒後にログイン画面へ遷移
    setTimeout(() => {
      router.push('/login')
    }, 2000)

  } catch (error) {
    if (error.response?.data?.email) {
      errorMessage.value = 'このメールアドレスはすでに登録されています'
    } else if (error.response?.data?.password) {
      errorMessage.value = 'パスワードは8文字以上で入力してください'
    } else {
      errorMessage.value = '登録に失敗しました。入力内容を確認してください'
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.register-container {
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

.btn-register {
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

.btn-register:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.login-link {
  text-align: center;
  margin-top: 20px;
  font-size: 13px;
  color: #64748b;
}

.login-link a {
  color: #2563eb;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
}
</style>