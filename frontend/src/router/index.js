import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Home from '../views/Home.vue'
import Friends from '../views/Friends.vue'
import Settings from '../views/Settings.vue'
import FriendHome from '../views/FriendHome.vue'

const routes = [
    { path: '/', redirect: '/login' },
    { path: '/login', name: 'Login', component: Login, meta: { guest: true } },
    { path: '/register', name: 'Register', component: Register, meta: { guest: true } },
    { path: '/home', name: 'Home', component: Home, meta: { requiresAuth: true } },
    { path: '/friends', name: 'Friends', component: Friends, meta: { requiresAuth: true } },
    { path: '/settings', name: 'Settings', component: Settings, meta: { requiresAuth: true } },
    { path: '/friends/:id', name: 'FriendHome', component: FriendHome, meta: { requiresAuth: true } },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// ナビゲーションガード
router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('access_token')

    if (to.meta.requiresAuth && !token) {
        // ログインが必要なページにトークンなしでアクセス → ログイン画面へ
        next('/login')
    } else if (to.meta.guest && token) {
        // ログイン済みなのにログイン画面にアクセス → ホームへ
        next('/home')
    } else {
        next()
    }
})

export default router