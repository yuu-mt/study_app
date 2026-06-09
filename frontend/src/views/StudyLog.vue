<template>
    <div class="log-container">
        <div class="header">
        <button class="btn-back" @click="router.push('/home')">← 戻る</button>
        <h1>📖 学習の軌跡</h1>
        </div>

        <div class="filter-area">
        <div class="filter-row">
            <select v-model="selectedCategory" @change="fetchLogs(1)">
            <option value="">すべて</option>
            <option v-for="cat in categories" :key="cat.id" :value="cat.name">
                {{ cat.get_name_display }}
            </option>
            </select>
            <input
            v-model="searchQuery"
            type="text"
            placeholder="🔍 キーワード検索"
            class="search-input"
            />
            <button class="btn-csv" @click="exportCSV">CSV</button>
        </div>
        </div>

        <!-- 月別グラフ -->
        <div v-if="monthlyData.length > 0" class="chart-section">
            <div class="chart-area">
                <div class="chart-title">月別学習時間</div>
                <div class="chart-wrap">
                    <Bar :data="chartData" :options="chartOptions" />
                </div>
            </div>
            <div v-if="monthlyComparison" class="comparison-area">
                <div class="comp-title">前月比</div>
                    <div :class="['comp-diff', monthlyComparison.isUp ? 'up' : 'down']">
                    {{ monthlyComparison.isUp ? '▲' : '▼' }} {{ monthlyComparison.diffStr }}
                    </div>
                    <div class="comp-detail">
                    <div class="comp-row">
                        <span>今月</span>
                        <span>{{ Math.floor(monthlyComparison.current.minutes / 60) }}時間{{ monthlyComparison.current.minutes % 60 }}分</span>
                    </div>
                    <div class="comp-row">
                        <span>前月</span>
                        <span>{{ Math.floor(monthlyComparison.previous.minutes / 60) }}時間{{ monthlyComparison.previous.minutes % 60 }}分</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="count-bar">{{ filteredLogs.length }}件</div>

        <!-- テーブル -->
        <div class="table-scroll">
        <table class="log-table">
            <thead>
            <tr>
                <th class="col-category">カテゴリー</th>
                <th class="col-title">タイトル</th>
                <th class="col-text">疑問点</th>
                <th class="col-text">解決策</th>
                <th class="col-text">できたこと</th>
                <th class="col-text">難しかったこと</th>
                <th class="col-star">理解度</th>
            </tr>
            </thead>
            <tbody>
            <tr v-if="filteredLogs.length === 0">
                <td colspan="7" class="empty">該当する記録がありません</td>
            </tr>
            <tr v-for="log in filteredLogs" :key="log.id">
                <td class="col-category">
                <span class="category-badge">{{ log.category_name }}</span>
                <div class="log-date">{{ log.study_date }}</div>
                </td>
                <td class="col-title">
                <div class="title-text">{{ log.title }}</div>
                <div v-if="log.description" class="sub-text">{{ log.description }}</div>
                </td>
                <td class="col-text">
                <span class="cell-text">{{ log.questions || '—' }}</span>
                </td>
                <td class="col-text">
                <span class="cell-text">{{ log.solutions|| '—' }}</span>
                </td>
                <td class="col-text">
                <span class="cell-text">{{ log.achievements || '—' }}</span>
                </td>
                <td class="col-text">
                <span class="cell-text">{{ log.struggles || '—' }}</span>
                </td>
                <td class="col-star">
                <div v-if="log.understanding" class="stars">
                    <span v-for="i in 5" :key="i" :class="log.understanding >= i ? 'star-on' : 'star-off'">★</span>
                </div>
                <span v-else class="no-data">—</span>
                </td>
            </tr>
            </tbody>
        </table>
        </div>

        <!-- ページネーション -->
        <div v-if="totalCount > 0" class="pagination">
        <button class="page-btn" :disabled="currentPage === 1" @click="changePage(currentPage - 1)">← 前へ</button>
        <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
        <button class="page-btn" :disabled="currentPage === totalPages" @click="changePage(currentPage + 1)">次へ →</button>
        </div>
    </div>
</template>

