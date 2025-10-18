<template>
  <div class="intro-container">
    <div class="intro-content">
      <h1>欢迎来到 VDSite</h1>
      <p class="intro-subtitle">一个简洁优雅的博客平台</p>
      
      <div class="features">
        <div class="feature-card">
          <h3>📝 文章发布</h3>
          <p>登录后即可发布和管理您的文章</p>
        </div>
        <div class="feature-card">
          <h3>💬 评论互动</h3>
          <p>与读者进行友好的交流互动</p>
        </div>
        <div class="feature-card">
          <h3>📊 数据统计</h3>
          <p>实时查看博客的访问数据</p>
        </div>
      </div>

      <div class="auth-section">
        <h2>开始使用</h2>
        <p>选择您的访问方式</p>
        <div class="button-group">
          <button @click="goToHome" class="guest-btn">访客浏览</button>
          <button @click="goToLogin" class="login-btn">登录账号</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goToLogin = () => {
  router.push('/login')
}

const goToHome = () => {
  // 直接跳转到首页，不经过路由守卫的认证检查
  router.push('/home')
}
</script>

<style scoped>
.intro-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.intro-content {
  text-align: center;
  max-width: 800px;
}

.intro-content h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  font-weight: bold;
}

.intro-subtitle {
  font-size: 1.3rem;
  opacity: 0.9;
  margin-bottom: 3rem;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin: 3rem 0;
}

.feature-card {
  background: rgba(255, 255, 255, 0.1);
  padding: 2rem;
  border-radius: 12px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.feature-card h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.feature-card p {
  opacity: 0.9;
  line-height: 1.6;
}

.auth-section {
  margin-top: 3rem;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.auth-section h2 {
  margin-bottom: 1rem;
}

.auth-section p {
  margin-bottom: 1.5rem;
  opacity: 0.9;
}

.button-group {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.login-btn {
  background: white;
  color: #667eea;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 6px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  transition: transform 0.3s;
}

.guest-btn {
  background: transparent;
  color: white;
  border: 2px solid white;
  padding: 0.75rem 2rem;
  border-radius: 6px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
}

.login-btn:hover {
  transform: translateY(-2px);
}

.guest-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .intro-content h1 {
    font-size: 2rem;
  }
  
  .features {
    grid-template-columns: 1fr;
  }
  
  .button-group {
    flex-direction: column;
  }
}
</style>