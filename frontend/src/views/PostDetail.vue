<template>
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
                  placeholder="昵称"
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
              <div class="comment-content" v-html="formatCommentContent(comment.content)"></div>
            </div>

            <!-- 安全地检查评论长度 -->
            <div v-if="safeComments.length === 0" class="no-comments">
              暂无评论，快来抢沙发吧！
            </div>
          </div>
        </section>

        <!-- 导航按钮 - 移到文章下方居中 -->
        <div class="navigation-buttons-bottom">
          <button @click="goBack" class="btn btn-filter">返回</button>
          <button @click="goToHome" class="btn btn-secondary">返回首页</button>
        </div>
      </div>

      <!-- 文章不存在 -->
      <div v-else class="error">
        <h2>文章不存在[404]</h2>
        <p>您访问的文章可能已被删除或不存在。</p>
        <router-link to="/Home" class="btn btn-primary">返回首页</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { blogAPI } from '@/services/api'
import { safeMarkdownToHtml } from '@/utils/markdown'

// 响应式数据
const loading = ref(true)
const post = ref(null)
const comments = ref([])
const submittingComment = ref(false)

const commentForm = ref({
  author_name: '',
  content: ''
})

const route = useRoute()
const router = useRouter()

// 计算属性
const isAuthor = computed(() => {
  // 这里需要根据实际认证逻辑实现
  return false
})

const safeComments = computed(() => {
  return Array.isArray(comments.value) ? comments.value : []
})

const safeCommentCount = computed(() => {
  return safeComments.value.length
})

// 方法
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
  // 使用安全的Markdown解析
  return safeMarkdownToHtml(content)
}

const formatCommentContent = (content) => {
  if (!content) return ''
  // 使用安全的Markdown解析评论内容
  return safeMarkdownToHtml(content)
}

const loadPost = async () => {
  try {
    loading.value = true
    const postId = route.params.id
    if (postId) {
      const response = await blogAPI.getPost(postId)
      post.value = response.data
      await loadComments(postId)
    }
  } catch (error) {
    console.error('加载文章失败:', error)
    post.value = null
  } finally {
    loading.value = false
  }
}

const loadComments = async (postId) => {
  try {
    const response = await blogAPI.getComments({ post: postId })
    comments.value = response.data || []
  } catch (error) {
    console.error('加载评论失败:', error)
    comments.value = []
  }
}

const submitComment = async () => {
  if (!commentForm.value.author_name || !commentForm.value.content) {
    return
  }

  try {
    submittingComment.value = true
    await blogAPI.addCommentToPost(route.params.id, commentForm.value)
    // 重新加载评论
    await loadComments(route.params.id)
    // 清空表单
    commentForm.value = {
      author_name: '',
      content: ''
    }
  } catch (error) {
    console.error('提交评论失败:', error)
  } finally {
    submittingComment.value = false
  }
}

const editPost = () => {
  if (post.value) {
    router.push(`/post/edit/${post.value.id}`)
  }
}

const deletePost = async () => {
  if (!post.value) return
  
  if (confirm('确定要删除这篇文章吗？此操作不可撤销。')) {
    try {
      await blogAPI.deletePost(post.value.id)
      // 删除成功后跳转到首页
      router.push('/home')
    } catch (error) {
      console.error('删除文章失败:', error)
    }
  }
}

const goBack = () => {
  router.back()
}

const goToHome = () => {
  router.push('/home')
}

// 生命周期
onMounted(() => {
  loadPost()
})
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

/* 导航按钮样式 - 底部居中 */
.navigation-buttons-bottom {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid #eee;
}

/* 返回按钮使用filter-button颜色 */
.btn-filter {
  padding: 0.5rem 1rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  font-size: 0.9rem;
}

.btn-filter:hover {
  background: #5a6fd8;
  transform: translateY(-1px);
}

/* 返回首页按钮保持原有样式 */
.btn-secondary {
  padding: 0.5rem 1rem;
  background: #6c757d;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  font-size: 0.9rem;
}

