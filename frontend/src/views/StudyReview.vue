<template>
    <div class="review-container">
        <div class="header">
            <h1>振り返り</h1>
            <p class="subtitle">{{ studyTitle }}</p>
        </div>

        <div class="review-body">
            <p class="intro">お疲れ様でした！振り返りを記録しましょう。<br> (スキップして後で入力もできます)</p>

            <!-- カテゴリーが「カリキュラム」の場合のみ章選択UIを表示（要件4-4） -->
            <div class="form-group" v-if="isCurriculum">
                <label>対象の章</label>
                <select v-model="form.chapter">
                <option value="">選択してください</option>
                <option v-for="chapter in chapters" :key="chapter.id" :value="chapter.id">
                    {{ chapter.chapter_number }}. {{ chapter.title }}
                </option>
                </select>
            </div>

            <!-- 理解度 -->
            <div class="form-group">
                <label>理解度</label>
                <div class="stars">
                    <button
                        v-for="i in 5"
                        :key="i"
                        :class="['star-btn', form.understanding >= i ? 'active' : '']"
                        @click="form.understanding = i"
                    >★</button>
                </div>
            </div>

            <div class="form-group">
                <label>問題点/疑問点</label>
                <textarea
                v-model="form.questions"
                placeholder="わからなかったこと、もっと調べたいことなど"></textarea>
            </div>
            <div class="form-group">
                <label>解決に向けて行なったこと</label>
                <textarea
                v-model="form.solutions"
                placeholder="問題をどう解決したか、次回の課題など"></textarea>
            </div>
            <div class="form-group">
                <label>できるようになったこと</label>
                <textarea
                v-model="form.achievements"
                placeholder="今日習得したこと、理解が深まったことなど"></textarea>
            </div>
            <div class="form-group">
                <label>難しかったこと</label>
                <textarea
                v-model="form.struggles"
                placeholder="つまずいた点、時間がかかったこと"></textarea>
            </div>

            <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

            <div class="actions">
                <button class="btn-skip" @click="skip">スキップ</button>
                <button class="btn-save" @click="save" :disabled="isSaving">{{ isSaving ? '保存中...' : '保存してホームへ' }}</button>
            </div>

            <!-- 章の完了操作（要件3-2）：受講生自身の操作のみで完了が確定し、講師承認は不要 -->
            <div v-if="isCurriculum" class="complete-section">
                <button class="btn-complete-chapter" @click="completeChapter" :disabled="isSaving">
                    {{ isSaving ? '処理中...' : '✓ この章を完了する' }}
                </button>
                <p class="complete-note">完了操作は取り消せません。振り返り内容も一緒に保存されます。</p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import api from '../api.js'

const router = useRouter()
const route = useRoute()

const recordId = ref(null)
const studyTitle = ref('')
const isSaving = ref(false)
const errorMessage = ref('')
const isCurriculum = ref(false)
const chapters = ref([])

const form = ref({
    understanding: 0,
    questions: '',
    struggles: '',
    achievements: '',
    solutions: '',
    chapter: '',
})

const fetchChapters = async () => {
    try {
        const res = await api.get('/curriculum/chapters/options/')
        chapters.value = res.data
    } catch (error) {
        console.error(error)
    }
}

onMounted(() => {
    recordId.value = route.query.id
    studyTitle.value = route.query.title || '学習記録'
    if (!recordId.value){
        router.push('/home')
        return
    }
    isCurriculum.value = route.query.curriculum === '1'
    if (route.query.chapter) {
        form.value.chapter = Number(route.query.chapter)
    }
    if (isCurriculum.value) {
        fetchChapters()
    }
})

const save = async () => {
    isSaving.value = true
    errorMessage.value = ''
    try{
        await api.patch(`/study/records/${recordId.value}/`,{
            questions: form.value.questions,
            struggles: form.value.struggles,
            achievements: form.value.achievements,
            solutions: form.value.solutions,
            understanding: form.value.understanding || null,
        })
        router.push('/home')
    } catch(error) {
        errorMessage.value = '保存に失敗しました'
    } finally {
        isSaving.value = false
    }
}

