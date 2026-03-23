<template>
    <div class="timer-container">
        <!-- ヘッダー -->
        <div class="header">
        <h1>📚 学習タイマー</h1>
        </div>

        <!-- 入力フォーム（タイマー停止中のみ表示） -->
        <div v-if="!isStarted" class="form-section">
        <div class="form-group">
            <label>カテゴリー</label>
            <select v-model="form.category">
            <option value="">選択してください</option>
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                {{ cat.get_name_display }}
            </option>
            </select>
        </div>

        <div class="form-group">
            <label>学習タイトル</label>
            <input v-model="form.title" type="text" placeholder="例：Python基礎勉強" />
        </div>

        <div class="form-group">
            <label>学習内容（任意）</label>
            <textarea v-model="form.description" placeholder="学習した内容を記録..."></textarea>
        </div>

        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

        <button class="btn-start" @click="startTimer">
            ▶ スタート
        </button>
        </div>

        <!-- タイマー表示（タイマー起動中） -->
        <div v-else class="timer-section">
        <div class="study-info">
            <div class="study-category">{{ categoryName }}</div>
            <div class="study-title">{{ form.title }}</div>
            <div v-if="form.description" class="study-desc">{{ form.description }}</div>
        </div>

        <!-- タイマー -->
        <div class="timer-display" :class="isPaused ? 'paused' : 'running'">
            <div class="time-text">{{ formattedTime }}</div>
            <div class="status-text">{{ isPaused ? '一時停止中' : '学習中...' }}</div>
        </div>

        <!-- ボタン -->
        <div class="timer-buttons">
            <button class="btn-pause" @click="togglePause">
            {{ isPaused ? '▶ 再開' : '⏸ 一時停止' }}
            </button>
            <button class="btn-complete" @click="completeTimer" :disabled="totalSeconds < 60">
            ✓ 完了
            </button>
        </div>

        <div v-if="totalSeconds < 60" class="min-time-note">
            ※ 1分以上で完了できます
        </div>

        <button class="btn-cancel" @click="cancelTimer">
            キャンセル
        </button>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api.js'

const router = useRouter()

const categories = ref([])
const form = ref({
    category: '',
    title: '',
    description: '',
})
const errorMessage = ref('')
const isStarted = ref(false)
const isPaused = ref(false)
const totalSeconds = ref(0)
let timerInterval = null

const fetchCategories = async () => {
    try {
        const res = await api.get('/study/categories/')
        categories.value = res.data.results
    } catch (error) {
        console.error(error)
    }
}

const categoryName = computed(() => {
    const cat = categories.value.find(c => c.id === form.value.category)
    return cat ? cat.get_name_display : ''
})

const formattedTime = computed(() => {
    const h = Math.floor(totalSeconds.value / 3600)
    const m = Math.floor((totalSeconds.value % 3600) / 60)
    const s = totalSeconds.value % 60
    if (h > 0) {
    return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
    }
    return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
})

const startTimer = () => {
    errorMessage.value = ''
    if (!form.value.category) {
        errorMessage.value = 'カテゴリーを選択してください'
        return
    }
    if (!form.value.title) {
        errorMessage.value = 'タイトルを入力してください'
        return
    }
    isStarted.value = true
    isPaused.value = false
    timerInterval = setInterval(() => {
        if (!isPaused.value) {
        totalSeconds.value++
        }
    }, 1000)
}

const togglePause = () => {
    isPaused.value = !isPaused.value
}

const completeTimer = async () => {
    if (totalSeconds.value < 60) return
    clearInterval(timerInterval)

    const durationMinutes = Math.floor(totalSeconds.value / 60)
    const today = new Date().toISOString().split('T')[0]

    try {
        await api.post('/study/records/', {
        category: Number(form.value.category),
        title: form.value.title,
        description: form.value.description,
        study_date: today,
        duration_minutes: durationMinutes,
        })
        router.push('/home')
    } catch (error) {
        console.error(error)
    }
}

const cancelTimer = () => {
    if (!confirm('タイマーをキャンセルしますか？記録は保存されません。')) return
    clearInterval(timerInterval)
    isStarted.value = false
    isPaused.value = false
    totalSeconds.value = 0
}

onUnmounted(() => {
    clearInterval(timerInterval)
})

fetchCategories()
</script>

<style scoped>
.timer-container {
    max-width: 480px;
    margin: 0 auto;
    padding: 0 0 80px;
    background: #f8faff;
    min-height: 100vh;
}

.header {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 16px 20px;
    background: #2563eb;
}

.header h1 {
    font-size: 18px;
    font-weight: 700;
    color: white;
    margin: 0;
}

.form-section {
    padding: 20px 16px;
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

.form-group input,
.form-group select,
.form-group textarea {
    width: 100%;
    padding: 12px 14px;
    border: 1.5px solid #e2e8f0;
    border-radius: 10px;
    font-size: 16px;
    outline: none;
    box-sizing: border-box;
    background: white;
    transition: border-color 0.2s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
    border-color: #2563eb;
}

.form-group textarea {
    height: 80px;
    resize: none;
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

.btn-start {
    width: 100%;
    padding: 16px;
    background: #2563eb;
    color: white;
    border: none;
    border-radius: 12px;
    font-size: 18px;
    font-weight: 700;
    cursor: pointer;
    margin-top: 8px;
}

.timer-section {
    padding: 24px 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 24px;
}

.study-info {
    background: white;
    border-radius: 12px;
    padding: 16px;
    width: 100%;
    border: 1px solid #e2e8f0;
}

.study-category {
    font-size: 11px;
    color: #2563eb;
    font-weight: 700;
    background: #eff6ff;
    padding: 2px 8px;
    border-radius: 10px;
    display: inline-block;
    margin-bottom: 6px;
}

.study-title {
    font-size: 18px;
    font-weight: 700;
    color: #1e293b;
}

.study-desc {
    font-size: 13px;
    color: #64748b;
    margin-top: 4px;
}

.timer-display {
    width: 220px;
    height: 220px;
    border-radius: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border: 6px solid #2563eb;
    transition: all 0.3s;
}

.timer-display.paused {
    border-color: #94a3b8;
    background: #f8faff;
}

.timer-display.running {
    background: #eff6ff;
    animation: pulse 2s ease-in-out infinite;
}

.time-text {
    font-size: 48px;
    font-weight: 700;
    color: #1e293b;
    font-variant-numeric: tabular-nums;
}

.status-text {
    font-size: 13px;
    color: #64748b;
    margin-top: 4px;
}

.timer-buttons {
    display: flex;
    gap: 12px;
    width: 100%;
}

.btn-pause {
    flex: 1;
    padding: 14px;
    border-radius: 12px;
    border: 2px solid #2563eb;
    background: white;
    color: #2563eb;
    font-size: 15px;
    font-weight: 700;
    cursor: pointer;
}

.btn-complete {
    flex: 1;
    padding: 14px;
    border-radius: 12px;
    border: none;
    background: #2563eb;
    color: white;
    font-size: 15px;
    font-weight: 700;
    cursor: pointer;
}

.btn-complete:disabled {
    background: #94a3b8;
    cursor: not-allowed;
}

.min-time-note {
    font-size: 12px;
    color: #94a3b8;
    margin-top: -16px;
}

.btn-cancel {
    background: none;
    border: none;
    color: #94a3b8;
    font-size: 13px;
    cursor: pointer;
    padding: 8px;
}

@keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(37, 99, 235, 0.2); }
    50% { box-shadow: 0 0 0 12px rgba(37, 99, 235, 0); }
}
</style>