<template>
    <div class="admin-shell">
        <aside class="sidebar">
            <div class="brand">
                <span class="brand-mark">MST</span>
                <span class="brand-text">管理画面</span>
            </div>

            <nav class="nav" v-if="hasAccess">
                <router-link to="/admin-dashboard/trainees" class="nav-item">受講生一覧</router-link>
                <router-link to="/admin-dashboard/progress" class="nav-item">進捗管理</router-link>
                <router-link to="/admin-dashboard/register" class="nav-item">受講生・メンバー登録</router-link>
                <router-link to="/admin-dashboard/curriculum" class="nav-item">カリキュラム管理</router-link>
            </nav>

            <div class="sidebar-footer">
                <div class="user-role" v-if="currentUser">
                    <div class="user-name">{{ currentUser.username }}</div>
                    <div class="role-badge" :class="`role-${currentUser.role}`">{{ roleLabel }}</div>
                </div>
                <router-link to="/home" class="back-link">← 受講生アプリへ戻る</router-link>
            </div>
        </aside>

        <main class="content">
            <div v-if="isLoading" class="state-message">読み込み中...</div>
            <div v-else-if="!hasAccess" class="state-message error">
                <p class="state-title">アクセス権がありません</p>
                <p>この管理画面は講師（instructor）または管理者（admin）のみ利用できます。</p>
                <router-link to="/home" class="back-link-inline">受講生アプリへ戻る</router-link>
            </div>
            <router-view v-else />
        </main>
    </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useAdminUser, loadCurrentUser } from './useAdminUser.js'

const { currentUser, isLoading } = useAdminUser()

const hasAccess = computed(() => {
    return currentUser.value && ['instructor', 'admin'].includes(currentUser.value.role)
})

const roleLabel = computed(() => {
    if (!currentUser.value) return ''
    return currentUser.value.role === 'admin' ? '管理者' : '講師'
})

onMounted(() => {
    if (!currentUser.value) {
        loadCurrentUser()
    }
})
</script>

<style scoped>
.admin-shell {
    display: flex;
    min-height: 100vh;
    background: #f8faff;
}

.sidebar {
    width: 240px;
    flex-shrink: 0;
    background: #0f172a;
    color: #e2e8f0;
    display: flex;
    flex-direction: column;
    position: sticky;
    top: 0;
    height: 100vh;
}

.brand {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 22px 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.brand-mark {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    background: #2563eb;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.5px;
}

.brand-text {
    font-size: 14px;
    font-weight: 700;
    color: white;
}

.nav {
    flex: 1;
    padding: 16px 12px;
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.nav-item {
    display: block;
    padding: 11px 14px;
    border-radius: 8px;
    color: #cbd5e1;
    text-decoration: none;
    font-size: 14px;
    font-weight: 600;
    transition: background 0.15s, color 0.15s;
}

.nav-item:hover {
    background: rgba(255, 255, 255, 0.06);
    color: white;
}

.nav-item.router-link-active {
    background: #2563eb;
    color: white;
}

.sidebar-footer {
    padding: 16px 20px 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.user-name {
    font-size: 13px;
    font-weight: 700;
    color: white;
}

.role-badge {
    display: inline-block;
    margin-top: 4px;
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 11px;
    font-weight: 700;
}

.role-badge.role-admin {
    background: #7c3aed;
    color: white;
}

.role-badge.role-instructor {
    background: #0891b2;
    color: white;
}

.back-link {
    display: block;
    margin-top: 14px;
    color: #94a3b8;
    font-size: 12px;
    text-decoration: none;
}

.back-link:hover {
    color: white;
}

.content {
    flex: 1;
    padding: 32px 40px;
    max-width: 1200px;
}

.state-message {
    padding: 60px 20px;
    text-align: center;
    color: #64748b;
    font-size: 14px;
}

.state-message.error {
    color: #b91c1c;
}

.state-title {
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 8px;
}

.back-link-inline {
    display: inline-block;
    margin-top: 16px;
    color: #2563eb;
    font-weight: 600;
    text-decoration: none;
}
</style>
