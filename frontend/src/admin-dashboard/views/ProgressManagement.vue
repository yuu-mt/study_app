<template>
    <div class="page">
        <div class="page-header">
            <h1>進捗管理</h1>
            <p class="page-desc">受講生の進捗状況を確認できます。受講生名をクリックすると詳細が表示されます。</p>
        </div>

        <div class="filter-tabs">
            <button
                v-for="tab in filterTabs"
                :key="tab.value"
                class="filter-tab"
                :class="{ active: activeFilter === tab.value }"
                @click="setFilter(tab.value)"
            >
                {{ tab.label }}
            </button>
        </div>

        <div v-if="isLoading" class="state-message">読み込み中...</div>
        <div v-else-if="loadError" class="state-message error">読み込みに失敗しました</div>
        <TraineeTable v-else :trainees="trainees" />
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api.js'
import TraineeTable from '../components/TraineeTable.vue'

const filterTabs = [
    { value: 'in_progress', label: '受講中' },
    { value: 'not_started', label: '未受講' },
    { value: 'completed', label: '完了' },
    { value: 'all', label: 'すべて' },
]

// デフォルトは「受講中」フィルター（要件3-1-c）
const activeFilter = ref('in_progress')
const trainees = ref([])
const isLoading = ref(true)
const loadError = ref(false)

const fetchTrainees = async () => {
    isLoading.value = true
    loadError.value = false
    try {
        const res = await api.get('/curriculum/trainees/', {
            params: { status: activeFilter.value },
        })
        trainees.value = res.data.results ?? res.data
    } catch (error) {
        console.error(error)
        loadError.value = true
    } finally {
        isLoading.value = false
    }
}

const setFilter = (value) => {
    activeFilter.value = value
    fetchTrainees()
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

.filter-tabs {
    display: flex;
    gap: 6px;
    margin-bottom: 20px;
}

.filter-tab {
    padding: 8px 16px;
    border-radius: 20px;
    border: 1.5px solid #e2e8f0;
    background: white;
    color: #64748b;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s;
}

.filter-tab:hover {
    border-color: #93c5fd;
}

.filter-tab.active {
    background: #2563eb;
    border-color: #2563eb;
    color: white;
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
