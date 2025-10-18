from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='分类名称')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '分类'  # 单数名称
        verbose_name_plural = '分类管理'  # 复数名称

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='文章标题')
    content = models.TextField(verbose_name='文章内容')
    excerpt = models.CharField(max_length=300, blank=True, verbose_name='文章摘要')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='文章分类')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_published = models.BooleanField(default=False, verbose_name='是否发布')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文章'  # 单数名称
        verbose_name_plural = '文章管理'  # 复数名称
        ordering = ['-created_at']  # 按创建时间倒序排列

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='所属文章')
    author_name = models.CharField(max_length=100, verbose_name='评论者姓名')
    content = models.TextField(verbose_name='评论内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    is_approved = models.BooleanField(default=False, verbose_name='是否审核通过')

    def __str__(self):
        return f"{self.author_name} 对《{self.post.title}》的评论"

    class Meta:
        verbose_name = '评论'  # 单数名称
        verbose_name_plural = '评论管理'  # 复数名称
        ordering = ['-created_at']  # 按评论时间倒序排列