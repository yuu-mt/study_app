<template>
    <div class="page">
        <div class="page-header">
            <h1>カリキュラム管理</h1>
            <p class="page-desc">
                <span v-if="isAdmin">章の追加・編集・削除・並び替えができます。</span>
                <span v-else>閲覧のみ可能です（編集はadminアカウントのみ）。</span>
            </p>
        </div>

        <div v-if="isLoading" class="state-message">読み込み中...</div>
        <div v-else-if="loadError" class="state-message error">読み込みに失敗しました</div>

        <template v-else>
            <table class="chapter-table">
                <thead>
                    <tr>
                        <th style="width:40px"></th>
                        <th>章番号</th>
                        <th>章タイトル</th>
                        <th>想定日数</th>
                        <th v-if="isAdmin" style="width:160px"></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(chapter, index) in chapters" :key="chapter.id">
                        <td class="reorder-cell" v-if="isAdmin">
                            <button class="reorder-btn" :disabled="index === 0" @click="move(index, -1)" title="上へ">▲</button>
                            <button class="reorder-btn" :disabled="index === chapters.length - 1" @click="move(index, 1)" title="下へ">▼</button>
                        </td>
                        <td v-else></td>
                        <td>{{ chapter.chapter_number }}</td>
                        <td>{{ chapter.title }}</td>
                        <td>{{ chapter.estimated_days }}日</td>
                        <td v-if="isAdmin" class="actions-cell">
                            <button class="btn-link" @click="startEdit(chapter)">編集</button>
                            <button class="btn-link danger" @click="deleteChapter(chapter)">削除</button>
                        </td>
                    </tr>
                </tbody>
            </table>
            <p class="total-note">全{{ chapters.length }}章・想定日数合計 {{ totalDays }}日</p>

            <section v-if="isAdmin" class="card">
                <h2>{{ editingChapter ? '章を編集' : '章を追加' }}</h2>
                <div class="form-grid">
                    <div class="form-field">
                        <label>章番号</label>
                        <input v-model="form.chapter_number" type="text" placeholder="例：14" />
                    </div>
                    <div class="form-field">
                        <label>章タイトル</label>
                        <input v-model="form.title" type="text" placeholder="例：総合演習" />
                    </div>
                    <div class="form-field">
                        <label>想定日数</label>
                        <input v-model.number="form.estimated_days" type="number" min="0" />
                    </div>
                </div>
                <div v-if="formError" class="error-message">{{ formError }}</div>
                <div class="form-actions">
                    <button v-if="editingChapter" class="btn-secondary" @click="cancelEdit">キャンセル</button>
                    <button class="btn-primary" :disabled="isSaving" @click="submitForm">
                        {{ isSaving ? '保存中...' : (editingChapter ? '更新する' : '追加する') }}
                    </button>
                </div>
            </section>
        </template>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../../api.js'
import { useAdminUser } from '../useAdminUser.js'

const { currentUser } = useAdminUser()
const isAdmin = computed(() => currentUser.value?.role === 'admin')

const chapters = ref([])
const isLoading = ref(true)
const loadError = ref(false)

const editingChapter = ref(null)
const form = ref({ chapter_number: '', title: '', estimated_days: 0 })
const formError = ref('')
const isSaving = ref(false)

const totalDays = computed(() => chapters.value.reduce((sum, c) => sum + c.estimated_days, 0))

const fetchChapters = async () => {
    isLoading.value = true
    loadError.value = false
    try {
        const res = await api.get('/curriculum/chapters/')
        chapters.value = (res.data.results ?? res.data).sort((a, b) => a.order - b.order)
    } catch (error) {
        console.error(error)
        loadError.value = true
    } finally {
        isLoading.value = false
    }
}

const startEdit = (chapter) => {
    editingChapter.value = chapter
    form.value = {
        chapter_number: chapter.chapter_number,
        title: chapter.title,
        estimated_days: chapter.estimated_days,
    }
    formError.value = ''
}

const cancelEdit = () => {
    editingChapter.value = null
    form.value = { chapter_number: '', title: '', estimated_days: 0 }
    formError.value = ''
}

