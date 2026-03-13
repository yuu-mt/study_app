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
  background: #ffffff;
  min-height: 100vh;
  padding-bottom: 80px;
}

.header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  background: #2563eb;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header h1 {
  font-size: 18px;
  font-weight: 700;
  color: white;
  margin: 0;
}

.btn-back {
  background: rgba(255,255,255,0.2);
  border: none;
  border-radius: 8px;
  padding: 6px 12px;
  color: white;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

.summary-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  padding: 20px 16px 0;
}

.card {
  background: #f8faff;
  border-radius: 12px;
  padding: 14px 10px;
  text-align: center;
  border: 1px solid #e2eaff;
}

.card-label {
  font-size: 10px;
  color: #64748b;
  margin-bottom: 6px;
  font-weight: 500;
}

.card-value {
  font-size: 18px;
  font-weight: 700;
  color: #2563eb;
}

.tabs {
  display: flex;
  gap: 8px;
  padding: 16px 16px 0;
  overflow-x: auto;
}

.tab-btn {
  padding: 8px 18px;
  border-radius: 20px;
  border: 1.5px solid #e2e8f0;
  background: #f8faff;
  color: #64748b;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s;
}

.tab-btn.active {
  background: #2563eb;
  border-color: #2563eb;
  color: white;
}

.record-card {
  background: white;
  border-radius: 12px;
  padding: 16px;
  margin: 12px 16px 0;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}

.record-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 6px;
}

.record-category {
  font-size: 11px;
  color: #2563eb;
  font-weight: 700;
  background: #eff6ff;
  padding: 2px 8px;
  border-radius: 10px;
}

.record-date {
  font-size: 11px;
  color: #94a3b8;
}

.record-title {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 4px;
}

.record-desc {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 8px;
}

.record-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
}

.record-duration {
  font-size: 12px;
  color: #64748b;
}

.stamp-btn {
  background: none;
  border: 1.5px solid #e2e8f0;
  border-radius: 20px;
  padding: 4px 10px;
  font-size: 12px;
  cursor: pointer;
  color: #64748b;
  transition: all 0.2s;
}

.stamp-btn.stamped {
  background: #eff6ff;
  border-color: #bfdbfe;
  color: #2563eb;
}

.empty {
  text-align: center;
  color: #94a3b8;
  padding: 40px 0;
  font-size: 14px;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  padding: 20px 0;
}

.page-btn {
  padding: 8px 16px;
  border-radius: 20px;
  border: 1.5px solid #2563eb;
  background: white;
  color: #2563eb;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

.page-btn:disabled {
  border-color: #e2e8f0;
  color: #94a3b8;
  cursor: not-allowed;
}

.page-info {
  font-size: 13px;
  color: #64748b;
  font-weight: 600;
}
</style>