// 章の完了操作。振り返り記録の保存と同時に、対象章を完了として記録する（要件3-2・4-4）
const completeChapter = async () => {
    errorMessage.value = ''
    if (!form.value.chapter) {
        errorMessage.value = '対象の章を選択してください'
        return
    }
    if (!confirm('この章を完了として記録します。よろしいですか？（完了後の取消はできません）')) return

    isSaving.value = true
    try {
        await api.patch(`/study/records/${recordId.value}/`, {
            chapter: Number(form.value.chapter),
            is_chapter_completion: true,
            questions: form.value.questions,
            struggles: form.value.struggles,
            achievements: form.value.achievements,
            solutions: form.value.solutions,
            understanding: form.value.understanding || null,
        })
        router.push('/home')
    } catch (error) {
        errorMessage.value = '完了処理に失敗しました'
    } finally {
        isSaving.value = false
    }
}

const skip = () => {
    router.push('/home')
}
</script>

<style scoped>
.review-container {
    max-width: 560px;
    margin: 0 auto;
    background: #f8faff;
    min-height: 100vh;
    padding-bottom: 48px;
}

.header {
    background: #2563eb;
    padding: 20px 20px 16px;
    color: white;
}

.header h1 {
    font-size: 20px;
    font-weight: 700;
    margin: 0 0 4px 0;
}

.subtitle {
    font-size: 13px;
    opacity: 0.85;
    margin: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.review-body {
    padding: 24px 20px 0;
}

.intro {
    font-size: 13px;
    color: #64748b;
    margin: 0 0 24px;
    line-height: 1.6;
}

.form-group {
    margin-bottom: 22px;
}

.form-group label {
    display: block;
    font-size: 13px;
    font-weight: 600;
    color: #374151;
    margin-bottom: 8px;
}

.form-group textarea {
    width: 100%;
    padding: 12px 14px;
    border: 1.5px solid #e2e8f0;
    border-radius: 10px;
    font-size: 15px;
    outline: none;
    box-sizing: border-box;
    resize: none;
    min-height: 88px;
    transition: border-color 0.2s;
    background: white;
    line-height: 1.6;
}

.form-group textarea:focus {
    border-color: #2563eb;
}

.stars {
    display: flex;
    gap: 10px;
}

.star-btn {
    font-size: 28px;
    background: none;
    border: none;
    cursor: pointer;
    color: #e2e8f0;
    padding: 2px 0;
    transition: color 0.15s;
    line-height: 1;
}

.star-btn.active {
    color: #fbbf24;
}

.error-message {
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #dc2626;
    padding: 10px 14px;
    border-radius: 8px;
    font-size: 13px;
    margin-bottom: 16px;
}

.actions {
    display: flex;
    gap: 12px;
    margin-top: 28px;
}

.btn-skip {
    flex: 1;
    padding: 13px;
    border-radius: 10px;
    border: 1.5px solid #e2e8f0;
    background: white;
    color: #64748b;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
}

.btn-save {
    flex: 2;
    padding: 13px;
    border-radius: 10px;
    border: none;
    background: #2563eb;
    color: white;
    font-size: 15px;
    font-weight: 700;
    cursor: pointer;
}

.btn-save:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.complete-section {
    margin-top: 20px;
    text-align: center;
}

.btn-complete-chapter {
    width: 100%;
    padding: 14px;
    border-radius: 10px;
    border: none;
    background: #16a34a;
    color: white;
    font-size: 15px;
    font-weight: 700;
    cursor: pointer;
}

.btn-complete-chapter:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.complete-note {
    font-size: 12px;
    color: #94a3b8;
    margin: 8px 0 0;
}

@media (min-width: 720px) {
    .review-container {
        margin-top: 24px;
        margin-bottom: 24px;
        min-height: calc(100vh - 48px);
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 16px 40px rgba(15, 23, 42, 0.12);
    }

    .review-body {
        padding: 28px 28px 0;
    }
}

@media (max-width: 520px) {
    .actions {
        flex-direction: column-reverse;
    }

    .btn-skip,
    .btn-save {
        flex: none;
        width: 100%;
    }
}
</style>
