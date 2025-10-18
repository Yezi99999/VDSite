<template>
  <div class="post-edit">
    <div class="container">
      <h1>{{ isEdit ? '编辑文章' : '创建文章' }}</h1>

      <form @submit.prevent="submitForm" class="post-form">
        <div class="form-group">
          <label for="title">文章标题 *</label>
          <input
            id="title"
            v-model="form.title"
            type="text"
            required
            class="form-input"
            placeholder="请输入文章标题"
          >
        </div>

        <div class="form-group">
          <label for="excerpt">文章摘要</label>
          <textarea
            id="excerpt"
            v-model="form.excerpt"
            rows="3"
            class="form-textarea"
            placeholder="请输入文章摘要（可选）"
          ></textarea>
        </div>

        <div class="form-group">
          <label for="category">文章分类 *</label>
          <select
            id="category"
            v-model="form.category"
            required
            class="form-select"
          >
            <option value="">请选择分类</option>
            <option
              v-for="category in categories"
              :key="category.id"
              :value="category.id"
            >
              {{ category.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="content">文章内容 *</label>
          <textarea
            id="content"
            v-model="form.content"
            rows="15"
            required
            class="form-textarea"
            placeholder="请输入文章内容..."
          ></textarea>
        </div>

        <div class="form-group">
          <label class="checkbox-label">
            <input
              type="checkbox"
              v-model="form.is_published"
              class="checkbox"
            >
            <span>立即发布</span>
          </label>
        </div>

        <div class="form-actions">
          <button
            type="submit"
            class="btn btn-primary"
            :disabled="submitting"
          >
            {{ submitting ? '提交中...' : (isEdit ? '更新文章' : '创建文章') }}
          </button>
          <button
            type="button"
            class="btn btn-secondary"
            @click="cancel"
          >
            取消
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { blogAPI } from '@/services/api'

const route = useRoute()
const router = useRouter()

// 响应式数据
const form = ref({
  title: '',
  excerpt: '',
  content: '',
  category: '',
  is_published: false
})
const categories = ref([])
const submitting = ref(false)

// 计算属性
const isEdit = computed(() => route.name === 'PostEdit')
const postId = computed(() => route.params.id)

// 生命周期
onMounted(async () => {
  await loadCategories()
  if (isEdit.value) {
    await loadPost()
  }
})

// 方法
const loadCategories = async () => {
  try {
    const response = await blogAPI.getCategories()
    categories.value = response.data
  } catch (error) {
    console.error('加载分类失败:', error)
  }
}

const loadPost = async () => {
  try {
    const response = await blogAPI.getPost(postId.value)
    const post = response.data
    form.value = {
      title: post.title,
      excerpt: post.excerpt || '',
      content: post.content,
      category: post.category,
      is_published: post.is_published
    }
  } catch (error) {
    console.error('加载文章失败:', error)
    alert('加载文章失败')
    router.push('/')
  }
}

const submitForm = async () => {
  if (!form.value.title.trim() || !form.value.content.trim() || !form.value.category) {
    alert('请填写完整信息')
    return
  }

  submitting.value = true
  try {
    if (isEdit.value) {
      await blogAPI.updatePost(postId.value, form.value)
      alert('文章更新成功！')
    } else {
      await blogAPI.createPost(form.value)
      alert('文章创建成功！')
    }
    router.push('/')
  } catch (error) {
    console.error('提交文章失败:', error)
    alert('操作失败，请重试')
  } finally {
    submitting.value = false
  }
}

const cancel = () => {
  if (confirm('确定要取消吗？未保存的更改将丢失。')) {
    router.go(-1)
  }
}
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

h1 {
  margin-bottom: 2rem;
  color: #333;
  text-align: center;
}

.post-form {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #333;
}

.form-input,
.form-textarea,
.form-select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-input:focus,
.form-textarea:focus,
.form-select:focus {
  outline: none;
  border-color: #667eea;
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.checkbox {
  margin-right: 0.5rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #eaeaea;
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

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #545b62;
}

@media (max-width: 768px) {
  .post-form {
    padding: 1rem;
  }

  .form-actions {
    flex-direction: column;
  }
}
</style>