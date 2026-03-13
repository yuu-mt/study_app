<template>
    <div class="friends-container">
        <!-- ヘッダー -->
        <div class="header">
        <button class="btn-back" @click="router.push('/home')">← 戻る</button>
        <h1>👥 友達</h1>
        </div>

        <!-- ユーザー検索 -->
        <div class="search-section">
        <h3>ユーザーを検索</h3>
        <div class="search-box">
            <input
            v-model="searchQuery"
            type="text"
            placeholder="ユーザー名で検索..."
            @input="searchUsers"
            />
        </div>

        <!-- 検索結果 -->
        <div v-if="searchResults.length > 0" class="user-list">
            <div v-for="user in searchResults" :key="user.id" class="user-card">
            <div class="user-info">
                <div class="avatar">{{ user.username ? user.username[0] : '?' }}</div>
                <div>
                <div class="username">{{ user.username }}</div>
                <div class="email">{{ user.email }}</div>
                </div>
            </div>
            <button
                :class="['btn-friend', isFriend(user.id) ? 'following' : '']"
                @click="toggleFriend(user)"
            >
                {{ isFriend(user.id) ? '✓ 登録済み' : '+ 追加' }}
            </button>
            </div>
        </div>
        <div v-else-if="searchQuery && !isSearching" class="empty">
            ユーザーが見つかりません
        </div>
        </div>

        <!-- 友達一覧 -->
        <div class="friends-section">
        <h3>友達一覧（{{ friends.length }}人）</h3>
        <div v-if="friends.length === 0" class="empty">
            まだ友達がいません
        </div>
        <div v-for="friend in friends" :key="friend.id" class="friend-block">
            <!-- 友達ヘッダー -->
            <div class="user-card">
            <div class="user-info">
                <div class="avatar">{{ friend.username ? friend.username[0] : '?' }}</div>
                <div>
                <div class="username">{{ friend.username }}</div>
                <div class="email">{{ friend.email }}</div>
                </div>
            </div>
            <div class="friend-actions">
                <button class="btn-records" @click="toggleRecords(friend)">
                {{ openFriendId === friend.id ? '▲ 閉じる' : '📖 記録を見る' }}
                </button>
                <button class="btn-friend following" @click="toggleFriend(friend)">
                ✓ 登録済み
                </button>
            </div>
            </div>

            <!-- 友達の学習記録 -->
            <div v-if="openFriendId === friend.id" class="friend-records">
            <div v-if="friendRecords.length === 0" class="empty">
                学習記録がありません
            </div>
            <div v-for="record in friendRecords" :key="record.id" class="record-card">
                <div class="record-header">
                <span class="record-category">{{ record.category_name }}</span>
                <span class="record-date">{{ record.study_date }}</span>
                </div>
                <div class="record-title">{{ record.title }}</div>
                <div class="record-footer">
                <span class="record-duration">⏱ {{ record.duration_display }}</span>
                <button
                    :class="['stamp-btn', record.my_stamp ? 'stamped' : '']"
                    @click="toggleStamp(record)"
                >
                    👍 {{ record.stamp_count }}
                </button>
                </div>
            </div>
            </div>
        </div>
        </div>
    </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api.js'

const router = useRouter()
const friends = ref([])
const searchQuery = ref('')
const searchResults = ref([])
const isSearching = ref(false)
const openFriendId = ref(null)
const friendRecords = ref([])

const fetchFriends = async () => {
    try {
        const res = await api.get('/accounts/friends/')
        friends.value = res.data.results.filter(f => f !== null)
    } catch (error) {
        if (error.response?.status === 401) router.push('/login')
    }
}

const searchUsers = async () => {
    if (!searchQuery.value.trim()) {
        searchResults.value = []
        return
    }
    isSearching.value = true
    try {
        const res = await api.get('/accounts/search/', {
        params: { q: searchQuery.value }
        })
        searchResults.value = res.data.results 
    } catch (error) {
        console.error(error)
    } finally {
        isSearching.value = false
    }
}

