from django.contrib import admin
from .models import Category, Post, Comment
from django.contrib.admin import AdminSite

# 自定义管理站点
admin.site.site_header = 'VD Blog 内容管理系统'
admin.site.site_title = 'VD Blog 管理后台'
admin.site.index_title = '站点管理'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    list_per_page = 20

    # 字段显示名称
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['name'].label = '分类名称'
        return form


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'created_at', 'is_published']
    list_filter = ['category', 'is_published', 'created_at']
    search_fields = ['title', 'content']
    list_editable = ['is_published']
    date_hierarchy = 'created_at'
    list_per_page = 20

    # 字段集 - 分组显示字段
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'category', 'author')
        }),
        ('内容', {
            'fields': ('excerpt', 'content')
        }),
        ('状态', {
            'fields': ('is_published',)
        }),
    )

    # 字段显示名称
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['title'].label = '文章标题'
        form.base_fields['content'].label = '文章内容'
        form.base_fields['excerpt'].label = '文章摘要'
        form.base_fields['category'].label = '文章分类'
        form.base_fields['author'].label = '作者'
        form.base_fields['is_published'].label = '是否发布'
        return form

    # 在创建文章时自动设置作者为当前用户
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author_name', 'created_at', 'is_approved']
    list_filter = ['is_approved', 'created_at']
    list_editable = ['is_approved']
    search_fields = ['author_name', 'content']
    list_per_page = 20

    # 字段显示名称
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['post'].label = '所属文章'
        form.base_fields['author_name'].label = '评论者姓名'
        form.base_fields['content'].label = '评论内容'
        form.base_fields['is_approved'].label = '是否审核通过'
        return form