<script setup>
    import { ref, computed, onMounted } from 'vue'
    import { useRouter } from 'vue-router'
    import api from '../api.js'
    import{ Bar }from 'vue-chartjs'
    import{
        Chart as ChartJS,
        CategoryScale,
        LinearScale,
        BarElement,
        Title,
        Tooltip,
        Legend
    } from 'chart.js'

    ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

    const router = useRouter()

    const logs = ref([])
    const categories = ref([])
    const selectedCategory = ref('')
    const searchQuery = ref('')
    const currentPage = ref(1)
    const totalCount = ref(0)
    const pageSize = 10
    const monthlyData = ref([])

    const totalPages = computed(() => Math.ceil(totalCount.value / pageSize))

    const filteredLogs = computed(() => {
    if (!searchQuery.value.trim()) return logs.value
    const keywords = searchQuery.value.trim().split(/\s+/)
    return logs.value.filter(log => {
        const target = [
        log.title, log.description, log.questions,
        log.struggles, log.achievements, log.solutions
        ].join(' ').toLowerCase()
        return keywords.every(kw => target.includes(kw.toLowerCase()))
    })
    })

    const fetchLogs = async (page = 1) => {
    try {
        const params = { page, page_size: pageSize }
        if (selectedCategory.value) params.category = selectedCategory.value
        const res = await api.get('/study/records/', { params })
        logs.value = res.data.results
        totalCount.value = res.data.count
        currentPage.value = page
    } catch (error) {
        if (error.response?.status === 401) router.push('/login')
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

    const changePage = (page) => {
    fetchLogs(page)
    window.scrollTo(0, 0)
    }

    const exportCSV = () => {
    const headers = ['日付', 'カテゴリー', 'タイトル', '学習内容', '理解度', '疑問点', '苦労したこと', 'できたこと', '解決策', '学習時間(分)']
    const rows = filteredLogs.value.map(log => [
        log.study_date,
        log.category_name || '',
        log.title,
        log.description || '',
        log.understanding || '',
        log.questions || '',
        log.struggles || '',
        log.achievements || '',
        log.solutions || '',
        log.duration_minutes,
    ])
    const csvContent = [headers, ...rows]
        .map(row => row.map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(','))
        .join('\n')
    const bom = '\uFEFF'
    const blob = new Blob([bom + csvContent], { type: 'text/csv;charset=utf-8;' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `学習の軌跡_${new Date().toISOString().split('T')[0]}.csv`
    a.click()
    URL.revokeObjectURL(url)
    }

    const fetchMonthlyChart = async () => {
        try{
            const res = await api.get('/study/monthly-chart/')
            monthlyData.value = res.data
        } catch (error) {
            console.error(error)
        }
    }

    const monthlyComparison = computed(() => {
        if(monthlyData.value.length < 2) return null
        const last = monthlyData.value[monthlyData.value.length - 1]
        const prev = monthlyData.value[monthlyData.value.length - 2]
        const diff = last.minutes - prev.minutes
        const diffH = Math.floor(Math.abs(diff) / 60)
        const diffM = Math.abs(diff) % 60
        const diffStr = diffH > 0 ? `${diffH}時間${diffM}分` : `${diffM}分`
        return{
            current: last,
            previous: prev,
            diff,
            diffStr,
            isUp: diff >= 0,
        }
    })

    const chartData = computed(() => ({
        labels: monthlyData.value.map(d => d.month),
        datasets:[
            {
                data: monthlyData.value.map(d => d.minutes),
                backgroundColor: monthlyData.value.map((_, i) =>i === monthlyData.value.length - 1 ? 'rgba(37, 99, 235, 0.85)' : 'rgba(37, 99, 235, 0.35)'),
                borderRadius: 4,
                barThickness: 32,      
                maxBarThickness: 48,  
            }
        ]
    }))

const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: { display: false },
        tooltip: {
        callbacks: {
            label: (context) => {
            const minutes = context.raw
            const h = Math.floor(minutes / 60)
            const m = minutes % 60
            if (h > 0) return m > 0 ? ` ${h}時間${m}分` : ` ${h}時間`
            return ` ${m}分`
            }
        }
        }
    },
    scales: {
        y: {
        beginAtZero: true,
        ticks: {
            callback: (value) => {
            const h = Math.floor(value / 60)
            return h > 0 ? `${h}h` : `${value}m`
            }
        },
        grid: { color: 'rgba(0,0,0,0.05)' }
        },
        x: { grid: { display: false } }
    }
}

    onMounted(() => {
    fetchLogs()
    fetchCategories()
    fetchMonthlyChart()
    })
</script>

<style scoped>
.log-container {
    max-width: 100%;
    margin: 0 auto;
    background: #f8faff;
    min-height: 100vh;
    padding-bottom: 40px;
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
    white-space: nowrap;
}

.filter-area {
    padding: 12px 16px;
    background: white;
    border-bottom: 1px solid #e2e8f0;
}

.filter-row {
    display: flex;
    gap: 8px;
    align-items: center;
}

.filter-row select {
    padding: 8px 10px;
    border: 1.5px solid #e2e8f0;
    border-radius: 8px;
    font-size: 13px;
    outline: none;
    background: white;
    min-width: 100px;
}

.search-input {
    width: 160px;
    padding: 8px 12px;
    border: 1.5px solid #e2e8f0;
    border-radius: 8px;
    font-size: 13px;
    outline: none;
}

.search-input:focus {
    border-color: #2563eb;
}

.btn-csv {
    padding: 8px 14px;
    background: #2563eb;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    white-space: nowrap;
}

.count-bar {
    padding: 6px 16px;
    font-size: 12px;
    color: #64748b;
    background: #f8faff;
}

.table-scroll {
    overflow-x: auto;
    padding: 0 8px;
}

.log-table {
    width: 100%;
    border-collapse: collapse;
    background: white;
    border-radius: 8px;
    overflow: hidden;
    font-size: 13px;
    min-width: 700px;
}

.log-table thead tr {
    background: #2563eb;
    color: white;
}

.log-table th {
    padding: 10px 12px;
    text-align: left;
    font-weight: 600;
    font-size: 12px;
    white-space: nowrap;
}

.log-table tbody tr {
    border-bottom: 1px solid #f1f5f9;
    transition: background 0.15s;
}

.log-table tbody tr:hover {
    background: #f8faff;
}

.col-category { width: 90px; }
.col-title    { width: 140px; }
.col-text     { width: 160px; }
.col-star     { width: 80px; }

.log-table td {
    padding: 10px 12px;
    vertical-align: top;
}

.category-badge {
    font-size: 11px;
    color: #2563eb;
    font-weight: 700;
    background: #eff6ff;
    padding: 2px 6px;
    border-radius: 8px;
    display: inline-block;
}

.log-date {
    font-size: 11px;
    color: #94a3b8;
    margin-top: 3px;
}

.title-text {
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 2px;
}

.sub-text {
    font-size: 11px;
    color: #64748b;
}

.cell-text {
    color: #4b5563;
    line-height: 1.5;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.no-data {
    color: #cbd5e1;
}

.stars { font-size: 12px; }
.star-on  { color: #fbbf24; }
.star-off { color: #e2e8f0; }

.empty {
    text-align: center;
    color: #94a3b8;
    padding: 40px;
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

.chart-section {
    display: flex;
    gap: 12px;
    padding: 12px 16px;
    background: white;
    border-bottom: 1px solid #e2e8f0;
    align-items: flex-start;
}

.chart-area {
    width: 340px;
    min-width: 200px;
}

.chart-title {
    font-size: 12px;
    font-weight: 600;
    color: #374151;
    margin-bottom: 6px;
}

.chart-wrap {
    height: 120px;
}

.comparison-area {
    width: 140px;
    flex-shrink: 0;
    background: #f8faff;
    border-radius: 10px;
    padding: 10px;
    text-align: center;
    margin-top: 20px;
    margin-left: 30px;
}

@media (max-width: 480px) {
    .chart-section {
        flex-direction: column;
    }

    .chart-area {
        width: 100%;
        min-width: unset;
        flex: unset;
    }

    .comparison-area {
        width: 100%;
        margin-top: 0;
        display: flex;
        align-items: center;
        gap: 12px;
        text-align: left;
        padding: 8px 12px;
        box-sizing: border-box;
    }
}

.comp-title {
    font-size: 11px;
    color: #64748b;
    margin-bottom: 4px;
}

.comp-diff {
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 8px;
}

.comp-diff.up   { color: #2563eb; }
.comp-diff.down { color: #dc2626; }

.comp-detail {
    font-size: 11px;
    color: #64748b;
}

.comp-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 2px;
}
</style>
