<template>
    <div class="settings-container">
        <!-- ヘッダー -->
        <div class="header">
            <button class="btn-back" @click="router.push('/home')">← 戻る</button>
            <h1>⚙️ 設定</h1>
        </div>

        <!-- プロフィール設定 -->
        <div class="section">
            <h3>プロフィール</h3>

            <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
            <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

            <div class="form-group">
                <label>ユーザー名</label>
                <input v-model="username" type="text" placeholder="ユーザー名" />
            </div>

            <div class="form-group">
                <label>メールアドレス</label>
                <input v-model="email" type="email" placeholder="メールアドレス" />
            </div>

            <button class="btn-primary" @click="updateProfile" :disabled="isLoading">
                {{ isLoading ? '保存中...' : 'プロフィールを保存' }}
            </button>
        </div>

        <!-- パスワード変更 -->
        <div class="section">
            <h3>パスワード変更</h3>

            <div v-if="pwSuccessMessage" class="success-message">{{ pwSuccessMessage }}</div>
            <div v-if="pwErrorMessage" class="error-message">{{ pwErrorMessage }}</div>

            <div class="form-group">
                <label>新しいパスワード（8文字以上）</label>
                <input v-model="newPassword" type="password" placeholder="新しいパスワード" />
            </div>

            <div class="form-group">
                <label>パスワード確認</label>
                <input v-model="confirmPassword" type="password" placeholder="パスワードを再入力" />
            </div>

            <button class="btn-primary" @click="updatePassword" :disabled="isPwLoading">
                {{ isPwLoading ? '変更中...' : 'パスワードを変更' }}
            </button>
        </div>

        <!-- ログアウト -->
        <div class="section">
            <button class="btn-logout" @click="logout">ログアウト</button>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const username = ref('')
const email = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const isLoading = ref(false)
const isPwLoading = ref(false)
const successMessage = ref('')
const errorMessage = ref('')
const pwSuccessMessage = ref('')
const pwErrorMessage = ref('')

const authHeader = () => ({
    Authorization: `Bearer ${localStorage.getItem('access_token')}`
})

const fetchProfile = async () => {
    try {
        const res = await axios.get('http://127.0.0.1:8000/api/accounts/me/', {
        headers: authHeader()
        })
        username.value = res.data.username
        email.value = res.data.email
    } catch (error) {
        if (error.response?.status === 401) router.push('/login')
    }
}

const updateProfile = async () => {
    errorMessage.value = ''
    successMessage.value = ''
    isLoading.value = true

    try {
        await axios.patch('http://127.0.0.1:8000/api/accounts/me/', {
        username: username.value,
        email: email.value,
        }, { headers: authHeader() })

        successMessage.value = 'プロフィールを更新しました'
    } catch (error) {
        errorMessage.value = '更新に失敗しました'
    } finally {
        isLoading.value = false
    }
}

const updatePassword = async () => {
    pwErrorMessage.value = ''
    pwSuccessMessage.value = ''

    if (newPassword.value.length < 8) {
        pwErrorMessage.value = 'パスワードは8文字以上で入力してください'
        return
    }
    if (newPassword.value !== confirmPassword.value) {
        pwErrorMessage.value = 'パスワードが一致しません'
        return
    }

    isPwLoading.value = true
    try {
        await axios.patch('http://127.0.0.1:8000/api/accounts/me/', {
        password: newPassword.value,
        }, { headers: authHeader() })

        pwSuccessMessage.value = 'パスワードを変更しました'
        newPassword.value = ''
        confirmPassword.value = ''
    } catch (error) {
        pwErrorMessage.value = 'パスワードの変更に失敗しました'
    } finally {
        isPwLoading.value = false
    }
}

const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    router.push('/login')
}

onMounted(() => {
    fetchProfile()
})
</script>

<style scoped>
.settings-container {
    max-width: 480px;
    margin: 0 auto;
    padding: 16px;
    background: #f5f7fa;
    min-height: 100vh;
}

.header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
}

.header h1 {
    font-size: 20px;
    font-weight: 700;
    color: #1a1a2e;
    margin: 0;
}

.btn-back {
    background: none;
    border: none;
    color: #667eea;
    font-size: 14px;
    cursor: pointer;
    padding: 0;
}

.section {
    background: white;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.section h3 {
    font-size: 14px;
    font-weight: 600;
    color: #444;
    margin: 0 0 16px 0;
}

.form-group {
    margin-bottom: 14px;
}

.form-group label {
    display: block;
    font-size: 13px;
    font-weight: 600;
    color: #444;
    margin-bottom: 6px;
}

.form-group input {
    width: 100%;
    padding: 10px 14px;
    border: 2px solid #e8e8e8;
    border-radius: 10px;
    font-size: 15px;
    outline: none;
    box-sizing: border-box;
    transition: border-color 0.2s;
}

.form-group input:focus {
    border-color: #667eea;
}

.btn-primary {
    width: 100%;
    padding: 12px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    transition: opacity 0.2s;
}

.btn-primary:disabled {
    opacity: 0.7;
    cursor: not-allowed;
}

.btn-logout {
    width: 100%;
    padding: 12px;
    background: white;
    color: #e53e3e;
    border: 1px solid #ffcccc;
    border-radius: 10px;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
}

.success-message {
    background: #f0fff4;
    border: 1px solid #9ae6b4;
    color: #276749;
    padding: 10px 14px;
    border-radius: 8px;
    font-size: 13px;
    margin-bottom: 12px;
}

.error-message {
    background: #fff0f0;
    border: 1px solid #ffcccc;
    color: #e53e3e;
    padding: 10px 14px;
    border-radius: 8px;
    font-size: 13px;
    margin-bottom: 12px;
}
</style>