<template>
    <div class="home-container">
        <!-- ヘッダー -->
        <div class="header">
            <h1>
                <span class="title-monster">Monster</span>
                <span class="title-study">Study Tracker</span>
            </h1>
            <div class="header-btns">
                <button class="btn-friends" @click="router.push('/friends')">👥</button>
                <button class="btn-friends" @click="router.push('/settings')">⚙️</button>
                <button class="btn-logout" @click="logout">ログアウト</button>
            </div>
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

        <!-- 週間グラフ -->
        <WeeklyChart :weeklyData="weeklyData" />
        <!-- モンスター -->
        <MonsterCard :totalMinutes="totalMinutes" :monsterType="monsterType" />
        <!-- カテゴリータブ -->
        <div class="tabs">
            <button
                v-for="tab in tabs"
                :key="tab.value"
                :class="['tab-btn', activeTab === tab.value ? 'active' : '']"
                @click="activeTab = tab.value; fetchRecords()"
            >
                {{ tab.label }}
            </button>
        </div>

        <!-- 学習記録一覧 -->
        <div class="records">
            <div v-if="records.length === 0" class="empty">
                まだ学習記録がありません
            </div>
            <div v-for="record in records" :key="record.id" class="record-card">
                <div class="record-header">
                    <span :class="['category-badge', record.category]">
                    {{ record.category_name }}
                    </span>
                    <span class="record-date">{{ record.study_date }}</span>
                </div>
                <div class="record-title">{{ record.title }}</div>
                <div v-if="record.description" class="record-desc">{{ record.description }}
                </div>
                <div class="record-footer">
                    <span class="record-duration">⏱ {{ record.duration_display }}</span>
                    <div class="record-actions">
                        <span class="stamp-count">👍 {{ record.stamp_count }}</span>
                        <button class="btn-edit" @click="openEditModal(record)">✏️</button>
                        <button class="btn-delete" @click="deleteRecord(record)">🗑️</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- ページネーション -->
        <div v-if="totalCount > 0" class="pagination">
        <button
            class="page-btn"
            :disabled="currentPage === 1"
            @click="changePage(currentPage - 1)"
        >
            ← 前へ
        </button>
        <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
        <button
            class="page-btn"
            :disabled="currentPage === totalPages"
            @click="changePage(currentPage + 1)"
        >
            次へ →
        </button>
        </div>

        <!-- 新規登録ボタン -->
        <button class="btn-add" @click="router.push('/timer')">＋</button>

        <!-- 新規登録モーダル -->
        <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
            <div class="modal">
                <h2>学習記録を追加</h2>

                <div class="form-group">
                    <label>カテゴリー</label>
                    <select v-model="newRecord.category">
                        <option value="">選択してください</option>
                        <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                        {{ cat.get_name_display }}
                        </option>
                    </select>
                </div>

                <div class="form-group">
                    <label>学習タイトル</label>
                    <input v-model="newRecord.title" type="text" placeholder="例：Python基礎勉強" />
                </div>

                <div class="form-group">
                    <label>学習内容（任意）</label>
                    <textarea v-model="newRecord.description" placeholder="学習した内容を記録..."></textarea>
                </div>

                <div class="form-group">
                    <label>学習日</label>
                    <input v-model="newRecord.study_date" type="date" />
                </div>

                <div class="form-group">
                    <label>学習時間</label>
                    <div class="duration-picker">
                        <select v-model="newRecord.hours">
                            <option v-for="h in 24" :key="h-1" :value="h-1">{{ h-1 }}時間</option>
                        </select>
                        <select v-model="newRecord.minutes">
                            <option v-for="m in [0,10,15,20,30,45]" :key="m" :value="m">{{ m }}分</option>
                        </select>
                    </div>
                </div>

                <div v-if="modalError" class="error-message">{{ modalError }}</div>

                <div class="modal-actions">
                    <button class="btn-cancel" @click="showModal = false">キャンセル</button>
                    <button class="btn-submit" @click="createRecord" :disabled="isSubmitting">
                        {{ isSubmitting ? '保存中...' : '保存する' }}
                    </button>
                </div>
            </div>
        </div>

        <!-- 編集モーダル -->
        <div v-if="showEditModal" class="modal-overlay" @click.self="showEditModal = false">
            <div class="modal">
                <h2>学習記録を編集</h2>

                <div class="form-group">
                    <label>カテゴリー</label>
                    <select v-model="editRecord.category">
                        <option value="">選択してください</option>
                        <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                        {{ cat.get_name_display }}
                        </option>
                    </select>
                </div>

                <div class="form-group">
                    <label>学習タイトル</label>
                    <input v-model="editRecord.title" type="text" />
                </div>

                <div class="form-group">
                    <label>学習内容（任意）</label>
                    <textarea v-model="editRecord.description"></textarea>
                </div>

                <div class="form-group">
                    <label>学習日</label>
                    <input v-model="editRecord.study_date" type="date" />
                </div>

                <div class="form-group">
                    <label>学習時間</label>
                    <div class="time-inputs">
                        <select v-model="editRecord.hours">
                            <option v-for="h in 24" :key="h-1" :value="h-1">{{ h-1 }}時間</option>
                        </select>
                        <select v-model="editRecord.minutes">
                            <option v-for="m in [0,10,15,20,30,45]" :key="m" :value="m">{{ m }}分</option>
                        </select>
                    </div>
                </div>

                <div v-if="editError" class="error-message">{{ editError }}</div>

                <div class="modal-actions">
                    <button class="btn-cancel" @click="showEditModal = false">キャンセル</button>
                    <button class="btn-submit" @click="updateRecord" :disabled="isSubmitting">
                        {{ isSubmitting ? '保存中...' : '保存する' }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import api from '../api.js'
import WeeklyChart from '../components/WeeklyChart.vue'
import MonsterCard from '../components/MonsterCard.vue'
import { ref, onMounted, computed } from 'vue'


const router = useRouter()

const summary = ref({ weekly_minutes: 0, monthly_minutes: 0, streak_days: 0 })
const weeklyData = ref([])
const records = ref([])
const categories = ref([])
const activeTab = ref('')
const showModal = ref(false)
const isSubmitting = ref(false)
const modalError = ref('')
const currentPage = ref(1)
const totalCount = ref(0)
const totalPages = computed(() => Math.ceil(totalCount.value / 10))
const monsterType = ref(localStorage.getItem('monster_type') || 'slime')

const tabs = [
    { label: 'すべて', value: '' },
    { label: '技術', value: 'tech' },
    { label: '教養', value: 'culture' },
    { label: '資格', value: 'license' },
]

const today = new Date().toISOString().split('T')[0]

const newRecord = ref({
    category: '',
    title: '',
    description: '',
    study_date: today,
    hours: 1,
    minutes: 0,
})

const showEditModal = ref(false)
const editError = ref('')
const editRecord = ref({
    id: null,
    category: '',
    title: '',
    description: '',
    study_date: '',
    hours: 1,
    minutes: 0,
})

const formatMinutes = (minutes) => {
    const h = Math.floor(minutes / 60)
    const m = minutes % 60
    if (h > 0) return m > 0 ? `${h}時間${m}分` : `${h}時間`
    return `${m}分`
}

const fetchRecords = async (page = 1) => {
    try {
        const params = { page }
        if (activeTab.value) params.category = activeTab.value
        const res = await api.get('/study/records/', { params })
        records.value = res.data.results
        totalCount.value = res.data.count
        currentPage.value = page
    } catch (error) {
        if (error.response?.status === 401) router.push('/login')
    }
}

const changePage = (page) => {
    fetchRecords(page)
    window.scrollTo(0, 0)
}

const fetchSummary = async () => {
    try {
        const res = await api.get('/study/summary/')
        summary.value = res.data
        } catch (error) {
            if (error.response?.status === 401) router.push('/login')
        }
}

const fetchWeeklyChart = async () => {
    try {
        const res = await api.get('/study/weekly-chart/')
        console.log('週間データ:', res.data)
        weeklyData.value = res.data
        } catch (error) {
            console.error(error)
        }
}

const fetchCategories = async () => {
    try {
        const res = await api.get('/study/categories/')
        categories.value = res.data.results
    } catch (error) {
        console.error(error)
    }
}

const createRecord = async () => {
    modalError.value = ''

    if (!newRecord.value.category) {
        modalError.value = 'カテゴリーを選択してください'
        return
    }
    if (!newRecord.value.title) {
        modalError.value = 'タイトルを入力してください'
        return
    }

    const duration = Number(newRecord.value.hours) * 60 + Number(newRecord.value.minutes)
    if (duration === 0) {
        modalError.value = '学習時間を入力してください'
        return
    }

    isSubmitting.value = true
    try {
        await api.post('/study/records/', {
        category: Number(newRecord.value.category),
        title: newRecord.value.title,
        description: newRecord.value.description,
        study_date: newRecord.value.study_date,
        duration_minutes: duration,
        })

        showModal.value = false
        newRecord.value = {
        category: '', title: '', description: '',
        study_date: today, hours: 1, minutes: 0
        }
        fetchRecords(1)
        fetchSummary()
        fetchWeeklyChart()
        fetchTotalSummary()
    } catch (error) {
        console.error('保存エラー:', error.response?.data)
        modalError.value = '保存に失敗しました'
    } finally {
        isSubmitting.value = false
    }
}

const toggleStamp = async (record) => {
    try {
        await api.post(`/study/records/${record.id}/stamp/`, { stamp_type: 'good' })
        fetchRecords()
    } catch (error) {
        console.error(error)
    }
}

const logout = () => {
localStorage.removeItem('access_token')
localStorage.removeItem('refresh_token')
router.push('/login')
}

const openEditModal = (record) => {
    editRecord.value = {
        id: record.id,
        category: record.category,
        title: record.title,
        description: record.description,
        study_date: record.study_date,
        hours: Math.floor(record.duration_minutes / 60),
        minutes: record.duration_minutes % 60,
    }
    showEditModal.value = true
}

const updateRecord = async () => {
    editError.value = ''
    const duration = Number(editRecord.value.hours) * 60 + Number(editRecord.value.minutes)
    if (!editRecord.value.title) {
        editError.value = 'タイトルを入力してください'
        return
    }
    isSubmitting.value = true
    try {
        await api.patch(`/study/records/${editRecord.value.id}/`, {
        category: Number(editRecord.value.category),
        title: editRecord.value.title,
        description: editRecord.value.description,
        study_date: editRecord.value.study_date,
        duration_minutes: duration,
        })
        showEditModal.value = false
        fetchRecords(currentPage.value)
        fetchSummary()
        fetchWeeklyChart()
    } catch (error) {
        editError.value = '更新に失敗しました'
    } finally {
        isSubmitting.value = false
    }
}

const deleteRecord = async (record) => {
    if (!confirm(`「${record.title}」を削除しますか？`)) return
    try {
        await api.delete(`/study/records/${record.id}/`)
        fetchRecords(currentPage.value)
        fetchSummary()
        fetchWeeklyChart()
    } catch (error) {
        console.error(error)
    }
}

const totalMinutes = ref(0)

const fetchTotalSummary = async () => {
    try {
        const res = await api.get('/study/total-summary/')
        totalMinutes.value = res.data.total_minutes
    } catch (error) {
        console.error(error)
    }
}



onMounted(() => {
fetchRecords()
fetchSummary()
fetchCategories()
fetchWeeklyChart()
fetchTotalSummary()
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
    justify-content: space-between;
    align-items: center;
    padding: 16px 20px;
    background: #2563eb;
    color: white;
    position: sticky;
    top: 0;
    z-index: 100;
}

.header h1 {
    font-size: 18px;
    font-weight: 700;
    color: white;
    margin: 0;
    display: flex;
    flex-direction: column;
    line-height: 1.2;
}

.title-study {
    font-size: 11px;
    font-weight: 600;
    color: #bfdbfe;
    letter-spacing: 3px;
    text-transform: uppercase;
}

.title-monster {
    font-family: Georgia, serif;
    font-size: 20px;
    font-weight: 700;
    color: #fca5a5;
    letter-spacing: 1px;
}

.header-btns {
    display: flex;
    gap: 8px;
    align-items: center;
}

.btn-friends {
    background: rgba(255,255,255,0.2);
    border: none;
    border-radius: 8px;
    padding: 6px 10px;
    font-size: 16px;
    cursor: pointer;
    color: white;
}

.btn-logout {
    background: rgba(255,255,255,0.2);
    border: none;
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    color: white;
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
    background: white;
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

.stamp-count {
    font-size: 12px;
    color: #64748b;
    padding: 4px 10px;
    border-radius: 20px;
    background: #f1f5f9;
}

.empty {
    text-align: center;
    color: #94a3b8;
    padding: 40px 0;
    font-size: 14px;
}

.btn-add {
    position: fixed;
    bottom: 24px;
    right: 24px;
    width: 52px;
    height: 52px;
    border-radius: 50%;
    background: #2563eb;
    color: white;
    border: none;
    font-size: 24px;
    cursor: pointer;
    box-shadow: 0 4px 16px rgba(37, 99, 235, 0.4);
    display: flex;
    align-items: center;
    justify-content: center;
}

.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 200;
    padding: 16px;
}

.modal {
    background: white;
    border-radius: 16px;
    padding: 24px;
    width: 100%;
    max-width: 400px;
    max-height: 90vh;
    overflow-y: auto;
}

.modal h2 {
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 20px;
    color: #1e293b;
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
    padding: 10px 14px;
    border: 1.5px solid #e2e8f0;
    border-radius: 10px;
    font-size: 15px;
    outline: none;
    box-sizing: border-box;
    transition: border-color 0.2s;
    background: white;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
    border-color: #2563eb;
}

.time-inputs {
    display: flex;
    gap: 10px;
}

.time-inputs input {
    flex: 1;
}

.error-message {
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #dc2626;
    padding: 10px 14px;
    border-radius: 8px;
    font-size: 13px;
    margin-bottom: 12px;
}

.modal-actions {
    display: flex;
    gap: 10px;
    margin-top: 20px;
}

.btn-cancel {
    flex: 1;
    padding: 12px;
    border-radius: 10px;
    border: 1.5px solid #e2e8f0;
    background: white;
    color: #64748b;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
}

.btn-submit {
    flex: 2;
    padding: 12px;
    border-radius: 10px;
    border: none;
    background: #2563eb;
    color: white;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
}

.btn-submit:disabled {
    opacity: 0.6;
    cursor: not-allowed;
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

.record-actions {
    display: flex;
    align-items: center;
    gap: 8px;
}

.btn-edit {
    background: none;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 4px 8px;
    font-size: 12px;
    cursor: pointer;
}

.btn-delete {
    background: none;
    border: 1px solid #fecaca;
    border-radius: 8px;
    padding: 4px 8px;
    font-size: 12px;
    cursor: pointer;
}
</style>