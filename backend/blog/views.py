from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Post, Category, Comment
from .serializers import (
    PostSerializer,
    CategorySerializer,
    CommentSerializer,
    PostListSerializer,
    PostCreateSerializer,
    PostUpdateSerializer,
    CommentCreateSerializer
)
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# 分类视图集
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# 文章视图集
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(is_published=True)
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        elif self.action == 'create':
            return PostCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return PostUpdateSerializer
        else:
            return PostSerializer

    def get_queryset(self):
        queryset = Post.objects.all()

        # 如果是普通用户，只返回已发布的文章
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_published=True)

        # 搜索功能
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(title__icontains=search)

        # 分类过滤
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category_id=category)

        # 预取关联数据以提高性能
        queryset = queryset.select_related('category', 'author').prefetch_related('comment_set')

        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        # 自动设置作者为当前用户
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        """为文章添加评论"""
        post = self.get_object()
        serializer = CommentCreateSerializer(
            data=request.data,
            context={'post': post}  # 传递 post 到序列化器上下文
        )

        if serializer.is_valid():
            # 自动设置评论为未审核状态
            comment = serializer.save(is_approved=False)
            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)

        # 打印验证错误以便调试
        print("评论验证错误:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 评论视图集
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(is_approved=True)
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.all()

        # 如果是管理员，可以看到所有评论，否则只看到已批准的
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_approved=True)

        # 按文章筛选评论
        post_id = self.request.query_params.get('post', None)
        if post_id:
            queryset = queryset.filter(post_id=post_id)

        return queryset.order_by('-created_at')


# 自定义 API 视图
@api_view(['GET'])
def home_stats(request):
    """获取主页统计数据"""
    try:
        total_posts = Post.objects.filter(is_published=True).count()
        total_categories = Category.objects.count()
        total_comments = Comment.objects.filter(is_approved=True).count()

        # 获取最近5篇文章
        recent_posts = Post.objects.filter(
            is_published=True
        ).order_by('-created_at')[:5]

        stats = {
            'total_posts': total_posts,
            'total_categories': total_categories,
            'total_comments': total_comments,
            'recent_posts': PostListSerializer(recent_posts, many=True).data
        }

        return Response(stats)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def featured_posts(request):
    """获取推荐文章"""
    try:
        featured = Post.objects.filter(
            is_published=True
        ).order_by('-created_at')[:3]

        serializer = PostListSerializer(featured, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 首页视图
def index(request):
    """简单的首页视图"""
    return JsonResponse({
        'message': 'VD Blog API 服务正在运行',
        'endpoints': {
            '主页统计': '/api/home/stats/',
            '推荐文章': '/api/home/featured/',
            '分类列表': '/api/categories/',
            '文章列表': '/api/posts/',
            '评论列表': '/api/comments/',
        }
    })


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_login(request):
    """用户登录"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        })
    else:
        return Response({
            'success': False,
            'error': '用户名或密码错误'
        }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def user_logout(request):
    """用户登出"""
    logout(request)
    return Response({'success': True})

@api_view(['GET'])
def check_auth(request):
    """检查用户认证状态"""
    if request.user.is_authenticated:
        return Response({
            'authenticated': True,
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name
            }
        })
    else:
        return Response({'authenticated': False})