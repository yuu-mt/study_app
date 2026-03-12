<template>
    <div class="ranking-container">
        <h3 class="ranking-title">🏆 週間ランキング</h3>
        <div v-if="ranking.length === 0" class="empty">
        友達を追加するとランキングが表示されます
        </div>
        <div v-for="item in ranking" :key="item.user_id"
        :class="['ranking-item', item.is_me ? 'is-me' : '']"
        >
        <div class="rank">
            <span v-if="item.rank === 1">🥇</span>
            <span v-else-if="item.rank === 2">🥈</span>
            <span v-else-if="item.rank === 3">🥉</span>
            <span v-else>{{ item.rank }}</span>
        </div>
        <div class="avatar">{{ item.username[0] }}</div>
        <div class="user-info">
            <div class="username">
            {{ item.username }}
            <span v-if="item.is_me" class="me-badge">自分</span>
            </div>
            <div class="progress-bar">
            <div
                class="progress-fill"
                :style="{ width: getProgressWidth(item.weekly_minutes) + '%' }"
            ></div>
            </div>
        </div>
        <div class="time">{{ formatMinutes(item.weekly_minutes) }}</div>
        </div>
    </div>
</template>

<script setup>
    const props = defineProps({
    ranking: {
        type: Array,
        default: () => []
    }
})

const formatMinutes = (minutes) => {
    const h = Math.floor(minutes / 60)
    const m = minutes % 60
    if (h > 0) return m > 0 ? `${h}時間${m}分` : `${h}時間`
    return `${m}分`
}

const getProgressWidth = (minutes) => {
    if (props.ranking.length === 0) return 0
    const max = Math.max(...props.ranking.map(r => r.weekly_minutes))
    if (max === 0) return 0
    return Math.round((minutes / max) * 100)
}
</script>

<style scoped>
.ranking-container {
    background: white;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    margin-bottom: 16px;
}

.ranking-title {
    font-size: 14px;
    font-weight: 600;
    color: #444;
    margin: 0 0 12px 0;
}

.empty {
    text-align: center;
    color: #aaa;
    padding: 16px 0;
    font-size: 13px;
}

.ranking-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 0;
    border-bottom: 1px solid #f0f0f0;
}

.ranking-item:last-child {
    border-bottom: none;
}

.ranking-item.is-me {
    background: #f5f3ff;
    border-radius: 10px;
    padding: 10px 8px;
    margin: 0 -8px;
}

.rank {
    width: 28px;
    text-align: center;
    font-size: 18px;
    font-weight: 700;
    color: #888;
    flex-shrink: 0;
}

.avatar {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    font-weight: 700;
    flex-shrink: 0;
}

.user-info {
    flex: 1;
    min-width: 0;
}

.username {
    font-size: 13px;
    font-weight: 600;
    color: #1a1a2e;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 6px;
}

.me-badge {
    background: #667eea;
    color: white;
    font-size: 10px;
    padding: 1px 6px;
    border-radius: 10px;
    font-weight: 600;
}

.progress-bar {
    height: 4px;
    background: #f0f0f0;
    border-radius: 2px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 2px;
    transition: width 0.3s ease;
}

.time {
    font-size: 12px;
    font-weight: 600;
    color: #667eea;
    flex-shrink: 0;
}
</style>