<template>
    <div class="chart-container">
        <h3 class="chart-title">📊 週間学習時間</h3>
        <Bar :data="chartData" :options="chartOptions" />
    </div>
</template>

<script setup>
    import { computed } from "vue";
    import { Bar } from 'vue-chartjs'
    import {
        Chart as ChartJS,
        CategoryScale,
        LinearScale,
        BarElement,
        Title,
        Tooltip,
        Legend
    } from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const props = defineProps({
    weeklyData: {
    type: Array,
    default: () => []
    }
})

const chartData = computed(() => ({
    labels: props.weeklyData.map(d => d.date),
    datasets: [
    {
        label: '学習時間（分）',
        data: props.weeklyData.map(d => d.minutes),
        backgroundColor: 'rgba(102, 126, 234, 0.7)',
        borderColor: 'rgba(102, 126, 234, 1)',
        borderWidth: 2,
        borderRadius: 6,
    }
    ]
}))

const chartOptions = {
    responsive: true,
    maintainAspectRatio: true,
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
        callback: (value) => `${value}分`
        },
        grid: {
        color: 'rgba(0,0,0,0.05)'
        }
    },
    x: {
        grid: { display: false }
    }
    }
}
</script>

<style scoped>
.chart-container {
    background: white;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    margin-bottom: 16px;
}

.chart-title {
    font-size: 14px;
    font-weight: 600;
    color: #444;
    margin: 0 0 12px 0;
}
</style>