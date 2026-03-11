import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Home from '../views/Home.vue'
import Friends from '../views/Friends.vue'
import Settings from '../views/Settings.vue'

const routes = [
    { path:'/',redirect: '/login'},
    { path: '/login',name: 'login',component: Login},
    { path: '/register',name: 'Register',component: Register},
    { path: '/home', name: 'Home', component: Home },
    { path: '/friends', name: 'Friends', component: Friends },
    { path: '/settings', name: 'Settings', component: Settings },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router