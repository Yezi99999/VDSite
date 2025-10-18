import { defineStore } from 'pinia'

export const usePostStore = defineStore('post', {
  state: () => ({
    posts: [],
    currentPost: null,
    loading: false
  }),

  actions: {
    async fetchPost(id) {
      this.loading = true
      try {
        const response = await blogAPI.getPost(id)
        this.currentPost = response.data
      } catch (error) {
        console.error('获取文章失败:', error)
        throw error
      } finally {
        this.loading = false
      }
    }
  }
})