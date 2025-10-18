<template>
  <div class="navigation-buttons">
    <button @click="goBack" class="btn btn-secondary">返回</button>
    <button @click="goToHome" class="btn btn-secondary">返回首页</button>
  </div>
  <div class="post-detail">
    <div class="container">
      <!-- 加载状态 -->
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>加载中...</p>
      </div>

      <!-- 文章内容 -->
      <div v-else-if="post" class="post-content">
        <!-- 文章头部 -->
        <header class="post-header">
          <h1 class="post-title">{{ post.title }}</h1>
          <div class="post-meta">
            <span class="author">作者: {{ post.author_name || '未知' }}</span>
            <span class="category">分类: {{ post.category_name || '未分类' }}</span>
            <span class="date">发布时间: {{ formatDate(post.created_at) }}</span>
            <span v-if="post.updated_at !== post.created_at" class="update-date">
              更新于: {{ formatDate(post.updated_at) }}
            </span>
          </div>
        </header>

        <!-- 文章正文 -->
        <article class="post-body">
          <div class="content" v-html="formatContent(post.content)"></div>
        </article>

        <!-- 文章操作 -->
        <div class="post-actions" v-if="isAuthor">
          <button @click="editPost" class="btn btn-edit">编辑文章</button>
          <button @click="deletePost" class="btn btn-delete">删除文章</button>
        </div>

        <!-- 评论区域 -->
        <section class="comments-section">
          <h2 class="comments-title">
            评论 ({{ safeCommentCount }})
          </h2>

          <!-- 评论表单 -->
          <div class="comment-form">
            <h3>发表评论</h3>
            <form @submit.prevent="submitComment">
              <div class="form-group">
                <input
                  v-model="commentForm.author_name"
                  type="text"
                  placeholder="您的姓名"
                  required
                  class="form-input"
                >
              </div>
              <div class="form-group">
                <textarea
                  v-model="commentForm.content"
                  placeholder="请输入评论内容..."
                  required
                  rows="4"
                  class="form-textarea"
                ></textarea>
              </div>
              <button type="submit" class="btn btn-primary" :disabled="submittingComment">
                {{ submittingComment ? '提交中...' : '发表评论' }}
              </button>
            </form>
          </div>

          <!-- 评论列表 -->
          <div class="comments-list">
            <!-- 使用计算属性确保 comments 存在 -->
            <div
              v-for="comment in safeComments"
              :key="comment.id"
              class="comment-item"
            >
              <div class="comment-header">
                <span class="comment-author">{{ comment.author_name }}</span>
                <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
              </div>
              <div class="comment-content">
                {{ comment.content }}
              </div>
            </div>

            <!-- 安全地检查评论长度 -->
            <div v-if="safeComments.length === 0" class="no-comments">
              暂无评论，快来抢沙发吧！
            </div>
          </div>
        </section>
      </div>

      <!-- 文章不存在 -->
      <div v-else class="error">
        <h2>文章不存在</h2>
        <p>您访问的文章可能已被删除或不存在。</p>
        <router-link to="/" class="btn btn-primary">返回首页</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { blogAPI } from '@/services/api'

const route = useRoute()
const router = useRouter()

const post = ref(null)
const comments = ref([])
const loading = ref(true)
const submittingComment = ref(false)

const commentForm = ref({
  author_name: '',
  content: ''
})

// 计算属性
const safeComments = computed(() => {
  return comments.value || []
})

const safeCommentCount = computed(() => {
  return comments.value?.length || 0
})

const isAuthor = computed(() => {
  // 简单的作者检查逻辑，可以根据实际需求调整
  return post.value?.author_name === '当前用户' // 这里需要根据实际用户系统调整
})

// 导航函数
const goBack = () => {
  router.back()
}

const goToHome = () => {
  router.push('/')
}

const editPost = () => {
  if (post.value?.id) {
    router.push(`/edit/${post.value.id}`)
  }
}

const deletePost = async () => {
  if (confirm('确定要删除这篇文章吗？')) {
    try {
      await blogAPI.deletePost(post.value.id)
      alert('文章删除成功')
      router.push('/')
    } catch (error) {
      console.error('删除文章失败:', error)
      alert('删除文章失败，请重试')
    }
  }
}

