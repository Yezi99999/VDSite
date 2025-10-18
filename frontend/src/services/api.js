import axios from 'axios'

// 获取CSRF token的函数
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // 检查cookie名称是否匹配
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const api = axios.create({
    baseURL: process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000/api/',
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true  // 允许发送cookie
})

// 请求拦截器 - 添加CSRF token
api.interceptors.request.use(
    config => {
        console.log(`Making ${config.method?.toUpperCase()} request to: ${config.url}`)
        
        // 对于非GET请求，添加CSRF token
        if (config.method !== 'get' && config.method !== 'GET') {
            const csrfToken = getCookie('csrftoken');
            if (csrfToken) {
                config.headers['X-CSRFToken'] = csrfToken;
            }
        }
        
        return config
    },
    error => {
        return Promise.reject(error)
    }
)

// 响应拦截器
api.interceptors.response.use(
    response => {
        return response
    },
    error => {
        console.error('API Error:', error.response?.data || error.message)
        return Promise.reject(error)
    }
)

export const blogAPI = {
    // 认证相关
    login(credentials) {
        return api.post('auth/login/', credentials)
    },

    logout() {
        return api.post('auth/logout/')
    },

    checkAuth() {
        return api.get('auth/check/')
    },

    // 主页相关
    getHomeStats() {
        return api.get('home/stats/')
    },

    getFeaturedPosts() {
        return api.get('home/featured/')
    },

    // 分类相关
    getCategories() {
        return api.get('categories/')
    },

    getCategory(id) {
        return api.get(`categories/${id}/`)
    },

    createCategory(categoryData) {
        return api.post('categories/', categoryData)
    },

    // 文章相关
    getPosts(params = {}) {
        return api.get('posts/', { params })
    },

    getPost(id) {
        return api.get(`posts/${id}/`)
    },

    createPost(postData) {
        return api.post('posts/', postData)
    },

    updatePost(id, postData) {
        return api.put(`posts/${id}/`, postData)
    },

    deletePost(id) {
        return api.delete(`posts/${id}/`)
    },
    searchPosts(query = null, category = null) {
        const params = {}
        if (query) params.search = query
        if (category) params.category = category
        return api.get('posts/', { params })
    },
    // 评论相关
    getComments(params = {}) {
        return api.get('comments/', { params })
    },

    getComment(id) {
        return api.get(`comments/${id}/`)
    },

    createComment(commentData) {
        return api.post('comments/', commentData)
    },

    updateComment(id, commentData) {
        return api.put(`comments/${id}/`, commentData)
    },

    deleteComment(id) {
        return api.delete(`comments/${id}/`)
    },

    // 为文章添加评论
    addCommentToPost(postId, commentData) {
        return api.post(`posts/${postId}/add_comment/`, commentData)
    }
}

export default api