const isFriend = (userId) => {
    return friends.value.some(f => f && f.id === userId)
    }

    const toggleFriend = async (user) => {
    try {
        await api.post(`/accounts/friends/${user.id}/`, {})
        fetchFriends()
    } catch (error) {
        console.error(error)
    }
}

onMounted(() => {
    fetchFriends()
})

    const toggleRecords = (friend) => {
    router.push(`/friends/${friend.id}`)
}

const toggleStamp = async (record) => {
    try {
        await api.post(`/study/records/${record.id}/stamp/`, { stamp_type: 'good' })
        // 記録を再取得
        const res = await api.get(`/study/friends/${openFriendId.value}/records/`)
        friendRecords.value = res.data.results
    } catch (error) {
        console.error(error)
    }
}
</script>

<style scoped>
.friends-container {
    max-width: 480px;
    margin: 0 auto;
    padding: 16px;
    background: #f5f7fa;
    min-height: 100vh;
}

.header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
}

.header h1 {
    font-size: 20px;
    font-weight: 700;
    color: #1a1a2e;
    margin: 0;
}

.btn-back {
    background: none;
    border: none;
    color: #667eea;
    font-size: 14px;
    cursor: pointer;
    padding: 0;
}

.search-section, .friends-section {
    background: white;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.search-section h3, .friends-section h3 {
    font-size: 14px;
    font-weight: 600;
    color: #444;
    margin: 0 0 12px 0;
}

.search-box input {
    width: 100%;
    padding: 10px 14px;
    border: 2px solid #e8e8e8;
    border-radius: 10px;
    font-size: 15px;
    outline: none;
    box-sizing: border-box;
}

.search-box input:focus {
    border-color: #667eea;
}

.user-list {
    margin-top: 12px;
}

.user-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #f0f0f0;
}

.user-card:last-child {
    border-bottom: none;
}

.user-info {
    display: flex;
    align-items: center;
    gap: 10px;
}

.avatar {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    font-weight: 700;
}

.username {
    font-size: 14px;
    font-weight: 600;
    color: #1a1a2e;
}

.email {
    font-size: 12px;
    color: #aaa;
}

.btn-friend {
    padding: 6px 14px;
    border-radius: 20px;
    border: 1px solid #667eea;
    background: white;
    color: #667eea;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
}

.btn-friend.following {
    background: #667eea;
    color: white;
}

.empty {
    text-align: center;
    color: #aaa;
    padding: 20px 0;
    font-size: 14px;
}

.friend-block {
    margin-bottom: 8px;
    border-bottom: 1px solid #f0f0f0;
}

.friend-block:last-child {
    border-bottom: none;
}

.friend-actions {
    display: flex;
    gap: 8px;
    align-items: center;
}

.btn-records {
    padding: 6px 10px;
    border-radius: 20px;
    border: 1px solid #ddd;
    background: white;
    color: #555;
    font-size: 11px;
    font-weight: 600;
    cursor: pointer;
}

.friend-records {
    padding: 8px 0 8px 48px;
}

.record-card {
    background: #f9f9f9;
    border-radius: 10px;
    padding: 10px 12px;
    margin-bottom: 8px;
}

.record-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 4px;
}

.record-category {
    font-size: 11px;
    color: #888;
    font-weight: 600;
}

.record-date {
    font-size: 11px;
    color: #aaa;
}

.record-title {
    font-size: 14px;
    font-weight: 600;
    color: #1a1a2e;
    margin-bottom: 6px;
}

.record-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.record-duration {
    font-size: 12px;
    color: #888;
}

.stamp-btn {
    background: none;
    border: 1px solid #ddd;
    border-radius: 20px;
    padding: 4px 10px;
    font-size: 12px;
    cursor: pointer;
    color: #888;
    transition: all 0.2s;
}

.stamp-btn.stamped {
    background: #fff0f0;
    border-color: #ffcccc;
    color: #e53e3e;
}
</style>