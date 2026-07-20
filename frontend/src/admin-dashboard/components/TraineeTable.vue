<template>
    <table class="trainee-table">
        <thead>
            <tr>
                <th>氏名</th>
                <th>ステータス</th>
                <th>担当メンバー</th>
                <th>学習開始日</th>
                <th>完了予定日</th>
                <th>現在の章</th>
                <th v-if="editableStatus"></th>
            </tr>
        </thead>
        <tbody>
            <tr v-if="trainees.length === 0">
                <td :colspan="editableStatus ? 7 : 6" class="empty-cell">該当する受講生がいません</td>
            </tr>
            <tr v-for="trainee in trainees" :key="trainee.id">
                <td>
                    <router-link :to="`/admin-dashboard/trainees/${trainee.id}`" class="trainee-name">
                        {{ trainee.name }}
                    </router-link>
                    <span v-if="trainee.is_delayed" class="delay-badge" title="完了予定日から1日以上超過しています">遅延</span>
                </td>
                <td><span class="status-badge" :class="`status-${trainee.status}`">{{ statusLabel(trainee.status) }}</span></td>
                <td>{{ trainee.mentor_name || '—' }}</td>
                <td>{{ trainee.start_date || '—' }}</td>
                <td>{{ trainee.expected_end_date || '—' }}</td>
                <td>
                    <span v-if="trainee.current_chapter">
                        {{ trainee.current_chapter.chapter_number }}. {{ trainee.current_chapter.title }}
                    </span>
                    <span v-else class="muted">—</span>
                </td>
                <td v-if="editableStatus">
                    <select
                        class="status-select"
                        :value="trainee.status"
                        @change="onStatusSelect(trainee, $event.target.value)"
                    >
                        <option v-for="opt in STATUS_OPTIONS" :key="opt.value" :value="opt.value">
                            {{ opt.label }}
                        </option>
                    </select>
                </td>
            </tr>
        </tbody>
    </table>

    <!-- 「受講中」への変更時、学習開始日が未入力なら入力を求める（要件3-4） -->
    <div v-if="pendingChange" class="modal-backdrop" @click.self="cancelPendingChange">
        <div class="modal">
            <h3>学習開始日を入力してください</h3>
            <p class="modal-note">「受講中」への変更には学習開始日が必要です。完了予定日は自動算出されます。</p>
            <input type="date" v-model="pendingStartDate" />
            <div v-if="modalError" class="modal-error">{{ modalError }}</div>
            <div class="modal-actions">
                <button class="btn-secondary" @click="cancelPendingChange">キャンセル</button>
                <button class="btn-primary" @click="confirmPendingChange">確定</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { STATUS_OPTIONS, statusLabel } from '../utils.js'
import api from '../../api.js'

const props = defineProps({
    trainees: { type: Array, required: true },
    editableStatus: { type: Boolean, default: false },
})
const emit = defineEmits(['updated'])

const pendingChange = ref(null)
const pendingStartDate = ref(new Date().toISOString().split('T')[0])
const modalError = ref('')

const onStatusSelect = (trainee, newStatus) => {
    if (newStatus === trainee.status) return
    if (newStatus === 'in_progress' && !trainee.start_date) {
        pendingChange.value = { traineeId: trainee.id, status: newStatus }
        pendingStartDate.value = new Date().toISOString().split('T')[0]
        modalError.value = ''
        return
    }
    applyStatusChange(trainee.id, { status: newStatus })
}

const cancelPendingChange = () => {
    pendingChange.value = null
    modalError.value = ''
}

const confirmPendingChange = async () => {
    if (!pendingStartDate.value) {
        modalError.value = '学習開始日を選択してください'
        return
    }
    await applyStatusChange(pendingChange.value.traineeId, {
        status: pendingChange.value.status,
        start_date: pendingStartDate.value,
    })
    pendingChange.value = null
}

const applyStatusChange = async (traineeId, payload) => {
    try {
        await api.patch(`/curriculum/trainees/${traineeId}/status/`, payload)
        emit('updated')
    } catch (error) {
        console.error(error)
        alert('ステータスの変更に失敗しました')
    }
}
</script>

<style scoped>
.trainee-table {
    width: 100%;
    border-collapse: collapse;
    background: white;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #e2e8f0;
}

.trainee-table th {
    text-align: left;
    font-size: 12px;
    font-weight: 700;
    color: #64748b;
    background: #f8faff;
    padding: 12px 16px;
    border-bottom: 1px solid #e2e8f0;
}

.trainee-table td {
    padding: 14px 16px;
    font-size: 14px;
    color: #1e293b;
    border-bottom: 1px solid #f1f5f9;
}

.trainee-table tr:last-child td {
    border-bottom: none;
}

.empty-cell {
    text-align: center;
    color: #94a3b8;
    padding: 32px;
}

.trainee-name {
    color: #2563eb;
    font-weight: 700;
    text-decoration: none;
}

.trainee-name:hover {
    text-decoration: underline;
}

.delay-badge {
    margin-left: 8px;
    background: #fef2f2;
    color: #dc2626;
    font-size: 11px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 10px;
}

.status-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 10px;
    font-size: 12px;
    font-weight: 700;
}

.status-badge.status-not_started {
    background: #f1f5f9;
    color: #64748b;
}

.status-badge.status-in_progress {
    background: #eff6ff;
    color: #2563eb;
}

.status-badge.status-completed {
    background: #f0fdf4;
    color: #16a34a;
}

.muted {
    color: #cbd5e1;
}

.status-select {
    padding: 6px 10px;
    border-radius: 8px;
    border: 1.5px solid #e2e8f0;
    font-size: 13px;
    background: white;
}

.modal-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(15, 23, 42, 0.45);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 50;
}

.modal {
    background: white;
    border-radius: 12px;
    padding: 24px;
    width: 320px;
}

.modal h3 {
    margin: 0 0 8px;
    font-size: 16px;
}

.modal-note {
    font-size: 12px;
    color: #64748b;
    margin: 0 0 16px;
    line-height: 1.6;
}

.modal input[type="date"] {
    width: 100%;
    padding: 10px 12px;
    border-radius: 8px;
    border: 1.5px solid #e2e8f0;
    font-size: 14px;
    box-sizing: border-box;
}

.modal-error {
    color: #dc2626;
    font-size: 12px;
    margin-top: 8px;
}

.modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 8px;
    margin-top: 20px;
}

.btn-secondary {
    padding: 9px 16px;
    border-radius: 8px;
    border: 1.5px solid #e2e8f0;
    background: white;
    color: #64748b;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
}

.btn-primary {
    padding: 9px 16px;
    border-radius: 8px;
    border: none;
    background: #2563eb;
    color: white;
    font-size: 13px;
    font-weight: 700;
    cursor: pointer;
}
</style>
