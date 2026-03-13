<template>
    <div class="home-container">
        <!-- ヘッダー -->
        <div class="header">
            <button class="btn-back" @click="router.push('/friends')">← 戻る</button>
            <h1>📚 {{ friendName }}の記録</h1>
        </div>

        <!-- 集計カード -->
        <div class="summary-cards">
            <div class="card">
                <div class="card-label">今週の学習時間</div>
                <div class="card-value">{{ formatMinutes(summary.weekly_minutes) }}</div>
            </div>
            <div class="card">
                <div class="card-label">今月の学習時間</div>
                <div class="card-value">{{ formatMinutes(summary.monthly_minutes) }}</div>
            </div>
            <div class="card">
                <div class="card-label">連続学習日数</div>
                <div class="card-value">{{ summary.streak_days }}日🔥</div>
            </div>
        </div>

        <!-- カテゴリータブ -->
        <div class="tabs">
            <button
                v-for="tab in tabs"
                :key="tab.value"
                :class="['tab-btn', activeTab === tab.value ? 'active' : '']"
                @click="activeTab = tab.value; fetchRecords(1)"
            >
                {{ tab.label }}
            </button>
        </div>

        <!-- 学習記録一覧 -->
        <div v-if="records.length === 0" class="empty">
        まだ学習記録がありません
        </div>
        <div v-for="record in records" :key="record.id" class="record-card">
            <div class="record-header">
                <span class="record-category">{{ record.category_name }}</span>
                <span class="record-date">{{ record.study_date }}</span>
            </div>
            <div class="record-title">{{ record.title }}</div>
            <div v-if="record.description" class="record-desc">{{ record.description }}</div>
            <div class="record-footer">
                <span class="record-duration">⏱ {{ record.duration_display }}</span>
                <button
                :class="['stamp-btn', record.my_stamp ? 'stamped' : '']"
                @click="toggleStamp(record)"
                >
                👍 {{ record.stamp_count }}
                </button>
            </div>
        </div>

        <!-- ページネーション -->
        <div v-if="totalCount > 0" class="pagination">
        <button
            class="page-btn"
            :disabled="currentPage === 1"
            @click="fetchRecords(currentPage - 1)"
        >
            ← 前へ
        </button>
        <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
        <button
            class="page-btn"
            :disabled="currentPage === totalPages"
            @click="fetchRecords(currentPage + 1)"
        >
            次へ →
        </button>
        </div>
    </div>
</template>
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '../api.js'

const router = useRouter()
const route = useRoute()

const friendId = route.params.id
const friendName = ref('')
const records = ref([])
const summary = ref({ weekly_minutes: 0, monthly_minutes: 0, streak_days: 0 })
const activeTab = ref('')
const currentPage = ref(1)
const totalCount = ref(0)
const totalPages = computed(() => Math.ceil(totalCount.value / 10))

const tabs = [
    { label: 'すべて', value: '' },
    { label: '技術', value: 'tech' },
    { label: '教養', value: 'culture' },
    { label: '資格', value: 'license' },
]

const formatMinutes = (minutes) => {
    const h = Math.floor(minutes / 60)
    const m = minutes % 60
    if (h > 0) return m > 0 ? `${h}時間${m}分` : `${h}時間`
    return `${m}分`
}

const fetchFriendInfo = async () => {
    try {
        const res = await api.get('/accounts/friends/')
        const friend = res.data.results.find(f => f.id === Number(friendId))
        if (friend) friendName.value = friend.username
    } catch (error) {
        console.error(error)
    }
}

const fetchRecords = async (page = 1) => {
    try {
        const params = { page }
        if (activeTab.value) params.category = activeTab.value
        console.log('friendId:', friendId)
        console.log('URL:', `/study/friends/${friendId}/records/`)
        const res = await api.get(`/study/friends/${friendId}/records/`, { params })
        console.log('records:', res.data)
        records.value = res.data.results
        totalCount.value = res.data.count
        currentPage.value = page
    } catch (error) {
        if (error.response?.status === 401) router.push('/login')
    }
}

const fetchSummary = async () => {
    try {
        const res = await api.get(`/study/friends/${friendId}/summary/`)
        summary.value = res.data
    } catch (error) {
        console.error(error)
    }
}

const toggleStamp = async (record) => {
    try {
        await api.post(`/study/records/${record.id}/stamp/`, { stamp_type: 'good' })
        fetchRecords(currentPage.value)
    } catch (error) {
        console.error(error)
    }
}

onMounted(() => {
    fetchFriendInfo()
    fetchRecords()
    fetchSummary()
})
</script>

<style scoped>
.home-container {
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
    font-size: 18px;
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
    white-space: nowrap;
}

.summary-cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-bottom: 16px;
}

.card {
    background: white;
    border-radius: 12px;
    padding: 12px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.card-label {
    font-size: 10px;
    color: #888;
    margin-bottom: 4px;
}

.card-value {
    font-size: 16px;
    font-weight: 700;
    color: #667eea;
}

.tabs {
    display: flex;
    gap: 8px;
    margin-bottom: 16px;
    overflow-x: auto;
}

.tab-btn {
    padding: 8px 16px;
    border-radius: 20px;
    border: 1px solid #ddd;
    background: white;
    color: #888;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    white-space: nowrap;
}

.tab-btn.active {
    background: #667eea;
    border-color: #667eea;
    color: white;
}

.record-card {
    display: block;
    background: white;
    border-radius: 12px;
    padding: 14px;
    margin-bottom: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.record-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 6px;
}

.record-category {
    font-size: 11px;
    color: #888;
    font-weight: 600;
}

.record-date {
    font-size: 11px;
    color: #aaa;
}

.record-title {
    font-size: 16px;
    font-weight: 700;
    color: #1a1a2e;
    margin-bottom: 4px;
}

.record-desc {
    font-size: 13px;
    color: #666;
    margin-bottom: 8px;
}

.record-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.record-duration {
    font-size: 12px;
    color: #888;
}

.stamp-btn {
    background: none;
    border: 1px solid #ddd;
    border-radius: 20px;
    padding: 4px 10px;
    font-size: 12px;
    cursor: pointer;
    color: #888;
    transition: all 0.2s;
}

.stamp-btn.stamped {
    background: #fff0f0;
    border-color: #ffcccc;
    color: #e53e3e;
}

.empty {
    text-align: center;
    color: #aaa;
    padding: 40px 0;
    font-size: 14px;
}

.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 16px;
    padding: 16px 0;
}

.page-btn {
    padding: 8px 16px;
    border-radius: 20px;
    border: 1px solid #667eea;
    background: white;
    color: #667eea;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
}

.page-btn:disabled {
    border-color: #ddd;
    color: #aaa;
    cursor: not-allowed;
}

.page-info {
    font-size: 13px;
    color: #888;
    font-weight: 600;
}
</style>