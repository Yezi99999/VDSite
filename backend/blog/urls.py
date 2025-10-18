from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('home/stats/', views.home_stats, name='home-stats'),
    path('home/featured/', views.featured_posts, name='featured-posts'),
    # 认证相关路由
    path('auth/login/', views.user_login, name='user-login'),
    path('auth/logout/', views.user_logout, name='user-logout'),
    path('auth/check/', views.check_auth, name='check-auth'),
]