.btn-secondary:hover {
  background: #5a6268;
  transform: translateY(-1px);
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

/* 添加Markdown内容样式 */
.content :deep(h1) {
  font-size: 2.2rem;
  font-weight: bold;
  margin: 2rem 0 1rem;
  color: #333;
  border-bottom: 2px solid #667eea;
  padding-bottom: 0.5rem;
}

.content :deep(h2) {
  font-size: 1.8rem;
  font-weight: bold;
  margin: 1.8rem 0 0.8rem;
  color: #444;
  border-bottom: 1px solid #ddd;
  padding-bottom: 0.3rem;
}

.content :deep(h3) {
  font-size: 1.5rem;
  font-weight: bold;
  margin: 1.5rem 0 0.5rem;
  color: #555;
}

.content :deep(p) {
  margin-bottom: 1rem;
}

.content :deep(blockquote) {
  border-left: 4px solid #667eea;
  background: #f8f9fa;
  padding: 1rem 1.5rem;
  margin: 1rem 0;
  font-style: italic;
  color: #666;
}

.content :deep(code) {
  background: #f1f3f4;
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  font-size: 0.9em;
}

.content :deep(pre) {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 6px;
  overflow-x: auto;
  margin: 1rem 0;
}

.content :deep(pre code) {
  background: none;
  padding: 0;
}

.content :deep(ul), .content :deep(ol) {
  margin: 1rem 0;
  padding-left: 2rem;
}

.content :deep(li) {
  margin-bottom: 0.5rem;
}

.content :deep(a) {
  color: #667eea;
  text-decoration: none;
}

.content :deep(a:hover) {
  text-decoration: underline;
}

.content :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
}

.content :deep(th), .content :deep(td) {
  border: 1px solid #ddd;
  padding: 0.75rem;
  text-align: left;
}

.content :deep(th) {
  background: #f8f9fa;
  font-weight: bold;
}

.content :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
  margin: 1rem 0;
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
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #f0f0f0;
}

.comment-author {
  font-weight: bold;
  color: #333;
}

.comment-date {
  color: #666;
  font-size: 0.9rem;
}

.comment-content {
  line-height: 1.6;
  color: #444;
}

/* 评论内容的Markdown样式 */
.comment-content :deep(h1),
.comment-content :deep(h2),
.comment-content :deep(h3) {
  font-size: 1.2rem;
  font-weight: bold;
  margin: 0.8rem 0 0.5rem;
  color: #333;
}

.comment-content :deep(h1) {
  font-size: 1.4rem;
  border-bottom: 1px solid #ddd;
  padding-bottom: 0.3rem;
}

.comment-content :deep(p) {
  margin-bottom: 0.8rem;
}

.comment-content :deep(blockquote) {
  border-left: 3px solid #667eea;
  background: #f8f9fa;
  padding: 0.8rem 1rem;
  margin: 0.8rem 0;
  font-style: italic;
  color: #666;
  font-size: 0.9rem;
}

.comment-content :deep(code) {
  background: #f1f3f4;
  padding: 0.1rem 0.3rem;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  font-size: 0.85em;
}

.comment-content :deep(pre) {
  background: #f8f9fa;
  padding: 0.8rem;
  border-radius: 4px;
  overflow-x: auto;
  margin: 0.8rem 0;
  font-size: 0.85rem;
}

.comment-content :deep(pre code) {
  background: none;
  padding: 0;
}

.comment-content :deep(ul),
.comment-content :deep(ol) {
  margin: 0.8rem 0;
  padding-left: 1.5rem;
}

.comment-content :deep(li) {
  margin-bottom: 0.3rem;
}

.comment-content :deep(a) {
  color: #667eea;
  text-decoration: none;
  font-size: 0.9rem;
}

.comment-content :deep(a:hover) {
  text-decoration: underline;
}

.comment-content :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
  margin: 0.5rem 0;
}

.error {
  text-align: center;
  padding: 3rem;
}
.error h2 {
  color: #dc3545;
  margin-bottom: 1rem;
}

.error p {
  margin-bottom: 2rem;
}

.error .btn {
  margin-top: 1.5rem;
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