import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    name: 'Intro',
    component: () => import('../views/IntroView.vue'),
    meta: { requiresGuest: true }  // 添加meta标记，需要访客状态
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('../views/HomeView.vue')
  },
  {
    path: '/posts',
    name: 'Posts',
    component: () => import('../views/PostList.vue')
  },
  {
    path: '/post/:id',
    name: 'PostDetail',
    component: () => import('../views/PostDetail.vue')
  },
  {
    path: '/post/create',
    name: 'PostCreate',
    component: () => import('../views/PostEdit.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/post/edit/:id',
    name: 'PostEdit',
    component: () => import('../views/PostEdit.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/AboutView.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginView.vue'),
    meta: { requiresGuest: true }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// 路由守卫
let lastAuthCheck = 0
const AUTH_CHECK_INTERVAL = 5000 // 5秒内只检查一次

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // 防抖：避免频繁调用认证检查
  const now = Date.now()
  if (now - lastAuthCheck > AUTH_CHECK_INTERVAL) {
    lastAuthCheck = now
    await authStore.checkAuth()
  }
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    // 需要认证但未登录，跳转到介绍页面
    next('/')
  } else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    // 需要访客但已登录，跳转到首页
    next('/home')
  } else {
    next()
  }
})

export default router