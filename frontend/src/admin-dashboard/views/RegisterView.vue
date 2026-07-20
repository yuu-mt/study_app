<template>
    <div class="page">
        <div class="page-header">
            <h1>受講生・メンバー登録</h1>
            <p class="page-desc">Monster Study Trackerへアプリ登録済みのユーザーから、受講生・講師を登録します。</p>
        </div>

        <section class="card">
            <h2>受講生登録</h2>
            <p class="card-desc">登録直後のステータスは「未受講」で固定されます。</p>

            <div class="form-row">
                <div class="form-field">
                    <label>ユーザー検索</label>
                    <input v-model="traineeQuery" @input="fetchTraineeCandidates" type="text" placeholder="ユーザー名・メールアドレスで検索" />
                </div>
            </div>

            <div class="candidate-list" v-if="traineeCandidates.length > 0">
                <button
                    v-for="user in traineeCandidates"
                    :key="user.id"
                    class="candidate-item"
                    :class="{ selected: selectedTraineeUser?.id === user.id }"
                    @click="selectedTraineeUser = user"
                >
                    <span class="candidate-name">{{ user.username }}</span>
                    <span class="candidate-email">{{ user.email }}</span>
                </button>
            </div>
            <p v-else class="empty-note">該当するユーザーが見つかりません（登録済みの場合は候補に表示されません）</p>

            <div class="form-row" v-if="selectedTraineeUser">
                <div class="form-field">
                    <label>担当メンバー（任意）</label>
                    <select v-model="selectedMentorId">
                        <option value="">未設定</option>
                        <option v-for="m in mentors" :key="m.id" :value="m.id">{{ m.username }}</option>
                    </select>
                </div>
            </div>

            <div v-if="traineeError" class="error-message">{{ traineeError }}</div>
            <div v-if="traineeSuccess" class="success-message">{{ traineeSuccess }}</div>

            <button class="btn-primary" :disabled="!selectedTraineeUser || isRegisteringTrainee" @click="registerTrainee">
                {{ isRegisteringTrainee ? '登録中...' : '受講生として登録する' }}
            </button>
        </section>

        <section class="card" v-if="isAdmin">
            <h2>講師登録</h2>
            <p class="card-desc">講師（instructor）ロールの付与はadminアカウントのみ実行できます。</p>

            <div class="form-row">
                <div class="form-field">
                    <label>ユーザー検索</label>
                    <input v-model="instructorQuery" @input="fetchInstructorCandidates" type="text" placeholder="ユーザー名・メールアドレスで検索" />
                </div>
            </div>

            <div class="candidate-list" v-if="instructorCandidates.length > 0">
                <button
                    v-for="user in instructorCandidates"
                    :key="user.id"
                    class="candidate-item"
                    :class="{ selected: selectedInstructorUser?.id === user.id }"
                    @click="selectedInstructorUser = user"
                >
                    <span class="candidate-name">{{ user.username }}</span>
                    <span class="candidate-email">{{ user.email }}</span>
                </button>
            </div>
            <p v-else class="empty-note">該当するユーザーが見つかりません</p>

            <div v-if="instructorError" class="error-message">{{ instructorError }}</div>
            <div v-if="instructorSuccess" class="success-message">{{ instructorSuccess }}</div>

            <button class="btn-primary" :disabled="!selectedInstructorUser || isRegisteringInstructor" @click="registerInstructor">
                {{ isRegisteringInstructor ? '登録中...' : '講師として登録する' }}
            </button>
        </section>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../../api.js'
import { useAdminUser } from '../useAdminUser.js'

const { currentUser } = useAdminUser()
const isAdmin = computed(() => currentUser.value?.role === 'admin')

// 受講生登録
const traineeQuery = ref('')
const traineeCandidates = ref([])
const selectedTraineeUser = ref(null)
const mentors = ref([])
const selectedMentorId = ref('')
const isRegisteringTrainee = ref(false)
const traineeError = ref('')
const traineeSuccess = ref('')

let traineeDebounce = null
const fetchTraineeCandidates = () => {
    clearTimeout(traineeDebounce)
    traineeDebounce = setTimeout(async () => {
        try {
            const res = await api.get('/curriculum/trainees/candidates/', {
                params: traineeQuery.value ? { q: traineeQuery.value } : {},
            })
            traineeCandidates.value = res.data
        } catch (error) {
            console.error(error)
        }
    }, 250)
}

const fetchMentors = async () => {
    try {
        const res = await api.get('/curriculum/mentors/')
        mentors.value = res.data
    } catch (error) {
        console.error(error)
    }
}

