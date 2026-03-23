import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Home from '../views/Home.vue'
import Friends from '../views/Friends.vue'
import Settings from '../views/Settings.vue'
import FriendHome from '../views/FriendHome.vue'
import ForgotPassword from '../views/ForgotPassword.vue'
import ResetPassword from '../views/ResetPassword.vue'
import SelectMonster from '../views/SelectMonster.vue'
import StudyTimer from '../views/StudyTimer.vue'


const routes = [
    { path: '/', redirect: '/login' },
    { path: '/login', name: 'Login', component: Login, meta: { guest: true } },
    { path: '/register', name: 'Register', component: Register, meta: { guest: true } },
    { path: '/home', name: 'Home', component: Home, meta: { requiresAuth: true } },
    { path: '/friends', name: 'Friends', component: Friends, meta: { requiresAuth: true } },
    { path: '/settings', name: 'Settings', component: Settings, meta: { requiresAuth: true } },
    { path: '/friends/:id', name: 'FriendHome', component: FriendHome, meta: { requiresAuth: true } },
    { path: '/forgot-password', name: 'ForgotPassword', component: ForgotPassword, meta: { guest: true } },
    { path: '/reset-password', name: 'ResetPassword', component: ResetPassword, meta: { guest: true } },
    { path: '/select-monster', name: 'SelectMonster', component: SelectMonster, meta: { requiresAuth: true } },
    { path: '/timer', name: 'StudyTimer', component: StudyTimer, meta: { requiresAuth: true } },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// ナビゲーションガード
router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('access_token')
    const monsterType = localStorage.getItem('monster_type')

    if (to.meta.requiresAuth && !token) {
        next('/login')
    } else if (to.meta.guest && token) {
        next('/home')
    } else if (token && !monsterType && to.path !== '/select-monster') {
        // ログイン済みだがモンスター未選択の場合
        if (to.meta.requiresAuth) {
        next('/select-monster')
        } else {
        next()
        }
    } else {
        next()
    }
})
export default router