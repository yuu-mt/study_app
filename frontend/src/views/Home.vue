<template>
  <div class="home-container">
    <!-- ヘッダー -->
    <div class="header">
      <h1>📚 StudyTracker</h1>
      <button class="btn-logout" @click="logout">ログアウト</button>
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

    <!-- カテゴリータブ -->
    <div class="tabs">
      <button
        v-for="tab in tabs"
        :key="tab.value"
        :class="['tab', activeTab === tab.value ? 'active' : '']"
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
        <div v-if="record.description" class="record-desc">{{ record.description }}</div>
        <div class="record-footer">
          <span class="record-duration">⏱ {{ record.duration_display }}</span>
          <span class="record-stamp">👍 {{ record.stamp_count }}</span>
        </div>
      </div>
    </div>

    <!-- 新規登録ボタン -->
    <button class="btn-add" @click="showModal = true">＋</button>

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

        <div class="modal-buttons">
          <button class="btn-cancel" @click="showModal = false">キャンセル</button>
          <button class="btn-primary" @click="createRecord" :disabled="isSubmitting">
            {{ isSubmitting ? '保存中...' : '保存する' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import WeeklyChart from '../components/WeeklyChart.vue'

const router = useRouter()

const summary = ref({ weekly_minutes: 0, monthly_minutes: 0, streak_days: 0 })
const weeklyData = ref([])
const records = ref([])
const categories = ref([])
const activeTab = ref('')
const showModal = ref(false)
const isSubmitting = ref(false)
const modalError = ref('')

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

const authHeader = () => ({
  Authorization: `Bearer ${localStorage.getItem('access_token')}`
})

const formatMinutes = (minutes) => {
  const h = Math.floor(minutes / 60)
  const m = minutes % 60
  if (h > 0) return m > 0 ? `${h}時間${m}分` : `${h}時間`
  return `${m}分`
}

const fetchRecords = async () => {
  try {
    const params = activeTab.value ? { category: activeTab.value } : {}
    const res = await axios.get('http://127.0.0.1:8000/api/study/records/', {
      headers: authHeader(),
      params
    })
    records.value = res.data
  } catch (error) {
    if (error.response?.status === 401) router.push('/login')
  }
}

const fetchSummary = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/study/summary/', {
      headers: authHeader()
    })
    summary.value = res.data
  } catch (error) {
    if (error.response?.status === 401) router.push('/login')
  }
}

const fetchWeeklyChart = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/study/weekly-chart/', {
      headers: authHeader()
    })
    console.log('週間データ:', res.data)
    weeklyData.value = res.data
  } catch (error) {
    console.error(error)
  }
}

const fetchCategories = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/study/categories/', {
      headers: authHeader()
    })
    categories.value = res.data
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
    const response = await axios.post('http://127.0.0.1:8000/api/study/records/', {
      category: newRecord.value.category,
      title: newRecord.value.title,
      description: newRecord.value.description,
      study_date: newRecord.value.study_date,
      duration_minutes: duration,
    }, { headers: authHeader() })

    console.log('APIレスポンス:', response.data)

    showModal.value = false
    newRecord.value = {
      category: '', title: '', description: '',
      study_date: today, hours: 1, minutes: 0
    }
    fetchRecords()
    fetchSummary()
  } catch (error) {
    modalError.value = '保存に失敗しました'
  } finally {
    isSubmitting.value = false
  }
}

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  router.push('/login')
}

onMounted(() => {
  fetchRecords()
  fetchSummary()
  fetchCategories()
  fetchWeeklyChart()
})
</script>

<style scoped>
.home-container {
  max-width: 480px;
  margin: 0 auto;
  padding: 16px;
  padding-bottom: 80px;
  background: #f5f7fa;
  min-height: 100vh;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.header h1 {
  font-size: 20px;
  font-weight: 700;
  color: #1a1a2e;
  margin: 0;
}

.btn-logout {
  background: none;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 6px 12px;
  font-size: 13px;
  color: #888;
  cursor: pointer;
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
  padding: 12px 8px;
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

.tab {
  padding: 6px 16px;
  border-radius: 20px;
  border: 1px solid #ddd;
  background: white;
  font-size: 13px;
  cursor: pointer;
  white-space: nowrap;
  color: #666;
}

.tab.active {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

.records {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.empty {
  text-align: center;
  color: #aaa;
  padding: 40px 0;
  font-size: 14px;
}

.record-card {
  background: white;
  border-radius: 12px;
  padding: 14px 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.record-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.category-badge {
  font-size: 11px;
  padding: 3px 10px;
  border-radius: 10px;
  font-weight: 600;
}

.category-badge.tech { background: #e0e7ff; color: #4338ca; }
.category-badge.culture { background: #d1fae5; color: #065f46; }
.category-badge.license { background: #fef3c7; color: #92400e; }

.record-date { font-size: 12px; color: #aaa; }

.record-title {
  font-size: 15px;
  font-weight: 600;
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
  gap: 12px;
  font-size: 12px;
  color: #888;
}

.btn-add {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-size: 28px;
  border: none;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(102,126,234,0.5);
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: flex-end;
  justify-content: center;
  z-index: 100;
}

.modal {
  background: white;
  border-radius: 20px 20px 0 0;
  padding: 24px 20px;
  width: 100%;
  max-width: 480px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal h2 {
  font-size: 18px;
  font-weight: 700;
  margin: 0 0 20px 0;
  color: #1a1a2e;
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

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 10px 14px;
  border: 2px solid #e8e8e8;
  border-radius: 10px;
  font-size: 15px;
  outline: none;
  box-sizing: border-box;
}

.form-group textarea {
  height: 80px;
  resize: none;
}

.duration-picker {
  display: flex;
  gap: 8px;
}

.duration-picker select {
  flex: 1;
}

.modal-buttons {
  display: flex;
  gap: 10px;
  margin-top: 16px;
}

.btn-cancel {
  flex: 1;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background: white;
  font-size: 15px;
  cursor: pointer;
  color: #666;
}

.btn-primary {
  flex: 1;
  padding: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
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