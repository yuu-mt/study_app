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
import StudyLog from '../views/StudyLog.vue'
import StudyReview from '../views/StudyReview.vue'
import AdminLayout from '../admin-dashboard/AdminLayout.vue'
import AdminTraineeList from '../admin-dashboard/views/TraineeList.vue'
import AdminProgressManagement from '../admin-dashboard/views/ProgressManagement.vue'
import AdminTraineeDetail from '../admin-dashboard/views/TraineeDetail.vue'
import AdminRegisterView from '../admin-dashboard/views/RegisterView.vue'
import AdminCurriculumManagement from '../admin-dashboard/views/CurriculumManagement.vue'


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
    { path: '/review', name: 'StudyReview', component: StudyReview, meta: { requiresAuth: true } },
    { path: '/study-log', name: 'StudyLog', component: StudyLog, meta: { requiresAuth: true } },
    {
        path: '/admin-dashboard',
        component: AdminLayout,
        meta: { requiresAuth: true },
        children: [
            { path: '', redirect: '/admin-dashboard/trainees' },
            { path: 'trainees', name: 'AdminTraineeList', component: AdminTraineeList },
            { path: 'progress', name: 'AdminProgressManagement', component: AdminProgressManagement },
            { path: 'register', name: 'AdminRegisterView', component: AdminRegisterView },
            { path: 'trainees/:id', name: 'AdminTraineeDetail', component: AdminTraineeDetail },
            { path: 'curriculum', name: 'AdminCurriculumManagement', component: AdminCurriculumManagement },
        ],
    },
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