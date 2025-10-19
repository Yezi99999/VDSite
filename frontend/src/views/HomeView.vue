<template>
  <div class="home">
    <!-- 英雄区域 -->
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">欢迎来到我的博客</h1>
        <p class="hero-subtitle">分享技术、生活和思考</p>
        <div class="hero-stats">
          <div class="stat-item">
            <span class="stat-number">{{ stats.total_posts }}</span>
            <span class="stat-label">篇文章</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">{{ stats.total_categories }}</span>
            <span class="stat-label">个分类</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">{{ stats.total_comments }}</span>
            <span class="stat-label">条评论</span>
          </div>
        </div>
      </div>
      <div class="hero-info">
          <div class="image-container">
            <img
              src="../assets/images/avatar.png"
              alt="叶子"
              class="profile-image"
            />
          </div>
        <p class="hero-description">
          喜欢通过双手来实现想要的效果，这里记录了我的技术成长和生活经历。
        </p>
      </div>
    </section>

    <!-- 主要内容区域 -->
    <div class="container">
      <div class="home-layout">
        <!-- 左侧内容 -->
        <main class="main-content">
          <!-- 推荐文章 -->
          <section class="featured-section">
            <h2 class="section-title">推荐文章</h2>
            <div class="featured-posts">
              <div
                v-for="post in featuredPosts"
                :key="post.id"
                class="featured-post-card"
                @click="goToPost(post.id)"
              >
                <div class="featured-post-content">
                  <h3 class="post-title">{{ post.title }}</h3>
                  <p class="post-excerpt">{{ post.excerpt || '暂无摘要' }}</p>
                  <div class="post-meta">
                    <span class="category">{{ post.category_name }}</span>
                    <span class="date">{{ formatDate(post.created_at) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <!-- 最新文章 -->
          <section class="recent-section">
            <div class="section-header">
              <h2 class="section-title">最新文章</h2>
              <div class="view-all" @click="goToPosts">查看全部 →</div>
            </div>
            <div class="recent-posts">
              <div
                v-for="post in recentPosts"
                :key="post.id"
                class="recent-post-card"
              >
                <div class="post-info">
                  <h3 class="post-title" @click="goToPost(post.id)">
                    {{ post.title }}
                  </h3>
                  <p class="post-excerpt">{{ post.excerpt || '暂无摘要' }}</p>
                  <div class="post-meta">
                    <span class="author">作者: {{ post.author_name }}</span>
                    <span class="category">{{ post.category_name }}</span>
                    <span class="date">{{ formatDate(post.created_at) }}</span>
                    <span class="comments">{{ post.comment_count }} 评论</span>
                  </div>
                </div>
              </div>
            </div>
          </section>
        </main>

        <!-- 侧边栏 -->
        <aside class="sidebar">
          <!-- 搜索框 -->
          <div class="sidebar-widget">
            <h3>搜索文章</h3>
            <div class="search-box">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="输入关键词..."
                @keyup.enter="performSearch"
                class="search-input"
              >
              <button @click="performSearch" class="search-button">搜索</button>
            </div>
          </div>

          <!-- 分类 -->
          <div class="sidebar-widget">
            <h3>文章分类</h3>
            <div class="categories">
              <div
                v-for="category in categories"
                :key="category.id"
                class="category-item"
                @click="filterByCategory(category.id)"
              >
                <span class="category-name">{{ category.name }}</span>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { blogAPI } from '@/services/api'

const router = useRouter()

// 响应式数据
const stats = ref({
  total_posts: 0,
  total_categories: 0,
  total_comments: 0,
  recent_posts: []
})
const featuredPosts = ref([])
const recentPosts = ref([])
const categories = ref([])
const searchQuery = ref('')

// 生命周期
onMounted(async () => {
  await loadHomeData()
  await loadCategories()
})

// 方法
const loadHomeData = async () => {
  try {
    // 加载主页统计数据
    const statsResponse = await blogAPI.getHomeStats()
    stats.value = statsResponse.data
    recentPosts.value = statsResponse.data.recent_posts

    // 加载推荐文章
    const featuredResponse = await blogAPI.getFeaturedPosts()
    featuredPosts.value = featuredResponse.data
  } catch (error) {
    console.error('加载主页数据失败:', error)
  }
}

const loadCategories = async () => {
  try {
    const response = await blogAPI.getCategories()
    categories.value = response.data
  } catch (error) {
    console.error('加载分类失败:', error)
  }
}

const goToPost = (id) => {
  router.push(`/post/${id}`)
}

const goToPosts = () => {
  router.push('/posts')
}

const performSearch = () => {
  if (searchQuery.value.trim()) {
    router.push(`/posts?search=${encodeURIComponent(searchQuery.value)}`)
  }
}

const filterByCategory = (categoryId) => {
  router.push(`/posts?category=${categoryId}`)
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<style scoped>
.home {
  min-height: 100vh;
}

/* 英雄区域样式 */
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 80px 0;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
}

.hero-content {
  flex: 1;
  padding: 0 40px;
  text-align: right;
}
.profile-image {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  margin-bottom: 1rem;
}
.hero-info {
  flex: 1;
  padding: 0 40px;
  text-align: left;
  border-left: 1px solid rgba(255, 255, 255, 0.3);
}

.hero-title {
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.hero-subtitle {
  font-size: 1.2rem;
  opacity: 0.9;
  margin-bottom: 2rem;
}

.hero-stats {
  display: flex;
  gap: 3rem;
  margin-top: 2rem;
  justify-content: right;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: bold;
}

.stat-label {
  font-size: 0.9rem;
  opacity: 0.8;
}

.hero-description {
  font-size: 1.1rem;
  line-height: 1.6;
  opacity: 0.9;
}

/* 布局 */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.home-layout {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 3rem;
  padding: 3rem 0;
}

/* 章节样式 */
.section-title {
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
  color: #333;
  border-left: 4px solid #667eea;
  padding-left: 1rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.view-all {
  color: #667eea;
  cursor: pointer;
  font-weight: 500;
}

.view-all:hover {
  text-decoration: underline;
}

/* 文章卡片样式 */
.featured-posts {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.featured-post-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.featured-post-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
}

.recent-post-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  border: 1px solid #eaeaea;
  transition: box-shadow 0.3s ease;
}

.recent-post-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.post-title {
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #333;
  cursor: pointer;
}

.post-title:hover {
  color: #667eea;
}

.post-excerpt {
  color: #666;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.post-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.85rem;
  color: #888;
}

.post-meta span {
  padding: 0.2rem 0.5rem;
  background: #f5f5f5;
  border-radius: 4px;
}

/* 侧边栏样式 */
.sidebar-widget {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  border: 1px solid #eaeaea;
}

.sidebar-widget h3 {
  margin-bottom: 1rem;
  color: #333;
  font-size: 1.2rem;
}

.search-box {
  display: flex;
  gap: 0.5rem;
}

.search-input {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  outline: none;
}

.search-input:focus {
  border-color: #667eea;
}

.search-button {
  padding: 0.5rem 1rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.search-button:hover {
  background: #5a6fd8;
}

.category-item {
  padding: 0.5rem 0;
  cursor: pointer;
  transition: color 0.3s ease;
}

.category-item:hover {
  color: #667eea;
}

.category-name {
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .home-layout {
    grid-template-columns: 1fr;
  }

  .hero-section {
    flex-direction: column;
    text-align: center;
    padding: 60px 0;
  }

  .hero-content {
    padding: 0 20px;
    text-align: center;
  }

  .hero-info {
    padding: 40px 20px 0 20px;
    text-align: center;
    border-left: none;
    border-top: 1px solid rgba(255, 255, 255, 0.3);
  }

  .hero-title {
    font-size: 2rem;
  }

  .hero-stats {
    justify-content: center;
    gap: 1.5rem;
  }

  .stat-item {
    align-items: center;
  }

  .stat-number {
    font-size: 2rem;
  }

  .featured-posts {
    grid-template-columns: 1fr;
  }

  .post-meta {
    flex-wrap: wrap;
    gap: 0.5rem;
  }
}
</style>