<template>
  <div class="auth-container">
    <div class="auth-card">
      <!-- ロゴ・タイトル -->
      <div class="auth-header">
        <div class="logo">📚</div>
        <h1>StudyTracker</h1>
        <p>新規アカウント登録</p>
      </div>

      <!-- エラーメッセージ -->
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <!-- 成功メッセージ -->
      <div v-if="successMessage" class="success-message">
        {{ successMessage }}
      </div>

      <div class="form-group">
        <label>ユーザー名</label>
        <input
          v-model="username"
          type="text"
          placeholder="ユーザー名を入力"
        />
      </div>

      <div class="form-group">
        <label>メールアドレス</label>
        <input
          v-model="email"
          type="email"
          placeholder="example@email.com"
        />
      </div>

      <div class="form-group">
        <label>パスワード（8文字以上）</label>
        <input
          v-model="password"
          type="password"
          placeholder="パスワードを入力"
        />
      </div>

      <button class="btn-primary" @click="register" :disabled="isLoading">
        {{ isLoading ? '登録中...' : 'アカウント登録' }}
      </button>

      <p class="auth-link">
        すでにアカウントをお持ちの方は
        <RouterLink to="/login">ログイン</RouterLink>
      </p>
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
.auth-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.auth-card {
  background: white;
  border-radius: 20px;
  padding: 40px 32px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

.auth-header {
  text-align: center;
  margin-bottom: 32px;
}

.logo {
  font-size: 48px;
  margin-bottom: 8px;
}

.auth-header h1 {
  font-size: 24px;
  font-weight: 700;
  color: #1a1a2e;
  margin: 0 0 4px 0;
}

.auth-header p {
  color: #888;
  font-size: 14px;
  margin: 0;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #444;
  margin-bottom: 6px;
}

.form-group input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e8e8e8;
  border-radius: 10px;
  font-size: 16px;
  outline: none;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.form-group input:focus {
  border-color: #667eea;
}

.btn-primary {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 8px;
  transition: opacity 0.2s;
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error-message {
  background: #fff0f0;
  border: 1px solid #ffcccc;
  color: #e53e3e;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 14px;
  margin-bottom: 16px;
}

.success-message {
  background: #f0fff4;
  border: 1px solid #9ae6b4;
  color: #276749;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 14px;
  margin-bottom: 16px;
}

.auth-link {
  text-align: center;
  font-size: 14px;
  color: #888;
  margin-top: 20px;
}

.auth-link a {
  color: #667eea;
  font-weight: 600;
  text-decoration: none;
}
</style>