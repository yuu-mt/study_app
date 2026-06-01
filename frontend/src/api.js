import axios from 'axios'
import router from './router/index.js'

const BASE_URL = import.meta.env.VITE_API_URL || 'https://monster-study-tracker.fly.dev/api'
const api = axios.create({
    baseURL: BASE_URL
})

// リクエストインターセプター
// 全リクエストにアクセストークンを自動付与
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    (error) => Promise.reject(error)
)

// レスポンスインターセプター
// 401エラー時にトークンをリフレッシュ
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config

        if (error.response?.status === 401 && !originalRequest._retry){
            originalRequest._retry = true

            try{
                const refreshToken = localStorage.getItem('refresh_token')
                const res = await axios.post(`${BASE_URL}/accounts/token/refresh/`,  { refresh: refreshToken
                })

                const newAccessToken = res.data.access
                localStorage.setItem('access_token', newAccessToken)
                originalRequest.headers.Authorization = `Bearer ${newAccessToken}`

                return api(originalRequest)
            } catch (refreshError) {
                // リフレッシュも失敗したらログアウト
                localStorage.removeItem('access_token')
                localStorage.removeItem('refresh_token')
                router.push('/login')
                return Promise.reject(refreshError)
            }
        }
        return Promise.reject(error)
    }
)

export default api
export const authApi = axios.create({
    baseURL: BASE_URL,
})
