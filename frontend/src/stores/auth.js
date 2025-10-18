import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { blogAPI } from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
    const user = ref(null)
    const isAuthenticated = ref(false)
    const isLoading = ref(false)

    const login = async (credentials) => {
        isLoading.value = true
        try {
            const response = await blogAPI.login(credentials)
            if (response.data.success) {
                user.value = response.data.user
                isAuthenticated.value = true
                return { success: true }
            }
        } catch (error) {
            console.error('Login failed:', error)
            return { 
                success: false, 
                error: error.response?.data?.error || '登录失败' 
            }
        } finally {
            isLoading.value = false
        }
    }

    const logout = async () => {
        try {
            await blogAPI.logout()
            user.value = null
            isAuthenticated.value = false
        } catch (error) {
            console.error('Logout failed:', error)
        }
    }

    const checkAuth = async () => {
        try {
            const response = await blogAPI.checkAuth()
            if (response.data.authenticated) {
                user.value = response.data.user
                isAuthenticated.value = true
            } else {
                user.value = null
                isAuthenticated.value = false
            }
        } catch (error) {
            console.error('Auth check failed:', error)
            user.value = null
            isAuthenticated.value = false
        }
    }

    return {
        user: computed(() => user.value),
        isAuthenticated: computed(() => isAuthenticated.value),
        isLoading: computed(() => isLoading.value),
        login,
        logout,
        checkAuth
    }
})