<template>
    <div class="container">
        <div class="logo">
        <h1>📚 StudyTracker</h1>
        <p>パスワードをリセット</p>
        </div>

        <div class="card">
        <div v-if="!sent">
            <p class="description">登録したメールアドレスを入力してください。パスワードリセット用のリンクをお送りします。</p>
            <div class="form-group">
            <label>メールアドレス</label>
            <input v-model="email" type="email" placeholder="example@email.com" />
            </div>
            <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
            <button class="btn-primary" @click="sendReset" :disabled="isLoading">
            {{ isLoading ? '送信中...' : 'リセットメールを送信' }}
            </button>
        </div>

        <div v-else class="success">
            <div class="success-icon">📧</div>
            <h3>メールを送信しました</h3>
            <p>{{ email }} にパスワードリセット用のリンクを送信しました。メールをご確認ください。</p>
        </div>

        <div class="back-link">
            <a @click="router.push('/login')">← ログイン画面に戻る</a>
        </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authApi } from '../api.js'

const router = useRouter()
const email = ref('')
const isLoading = ref(false)
const errorMessage = ref('')
const sent = ref(false)

const sendReset = async () => {
    errorMessage.value = ''
    if (!email.value) {
        errorMessage.value = 'メールアドレスを入力してください'
        return
    }
    isLoading.value = true
    try {
        await authApi.post('/accounts/password-reset/', { email: email.value })
        sent.value = true
    } catch (error) {
        errorMessage.value = '送信に失敗しました。もう一度お試しください'
    } finally {
        isLoading.value = false
    }
}
</script>

<style scoped>
.container {
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

.description {
    font-size: 13px;
    color: #64748b;
    margin-bottom: 20px;
    line-height: 1.6;
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

.btn-primary {
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

.btn-primary:disabled {
    opacity: 0.6;
    cursor: not-allowed;
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

.success {
    text-align: center;
    padding: 20px 0;
}

.success-icon {
    font-size: 48px;
    margin-bottom: 16px;
}

.success h3 {
    font-size: 18px;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 8px;
}

.success p {
    font-size: 13px;
    color: #64748b;
    line-height: 1.6;
}

.back-link {
    text-align: center;
    margin-top: 20px;
    font-size: 13px;
}

.back-link a {
    color: #2563eb;
    font-weight: 600;
    cursor: pointer;
}
</style>