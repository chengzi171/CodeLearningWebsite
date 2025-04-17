from django.urls import path
from . import views  

urlpatterns = [
    path('articles/', views.ArticleListView.as_view(), name='article-list'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/create/', views.UserCreateView.as_view(), name='user-create'),  # 添加用户创建的路由
    path('users/login/', views.UserLoginView.as_view(), name='user-login'),  # 添加用户登录的路由
    path('users/<int:user_id>/', views.UserDetailView.as_view(), name='user-detail'),  # 用户详情路由
    path('users/<int:user_id>/articles/create/', views.ArticleCreateView.as_view(), name='article-create'),  # 添加文章创建路由
    path('users/<int:user_id>/articles/', views.UserArticlesView.as_view(), name='user-articles'),  # 用户文章路由
    path('users/<int:user_id/update/', views.UserUpdateView.as_view(), name='user-update'),  # 用户更新路由
    path('users/<int:user_id>/articles/<int:article_id>/', views.ArticleDetailView.as_view(), name='article-detail'),
]