const submitForm = async () => {
    formError.value = ''
    if (!form.value.chapter_number || !form.value.title) {
        formError.value = '章番号とタイトルを入力してください'
        return
    }
    isSaving.value = true
    try {
        if (editingChapter.value) {
            await api.patch(`/curriculum/chapters/${editingChapter.value.id}/`, {
                chapter_number: form.value.chapter_number,
                title: form.value.title,
                estimated_days: form.value.estimated_days,
            })
        } else {
            const nextOrder = chapters.value.length > 0
                ? Math.max(...chapters.value.map(c => c.order)) + 1
                : 0
            await api.post('/curriculum/chapters/', {
                chapter_number: form.value.chapter_number,
                title: form.value.title,
                estimated_days: form.value.estimated_days,
                order: nextOrder,
            })
        }
        cancelEdit()
        await fetchChapters()
    } catch (error) {
        formError.value = error.response?.data?.chapter_number?.[0] || '保存に失敗しました'
    } finally {
        isSaving.value = false
    }
}

const deleteChapter = async (chapter) => {
    if (!confirm(`「${chapter.chapter_number}. ${chapter.title}」を削除しますか？`)) return
    try {
        await api.delete(`/curriculum/chapters/${chapter.id}/`)
        await fetchChapters()
    } catch (error) {
        alert(error.response?.data?.error || '削除に失敗しました（進捗記録が存在する章は削除できません）')
    }
}

// 上下ボタンによる並び替え（要件3-3-a）
const move = async (index, direction) => {
    const targetIndex = index + direction
    if (targetIndex < 0 || targetIndex >= chapters.value.length) return

    const reordered = [...chapters.value]
    const [moved] = reordered.splice(index, 1)
    reordered.splice(targetIndex, 0, moved)
    chapters.value = reordered

    const payload = reordered.map((c, i) => ({ id: c.id, order: i }))
    try {
        await api.patch('/curriculum/chapters/reorder/', payload)
        await fetchChapters()
    } catch (error) {
        console.error(error)
        await fetchChapters()
    }
}

onMounted(fetchChapters)
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

.chapter-table {
    width: 100%;
    border-collapse: collapse;
    background: white;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #e2e8f0;
}

.chapter-table th {
    text-align: left;
    font-size: 12px;
    font-weight: 700;
    color: #64748b;
    background: #f8faff;
    padding: 10px 16px;
    border-bottom: 1px solid #e2e8f0;
}

.chapter-table td {
    padding: 11px 16px;
    font-size: 13px;
    color: #1e293b;
    border-bottom: 1px solid #f1f5f9;
}

.reorder-cell {
    display: flex;
    gap: 2px;
}

.reorder-btn {
    width: 22px;
    height: 22px;
    border-radius: 4px;
    border: 1px solid #e2e8f0;
    background: white;
    color: #64748b;
    font-size: 10px;
    cursor: pointer;
}

.reorder-btn:disabled {
    opacity: 0.3;
    cursor: not-allowed;
}

.actions-cell {
    display: flex;
    gap: 12px;
}

.btn-link {
    background: none;
    border: none;
    color: #2563eb;
    font-size: 12px;
    font-weight: 700;
    cursor: pointer;
    padding: 0;
}

.btn-link.danger {
    color: #dc2626;
}

.total-note {
    font-size: 12px;
    color: #94a3b8;
    margin: 10px 0 0;
}

.card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 24px;
    margin-top: 24px;
    max-width: 640px;
}

.card h2 {
    font-size: 15px;
    font-weight: 800;
    color: #0f172a;
    margin: 0 0 16px;
}

.form-grid {
    display: grid;
    grid-template-columns: 100px 1fr 120px;
    gap: 12px;
    margin-bottom: 14px;
}

.form-field label {
    display: block;
    font-size: 11px;
    font-weight: 700;
    color: #374151;
    margin-bottom: 6px;
}

.form-field input {
    width: 100%;
    padding: 9px 10px;
    border-radius: 8px;
    border: 1.5px solid #e2e8f0;
    font-size: 13px;
    box-sizing: border-box;
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

.form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 8px;
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
    padding: 9px 18px;
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

.state-message {
    padding: 40px;
    text-align: center;
    color: #64748b;
}

.state-message.error {
    color: #dc2626;
}
</style>
