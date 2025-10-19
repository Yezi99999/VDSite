<template>
  <div id="app">
    <!-- 导航栏 -->
    <nav class="navbar" v-if="showNavbar">
      <div class="nav-container">
        <router-link to="/" class="nav-logo">VDSite</router-link>
        <div class="nav-links">
          <router-link to="/home">首页</router-link>
          <router-link to="/posts">文章</router-link>
          <router-link v-if="isAuthenticated" to="/post/create">写文章</router-link>
          <router-link to="/about">关于</router-link>
          <div class="auth-section" v-if="isAuthenticated">
            <span class="user-info">欢迎, {{ user?.username }}</span>
            <button @click="handleLogout" class="logout-btn">退出</button>
          </div>
          <router-link v-else to="/login" class="login-link">登录</router-link>
        </div>
      </div>
    </nav>

    <!-- 主要内容区域 -->
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const isAuthenticated = computed(() => authStore.isAuthenticated)
const user = computed(() => authStore.user)
const showNavbar = computed(() => router.currentRoute.value.name !== 'Intro')

const handleLogout = async () => {
  await authStore.logout()
  router.push('/')
}

// 初始化认证状态
onMounted(async () => {
  await authStore.checkAuth()
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f8f9fa;
  color: #333;
}

.navbar {
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: #667eea;
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.nav-links a {
  text-decoration: none;
  color: #333;
  font-weight: 500;
  transition: color 0.3s;
  padding: 0.5rem 1rem;
  border-radius: 4px;
}

.nav-links a:hover,
.nav-links a.router-link-active {
  color: #667eea;
  background-color: #faf0ea;
}

.auth-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-info {
  color: #666;
  font-size: 0.9rem;
}

.logout-btn {
  background: #dc3545;
  color: white;
  border: none;
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
}

.logout-btn:hover {
  background: #c82333;
}

.login-link {
  background: #667eea;
  color: white !important;
}

.login-link:hover {
  background: #5a6fd8 !important;
}

main {
  min-height: calc(100vh - 80px);
  padding: unset;
}

::-webkit-scrollbar {
  display: block;
  width: 6px;
  height: 1px;
}

::-webkit-scrollbar-track {
  width: 6px;
  background: rgba(16, 31, 28, 0.1);
  -webkit-border-radius: 2em;
  -moz-border-radius: 2em;
  border-radius: 2em;
}

::-webkit-scrollbar-thumb {
  background-color: rgba(144,90,183,.5);
  background-clip: padding-box;
  min-height: 28px;
  -webkit-border-radius: 2em;
  -moz-border-radius: 2em;
  border-radius: 2em;
  transition: background-color .3s;
  cursor: pointer;
}

::-webkit-scrollbar-thumb:hover {
  background-color: rgba(144,147,153,.3);
}
::-webkit-scrollbar-button {
  display: none;
}
/* 响应式设计 */
@media (max-width: 768px) {
  .nav-container {
    padding: 0 1rem;
    flex-direction: column;
    gap: 1rem;
  }
  
  .nav-links {
    gap: 1rem;
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .nav-links a {
    padding: 0.5rem;
    font-size: 0.9rem;
  }
  
  .auth-section {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style>