// 辅助函数
const formatDate = (dateString) => {
  if (!dateString) return '未知时间'
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatContent = (content) => {
  if (!content) return ''
  // 简单的HTML转义和换行处理
  return content
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;')
    .replace(/\n/g, '<br>')
}

onMounted(async () => {
  await loadPost()
  await loadComments()
})

const loadPost = async () => {
  try {
    const response = await blogAPI.getPost(route.params.id)
    post.value = response.data
  } catch (error) {
    console.error('加载文章失败:', error)
    post.value = {
      title: '文章加载失败',
      content: '无法加载文章内容',
      author_name: '未知',
      category_name: '未知',
      created_at: new Date().toISOString()
    }
  }
}

const loadComments = async () => {
  try {
    // 修复：使用正确的API方法，通过参数过滤特定文章的评论
    const response = await blogAPI.getComments({ post: route.params.id })
    comments.value = response.data
  } catch (error) {
    console.error('加载评论失败:', error)
    comments.value = []
  } finally {
    loading.value = false
  }
}

const submitComment = async () => {
  if (!commentForm.value.author_name.trim() || !commentForm.value.content.trim()) {
    alert('请填写姓名和评论内容')
    return
  }

  submittingComment.value = true
  try {
    await blogAPI.addCommentToPost(post.value.id, {
      author_name: commentForm.value.author_name,
      content: commentForm.value.content
    })

    commentForm.value = { author_name: '', content: '' }
    await loadComments()
    alert('评论提交成功！等待管理员审核后显示。')
  } catch (error) {
    console.error('提交评论失败:', error)
    alert(`提交评论失败: ${error.response?.data?.message || '请重试'}`)
  } finally {
    submittingComment.value = false
  }
}
</script>

<style scoped>
/* 导航栏样式 */
.navigation-buttons {
  background: #f8f9fa;
  padding: 1rem 2rem;
  border-bottom: 1px solid #eaeaea;
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.navigation-buttons .btn {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  background: white;
  color: #333;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.navigation-buttons .btn:hover {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

.navigation-buttons .btn-secondary {
  background: #6c757d;
  color: white;
  border-color: #6c757d;
}

.navigation-buttons .btn-secondary:hover {
  background: #5a6268;
  border-color: #545b62;
}

/* 保持之前的样式不变 */
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.loading {
  text-align: center;
  padding: 3rem;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 2s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.post-header {
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eaeaea;
}

.post-title {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 1rem;
  color: #333;
  line-height: 1.2;
}

.post-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  color: #666;
  font-size: 0.9rem;
}

.post-body {
  margin-bottom: 3rem;
}

.content {
  line-height: 1.8;
  font-size: 1.1rem;
  color: #333;
}

.content :deep(br) {
  margin-bottom: 1rem;
}

.post-actions {
  display: flex;
  gap: 1rem;
  margin-bottom: 3rem;
  padding: 1rem 0;
  border-top: 1px solid #eaeaea;
  border-bottom: 1px solid #eaeaea;
}

.comments-section {
  border-top: 2px solid #eaeaea;
  padding-top: 2rem;
}

.comments-title {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  color: #333;
}

.comment-form {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.comment-form h3 {
  margin-bottom: 1rem;
  color: #333;
}

.form-group {
  margin-bottom: 1rem;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #667eea;
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.btn-primary {
  background: #667eea;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #5a6fd8;
}

.btn-primary:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.btn-edit {
  background: #28a745;
  color: white;
}

.btn-edit:hover {
  background: #218838;
}

.btn-delete {
  background: #dc3545;
  color: white;
}

.btn-delete:hover {
  background: #c82333;
}

.comments-list {
  space-y: 1rem;
}

.comment-item {
  background: white;
  border: 1px solid #eaeaea;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1rem;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.comment-author {
  font-weight: bold;
  color: #333;
}

.comment-date {
  color: #666;
  font-size: 0.85rem;
}

.comment-content {
  line-height: 1.6;
  color: #333;
}

.no-comments {
  text-align: center;
  padding: 2rem;
  color: #666;
  font-style: italic;
}

.error {
  text-align: center;
  padding: 3rem;
}

.error h2 {
  color: #dc3545;
  margin-bottom: 1rem;
}

@media (max-width: 768px) {
  .navigation-buttons {
    padding: 1rem;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .post-title {
    font-size: 2rem;
  }

  .post-meta {
    flex-direction: column;
    gap: 0.5rem;
  }

  .post-actions {
    flex-direction: column;
  }

  .comment-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
}
</style>