import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index.js'
import './style.css'

const app = createApp(App)
app.use(router)
app.mount('#app')

// Service Worker登録
if ('serviceWorker' in navigator && import.meta.env.PROD) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
        .then(reg => console.log('SW registered:', reg))
        .catch(err => console.log('SW error:', err))
    })
} else if ('serviceWorker' in navigator) {
    navigator.serviceWorker.getRegistrations()
        .then(registrations => {
            registrations.forEach(registration => registration.unregister())
        })
        .catch(err => console.log('SW unregister error:', err))
}
