<template>
  <div class="post-list">
    <div class="container">
      <h1>文章列表</h1>

      <!-- 搜索和过滤 -->
      <div class="filters">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索文章..."
          @keyup.enter="loadPosts"
          class="search-input"
        >
        <select v-model="selectedCategory" @change="loadPosts" class="category-select">
          <option value="">所有分类</option>
          <option v-for="category in categories" :key="category.id" :value="category.id">
            {{ category.name }}
          </option>
        </select>
        <button @click="loadPosts" class="filter-button">筛选</button>
      </div>

      <!-- 文章列表 -->
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else>
        <div v-for="post in posts" :key="post.id" class="post-card">
          <h2 @click="goToPost(post.id)" class="post-title">{{ post.title }}</h2>
          <p class="post-excerpt">{{ post.excerpt || '暂无摘要' }}</p>
          <div class="post-meta">
            <span>作者: {{ post.author_name }}</span>
            <span>分类: {{ post.category_name }}</span>
            <span>日期: {{ formatDate(post.created_at) }}</span>
            <span>{{ post.comment_count }} 评论</span>
          </div>
        </div>

        <div v-if="posts.length === 0" class="no-posts">
          暂无文章
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { blogAPI } from '@/services/api'

const router = useRouter()
const route = useRoute()

const posts = ref([])
const categories = ref([])
const loading = ref(false)
const searchQuery = ref('')
const selectedCategory = ref('')

onMounted(async () => {
  await loadCategories()
  await loadPosts()
})

// 监听路由参数变化
watch(() => route.query, () => {
  // 从URL参数更新筛选条件
  searchQuery.value = route.query.search || ''
  selectedCategory.value = route.query.category || ''
  loadPosts()
})

const loadPosts = async () => {
  loading.value = true
  try {
    // 更新URL参数
    const query = {}
    if (searchQuery.value) query.search = searchQuery.value
    if (selectedCategory.value) query.category = selectedCategory.value

    router.push({ query })

    // 获取文章列表
    const response = await blogAPI.searchPosts(searchQuery.value, selectedCategory.value)
    posts.value = response.data
  } catch (error) {
    console.error('加载文章失败:', error)
  } finally {
    loading.value = false
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

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('zh-CN')
}
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  align-items: center;
}

.search-input {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.category-select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.filter-button {
  padding: 0.5rem 1rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.post-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s;
}

.post-card:hover {
  transform: translateY(-2px);
}

.post-title {
  color: #333;
  margin-bottom: 0.5rem;
}

.post-excerpt {
  color: #666;
  margin-bottom: 1rem;
}

.post-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.8rem;
  color: #888;
}

.loading, .no-posts {
  text-align: center;
  padding: 2rem;
  color: #666;
}
</style>