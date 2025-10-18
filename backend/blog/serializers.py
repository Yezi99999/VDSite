from rest_framework import serializers
from .models import Post, Category, Comment
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author_name', 'content', 'created_at', 'is_approved']
        read_only_fields = ['id', 'created_at', 'is_approved']


class CommentCreateSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), required=False)

    class Meta:
        model = Comment
        fields = ['post', 'author_name', 'content']

    def create(self, validated_data):
        # 如果 post 没有提供，从上下文中获取
        if 'post' not in validated_data and 'post' in self.context:
            validated_data['post'] = self.context['post']
        return super().create(validated_data)

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'excerpt', 'category', 'category_name', 
                 'author', 'author_name', 'created_at', 'updated_at', 'is_published', 
                 'comment_count']

    def get_comment_count(self, obj):
        return obj.comment_set.filter(is_approved=True).count()


class PostListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    author_name = serializers.CharField(source='author.username', read_only=True)
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'excerpt', 'category_name', 'author_name',
                  'created_at', 'comment_count', 'is_published']

    def get_comment_count(self, obj):
        return obj.comment_set.filter(is_approved=True).count()


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'excerpt', 'category', 'is_published']


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'excerpt', 'category', 'is_published']