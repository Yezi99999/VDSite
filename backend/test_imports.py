# backend/test_imports.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VDSite.settings')
django.setup()

try:
    from blog.serializers import (
        PostSerializer,
        CategorySerializer,
        CommentSerializer,
        PostListSerializer,
        PostCreateSerializer,
        PostUpdateSerializer,
        CommentCreateSerializer
    )

    print("✓ 所有序列化器导入成功")

    from blog.views import (
        CategoryViewSet,
        PostViewSet,
        CommentViewSet,
        home_stats,
        featured_posts
    )

    print("✓ 所有视图导入成功")

    print("导入检查完成！")

except ImportError as e:
    print(f"✗ 导入失败: {e}")