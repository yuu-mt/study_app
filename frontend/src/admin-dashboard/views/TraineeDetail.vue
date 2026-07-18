<template>
    <div class="page">
        <router-link to="/admin-dashboard/trainees" class="back-link">← 受講生一覧へ戻る</router-link>

        <div v-if="isLoading" class="state-message">読み込み中...</div>
        <div v-else-if="loadError" class="state-message error">読み込みに失敗しました</div>

        <template v-else-if="trainee">
            <div class="page-header">
                <div class="header-main">
                    <h1>{{ trainee.name }}</h1>
                    <span class="status-badge" :class="`status-${trainee.status}`">{{ statusLabel(trainee.status) }}</span>
                    <span v-if="trainee.is_delayed" class="delay-badge">遅延中</span>
                </div>
                <div class="meta-grid">
                    <div class="meta-item"><span class="meta-label">担当メンバー</span>{{ trainee.mentor_name || '—' }}</div>
                    <div class="meta-item"><span class="meta-label">学習開始日</span>{{ trainee.start_date || '—' }}</div>
                    <div class="meta-item"><span class="meta-label">完了予定日</span>{{ trainee.expected_end_date || '—' }}</div>
                    <div class="meta-item">
                        <span class="meta-label">現在の章</span>
                        <span v-if="trainee.current_chapter">{{ trainee.current_chapter.chapter_number }}. {{ trainee.current_chapter.title }}</span>
                        <span v-else>—</span>
                    </div>
                </div>
            </div>

            <section class="section">
                <h2>章別の進捗</h2>
                <table class="progress-table">
                    <thead>
                        <tr>
                            <th>章</th>
                            <th>状態</th>
                            <th>完了日時</th>
                            <th>累計学習時間</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="progress in trainee.chapter_progresses" :key="progress.id">
                            <td>
                                <button
                                    class="chapter-link"
                                    :class="{ active: selectedChapter === progress.chapter_number }"
                                    @click="toggleChapterFilter(progress.chapter_number)"
                                    title="この章の振り返り記録だけを表示"
                                >
                                    {{ progress.chapter_number }}. {{ progress.chapter_title }}
                                </button>
                            </td>
                            <td>
                                <span class="progress-badge" :class="progress.is_completed ? 'done' : 'pending'">
                                    {{ progress.is_completed ? '完了' : '未完了' }}
                                </span>
                            </td>
                            <td>{{ formatDateTime(progress.completed_at) }}</td>
                            <td>{{ formatMinutes(progress.total_minutes) }}</td>
                        </tr>
                        <tr v-if="trainee.chapter_progresses.length === 0">
                            <td colspan="4" class="empty-cell">まだ学習記録がありません</td>
                        </tr>
                    </tbody>
                </table>
            </section>

            <section class="section">
                <div class="section-head">
                    <h2>振り返り記録</h2>
                    <span v-if="selectedChapter" class="filter-note">
                        「{{ selectedChapter }}章」のみ表示中
                        <button class="clear-filter" @click="selectedChapter = null">すべて表示</button>
                    </span>
                </div>
                <div v-if="filteredReflections.length === 0" class="empty-cell">
                    {{ selectedChapter ? 'この章の振り返り記録はまだありません' : '振り返り記録がまだありません' }}
                </div>
                <div v-else class="reflection-list">
                    <div class="reflection-card" v-for="(r, idx) in filteredReflections" :key="idx">
                        <div class="reflection-head">
                            <span class="reflection-chapter" v-if="r.chapter">{{ r.chapter }}. {{ r.chapter_title }}</span>
                            <span class="reflection-item" v-if="r.item">{{ r.item }}. {{ r.item_title }}</span>
                            <span class="reflection-date">{{ r.study_date }}</span>
                            <span v-if="r.understanding" class="reflection-stars">{{ '★'.repeat(r.understanding) }}{{ '☆'.repeat(5 - r.understanding) }}</span>
                        </div>
                        <dl class="reflection-body">
                            <template v-if="r.questions"><dt>問題点/疑問点</dt><dd>{{ r.questions }}</dd></template>
                            <template v-if="r.struggles"><dt>難しかったこと</dt><dd>{{ r.struggles }}</dd></template>
                            <template v-if="r.achievements"><dt>できるようになったこと</dt><dd>{{ r.achievements }}</dd></template>
                            <template v-if="r.solutions"><dt>解決に向けて行ったこと</dt><dd>{{ r.solutions }}</dd></template>
                        </dl>
                    </div>
                </div>
            </section>
        </template>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../../api.js'
import { statusLabel, formatMinutes } from '../utils.js'

const route = useRoute()
const trainee = ref(null)
const isLoading = ref(true)
const loadError = ref(false)

