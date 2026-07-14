import { ref } from 'vue'
import api from '../api.js'

const currentUser = ref(null)
const isLoading = ref(true)
const loadError = ref(null)

export async function loadCurrentUser() {
    isLoading.value = true
    loadError.value = null
    try {
        const res = await api.get('/accounts/me/')
        currentUser.value = res.data
    } catch (error) {
        loadError.value = error
    } finally {
        isLoading.value = false
    }
}

export function useAdminUser() {
    return { currentUser, isLoading, loadError, loadCurrentUser }
}
