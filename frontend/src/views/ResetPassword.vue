<template>
    <div class="container">
        <div class="logo">
        <h1>📚 StudyTracker</h1>
        <p>新しいパスワードを設定</p>
        </div>

        <div class="card">
        <div v-if="!completed">
            <div class="form-group">
            <label>新しいパスワード（8文字以上）</label>
            <input v-model="password" type="password" placeholder="新しいパスワード" />
            </div>
            <div class="form-group">
            <label>パスワード確認</label>
            <input v-model="confirmPassword" type="password" placeholder="パスワードを再入力" />
            </div>
            <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
            <button class="btn-primary" @click="resetPassword" :disabled="isLoading">
            {{ isLoading ? '変更中...' : 'パスワードを変更' }}
            </button>
        </div>

        <div v-else class="success">
            <div class="success-icon">✅</div>
            <h3>パスワードを変更しました</h3>
            <p>新しいパスワードでログインしてください。</p>
            <button class="btn-primary" style="margin-top: 20px" @click="router.push('/login')">
            ログイン画面へ
            </button>
        </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { authApi } from '../api.js'

const router = useRouter()
const route = useRoute()

const token = ref('')
const password = ref('')
const confirmPassword = ref('')
const isLoading = ref(false)
const errorMessage = ref('')
const completed = ref(false)

onMounted(() => {
    token.value = route.query.token
    if (!token.value) {
        router.push('/login')
    }
})

const resetPassword = async () => {
    errorMessage.value = ''
    if (password.value.length < 8) {
        errorMessage.value = 'パスワードは8文字以上で入力してください'
        return
    }
    if (password.value !== confirmPassword.value) {
        errorMessage.value = 'パスワードが一致しません'
        return
    }
    isLoading.value = true
    try {
        await authApi.post('/accounts/password-reset/confirm/', {
        token: token.value,
        password: password.value
        })
        completed.value = true
    } catch (error) {
        errorMessage.value = error.response?.data?.error || 'パスワードのリセットに失敗しました'
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
}
</style>