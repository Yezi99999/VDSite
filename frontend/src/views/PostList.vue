<template>
  <div class="post-list">
    <div class="container">
      <h1>{{ pageTitle }}</h1>

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
        <button @click="loadPosts" class="filter-button">搜索</button>
      </div>

      <!-- 当前筛选条件显示 -->
      <div v-if="currentFilter" class="current-filter">
        当前筛选: {{ currentFilter }}
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
import { ref, onMounted, watch, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { blogAPI } from '@/services/api'

const router = useRouter()
const route = useRoute()

const posts = ref([])
const categories = ref([])
const loading = ref(false)
const searchQuery = ref('')
const selectedCategory = ref('')
const categoriesLoaded = ref(false)

// 计算属性 - 基于当前选择的分类而不是URL参数
const pageTitle = computed(() => {
  if (searchQuery.value) {
    return `搜索: "${searchQuery.value}"`
  } else if (selectedCategory.value) {
    if (!categoriesLoaded.value) return '文章列表'
    const category = categories.value.find(cat => cat.id == selectedCategory.value)
    return category ? `${category.name} - 文章列表` : '文章列表'
  }
  return '文章列表'
})

const currentFilter = computed(() => {
  if (searchQuery.value) {
    return `搜索关键词: "${searchQuery.value}"`
  } else if (selectedCategory.value) {
    if (!categoriesLoaded.value) return ''
    const category = categories.value.find(cat => cat.id == selectedCategory.value)
    return category ? `分类: ${category.name}` : ''
  }
  return ''
})

const loadPosts = async () => {
  loading.value = true
  try {
    // 更新URL参数以反映当前筛选条件
    const query = {}
    if (searchQuery.value) query.search = searchQuery.value
    if (selectedCategory.value) query.category = selectedCategory.value
    
    // 只有当URL参数与当前筛选条件不同时才更新URL
    if (JSON.stringify(route.query) !== JSON.stringify(query)) {
      router.push({ query })
    } else {
      // 直接获取文章列表
      const response = await blogAPI.searchPosts(searchQuery.value, selectedCategory.value)
      posts.value = response.data
    }
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
    categoriesLoaded.value = true
  } catch (error) {
    console.error('加载分类失败:', error)
  }
}

const goToPost = (id) => {
  router.push(`/post/${id}`)
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// 监听路由参数变化
watch(() => route.query, () => {
  // 从URL参数更新筛选条件
  searchQuery.value = route.query.search || ''
  selectedCategory.value = route.query.category || ''
  // 只有当URL参数与当前筛选条件不同时才加载文章
  if (route.query.search || route.query.category) {
    loadPosts()
  }
})

onMounted(async () => {
  await loadCategories()
  
  // 手动处理初始URL参数
  searchQuery.value = route.query.search || ''
  selectedCategory.value = route.query.category || ''
  
  // 加载文章
  await loadPosts()
})
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
  margin-bottom: 1rem;
  align-items: center;
}

.current-filter {
  background: #f8f9fa;
  padding: 0.75rem 1rem;
  border-radius: 4px;
  margin-bottom: 1.5rem;
  border-left: 4px solid #667eea;
  font-weight: 500;
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