// 章別の進捗テーブルで章名をクリックすると、その章の振り返り記録だけに絞り込む
const selectedChapter = ref(null)

const toggleChapterFilter = (chapterNumber) => {
    selectedChapter.value = selectedChapter.value === chapterNumber ? null : chapterNumber
}

const filteredReflections = computed(() => {
    if (!trainee.value) return []
    if (!selectedChapter.value) return trainee.value.reflections
    return trainee.value.reflections.filter(r => r.chapter === selectedChapter.value)
})

const formatDateTime = (value) => {
    if (!value) return '—'
    return new Date(value).toLocaleString('ja-JP')
}

const fetchTrainee = async () => {
    isLoading.value = true
    loadError.value = false
    try {
        const res = await api.get(`/curriculum/trainees/${route.params.id}/`)
        trainee.value = res.data
    } catch (error) {
        console.error(error)
        loadError.value = true
    } finally {
        isLoading.value = false
    }
}

onMounted(fetchTrainee)
</script>

<style scoped>
.back-link {
    display: inline-block;
    margin-bottom: 16px;
    color: #2563eb;
    font-size: 13px;
    font-weight: 600;
    text-decoration: none;
}

.page-header {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 24px;
}

.header-main {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 16px;
}

.header-main h1 {
    font-size: 22px;
    font-weight: 800;
    color: #0f172a;
    margin: 0;
}

.status-badge {
    padding: 3px 10px;
    border-radius: 10px;
    font-size: 12px;
    font-weight: 700;
}

.status-badge.status-not_started { background: #f1f5f9; color: #64748b; }
.status-badge.status-in_progress { background: #eff6ff; color: #2563eb; }
.status-badge.status-completed { background: #f0fdf4; color: #16a34a; }

.delay-badge {
    background: #fef2f2;
    color: #dc2626;
    font-size: 12px;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 10px;
}

.meta-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 16px;
}

.meta-item {
    font-size: 14px;
    color: #1e293b;
    font-weight: 600;
}

.meta-label {
    display: block;
    font-size: 11px;
    color: #94a3b8;
    font-weight: 700;
    margin-bottom: 4px;
    text-transform: uppercase;
    letter-spacing: 0.03em;
}

.section {
    margin-bottom: 28px;
}

.section h2 {
    font-size: 15px;
    font-weight: 800;
    color: #0f172a;
    margin: 0 0 12px;
}

.section-head {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
}

.section-head h2 {
    margin: 0;
}

.filter-note {
    font-size: 12px;
    color: #2563eb;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 8px;
}

.clear-filter {
    background: none;
    border: none;
    color: #94a3b8;
    font-size: 12px;
    font-weight: 600;
    text-decoration: underline;
    cursor: pointer;
    padding: 0;
}

.chapter-link {
    background: none;
    border: none;
    padding: 4px 8px;
    margin: -4px -8px;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 600;
    color: #1e293b;
    cursor: pointer;
    text-align: left;
}

.chapter-link:hover {
    background: #eff6ff;
    color: #2563eb;
}

.chapter-link.active {
    background: #2563eb;
    color: white;
}

.progress-table {
    width: 100%;
    border-collapse: collapse;
    background: white;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #e2e8f0;
}

.progress-table th {
    text-align: left;
    font-size: 12px;
    font-weight: 700;
    color: #64748b;
    background: #f8faff;
    padding: 10px 16px;
    border-bottom: 1px solid #e2e8f0;
}

.progress-table td {
    padding: 12px 16px;
    font-size: 13px;
    color: #1e293b;
    border-bottom: 1px solid #f1f5f9;
}

.progress-badge {
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 11px;
    font-weight: 700;
}

.progress-badge.done { background: #f0fdf4; color: #16a34a; }
.progress-badge.pending { background: #f1f5f9; color: #94a3b8; }

.empty-cell {
    text-align: center;
    color: #94a3b8;
    padding: 24px;
    font-size: 13px;
}

.reflection-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.reflection-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 16px 18px;
}

.reflection-head {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
    font-size: 12px;
    flex-wrap: wrap;
}

.reflection-chapter {
    background: #eff6ff;
    color: #2563eb;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 8px;
}

.reflection-item {
    background: #f5f3ff;
    color: #7c3aed;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 8px;
}

.reflection-date {
    color: #94a3b8;
}

.reflection-stars {
    color: #fbbf24;
    margin-left: auto;
}

.reflection-body {
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.reflection-body dt {
    font-size: 11px;
    font-weight: 700;
    color: #64748b;
    margin-bottom: 2px;
}

.reflection-body dd {
    margin: 0;
    font-size: 13px;
    color: #1e293b;
    line-height: 1.6;
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