const registerTrainee = async () => {
    if (!selectedTraineeUser.value) return
    isRegisteringTrainee.value = true
    traineeError.value = ''
    traineeSuccess.value = ''
    try {
        await api.post('/curriculum/trainees/register/', {
            user_id: selectedTraineeUser.value.id,
            mentor_id: selectedMentorId.value || null,
        })
        traineeSuccess.value = `${selectedTraineeUser.value.username} さんを受講生として登録しました`
        selectedTraineeUser.value = null
        selectedMentorId.value = ''
        traineeQuery.value = ''
        traineeCandidates.value = []
    } catch (error) {
        traineeError.value = error.response?.data?.user_id?.[0] || '登録に失敗しました'
    } finally {
        isRegisteringTrainee.value = false
    }
}

// 講師登録（adminのみ）
const instructorQuery = ref('')
const instructorCandidates = ref([])
const selectedInstructorUser = ref(null)
const isRegisteringInstructor = ref(false)
const instructorError = ref('')
const instructorSuccess = ref('')

let instructorDebounce = null
const fetchInstructorCandidates = () => {
    clearTimeout(instructorDebounce)
    instructorDebounce = setTimeout(async () => {
        try {
            const res = await api.get('/curriculum/instructors/candidates/', {
                params: instructorQuery.value ? { q: instructorQuery.value } : {},
            })
            instructorCandidates.value = res.data
        } catch (error) {
            console.error(error)
        }
    }, 250)
}

const registerInstructor = async () => {
    if (!selectedInstructorUser.value) return
    isRegisteringInstructor.value = true
    instructorError.value = ''
    instructorSuccess.value = ''
    try {
        await api.post('/curriculum/instructors/register/', {
            user_id: selectedInstructorUser.value.id,
        })
        instructorSuccess.value = `${selectedInstructorUser.value.username} さんを講師として登録しました`
        selectedInstructorUser.value = null
        instructorQuery.value = ''
        instructorCandidates.value = []
        fetchMentors()
    } catch (error) {
        instructorError.value = '登録に失敗しました'
    } finally {
        isRegisteringInstructor.value = false
    }
}

onMounted(() => {
    fetchTraineeCandidates()
    fetchMentors()
    if (isAdmin.value) fetchInstructorCandidates()
})
</script>

<style scoped>
.page-header {
    margin-bottom: 24px;
}

.page-header h1 {
    font-size: 22px;
    font-weight: 800;
    color: #0f172a;
    margin: 0 0 6px;
}

.page-desc {
    font-size: 13px;
    color: #64748b;
    margin: 0;
}

.card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 20px;
    max-width: 560px;
}

.card h2 {
    font-size: 16px;
    font-weight: 800;
    color: #0f172a;
    margin: 0 0 4px;
}

.card-desc {
    font-size: 12px;
    color: #94a3b8;
    margin: 0 0 18px;
}

.form-row {
    margin-bottom: 14px;
}

.form-field label {
    display: block;
    font-size: 12px;
    font-weight: 700;
    color: #374151;
    margin-bottom: 6px;
}

.form-field input,
.form-field select {
    width: 100%;
    padding: 10px 12px;
    border-radius: 8px;
    border: 1.5px solid #e2e8f0;
    font-size: 14px;
    box-sizing: border-box;
}

.candidate-list {
    display: flex;
    flex-direction: column;
    gap: 6px;
    max-height: 220px;
    overflow-y: auto;
    margin-bottom: 14px;
}

.candidate-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 12px;
    border-radius: 8px;
    border: 1.5px solid #e2e8f0;
    background: white;
    cursor: pointer;
    text-align: left;
}

.candidate-item.selected {
    border-color: #2563eb;
    background: #eff6ff;
}

.candidate-name {
    font-size: 13px;
    font-weight: 700;
    color: #1e293b;
}

.candidate-email {
    font-size: 12px;
    color: #94a3b8;
}

.empty-note {
    font-size: 12px;
    color: #94a3b8;
    margin-bottom: 14px;
}

.error-message {
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #dc2626;
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 12px;
    margin-bottom: 12px;
}

.success-message {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    color: #16a34a;
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 12px;
    margin-bottom: 12px;
}

.btn-primary {
    padding: 10px 20px;
    border-radius: 8px;
    border: none;
    background: #2563eb;
    color: white;
    font-size: 13px;
    font-weight: 700;
    cursor: pointer;
}

.btn-primary:disabled {
    background: #cbd5e1;
    cursor: not-allowed;
}
</style>
