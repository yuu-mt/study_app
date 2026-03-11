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
                        <div class="avatar">{{ user.username[0] }}</div>
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
            <div v-for="friend in friends" :key="friend.id" class="user-card">
                <div class="user-info">
                    <div class="avatar">{{ friend.username[0] }}</div>
                    <div>
                        <div class="username">{{ friend.username }}</div>
                        <div class="email">{{ friend.email }}</div>
                    </div>
                </div>
                <button class="btn-friend following" @click="toggleFriend(friend)">
                ✓ 登録済み
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const friends = ref([])
const searchQuery = ref('')
const searchResults = ref([])
const isSearching = ref(false)

const authHeader = () => ({
    Authorization: `Bearer ${localStorage.getItem('access_token')}`
})

const fetchFriends = async () => {
    try {
        const res = await axios.get('http://127.0.0.1:8000/api/accounts/friends/', {
        headers: authHeader()
        })
        friends.value = res.data
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
        const res = await axios.get('http://127.0.0.1:8000/api/accounts/search/', {
        headers: authHeader(),
        params: { q: searchQuery.value }
        })
        searchResults.value = res.data
    } catch (error) {
        console.error(error)
    } finally {
        isSearching.value = false
    }
}

const isFriend = (userId) => {
    return friends.value.some(f => f.id === userId)
}

const toggleFriend = async (user) => {
    try {
        await axios.post(
        `http://127.0.0.1:8000/api/accounts/friends/${user.id}/`,
        {},
        { headers: authHeader() }
        )
        // 友達一覧を再取得
        fetchFriends()
    } catch (error) {
        console.error(error)
    }
}

onMounted(() => {
    fetchFriends()
})
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
</style>