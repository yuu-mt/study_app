<template>
    <div class="page">
        <div class="page-header">
            <h1>受講生一覧</h1>
            <p class="page-desc">全ての受講生を表示しています。ステータスはこの画面から直接変更できます。</p>
        </div>

        <div v-if="isLoading" class="state-message">読み込み中...</div>
        <div v-else-if="loadError" class="state-message error">読み込みに失敗しました</div>
        <TraineeTable v-else :trainees="trainees" editable-status @updated="fetchTrainees" />
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api.js'
import TraineeTable from '../components/TraineeTable.vue'

const trainees = ref([])
const isLoading = ref(true)
const loadError = ref(false)

const fetchTrainees = async () => {
    isLoading.value = true
    loadError.value = false
    try {
        const res = await api.get('/curriculum/trainees/')
        trainees.value = res.data.results ?? res.data
    } catch (error) {
        console.error(error)
        loadError.value = true
    } finally {
        isLoading.value = false
    }
}

onMounted(fetchTrainees)
</script>

<style scoped>
.page-header {
    margin-bottom: 20px;
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

.state-message {
    padding: 40px;
    text-align: center;
    color: #64748b;
}

.state-message.error {
    color: #dc2626;
}
</style>
