from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Article, User
from .serializers import ArticleSerializer, UserSerializer
from django.contrib.auth.hashers import check_password, make_password

class ArticleListView(APIView):
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    
class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()  # 查询所有用户
        serializer = UserSerializer(users, many=True)  # 序列化用户数据
        return Response(serializer.data, status=200)

class UserCreateView(APIView):
    def post(self, request):
        # 接收前端传来的数据
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            # 对密码进行加密
            password = serializer.validated_data.get('password')
            serializer.validated_data['password'] = make_password(password)
            
            # 保存用户到数据库
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # 返回成功响应
        
        # 返回错误信息
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserCreateView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)  # 接收前端传来的数据
        if serializer.is_valid():  # 验证数据是否合法
            serializer.save()  # 保存到数据库
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # 返回成功响应
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 返回错误信息

class UserLoginView(APIView):
    def post(self, request):
        # 从请求中获取用户名和密码
        username = request.data.get('username')
        password = request.data.get('password')
        print(f"Username: {username}, Password: {password}")  # 打印用户名和密码

        # 检查用户名和密码是否提供
        if not username or not password:
            print("Username or password not provided")
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 查询用户
            user = User.objects.get(username=username)
            print(f"User found: {user.username}")
            print(f"User password: {user.password}")
            # 验证密码
            if check_password(password, user.password):
                # 登录成功，返回用户信息
                print("Login successful")
                return Response({
                    "message": "Login successful",
                    "user_id": user.id,
                    "username": user.username,
                    "description": user.description
                }, status=status.HTTP_200_OK)
            else:
                print("Invalid password")
                # 密码错误
                return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            print("User does not exist")
            # 用户不存在
            return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)
        
class UserUpdateView(APIView):
    def put(self, request, user_id):
        try:
            # 根据用户 ID 查询用户
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # 获取前端传来的数据
        description = request.data.get('description')
        if not description:
            return Response({"error": "Description is required"}, status=status.HTTP_400_BAD_REQUEST)

        # 更新用户简介
        user.description = description
        user.save()

        # 返回更新后的用户信息
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UserDetailView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)  # 根据用户 ID 查询用户
            serializer = UserSerializer(user)  # 序列化用户数据
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
class ArticleCreateView(APIView):
    def post(self, request, user_id):
        try:
            # 验证用户是否存在
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # 将用户作为文章的作者
        data = request.data
        data['author'] = user.id  # 将用户 ID 作为作者字段

        # 序列化并保存文章
        serializer = ArticleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserArticlesView(APIView):
    def get(self, request, user_id):
        try:
            # 验证用户是否存在
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # 查询该用户的所有文章
        articles = Article.objects.filter(author=user)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ArticleDetailView(APIView):
    def get(self, request, article_id):
        try:
            # 验证文章是否存在
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return Response({"error": "Article not found"}, status=status.HTTP_404_NOT_FOUND)

        # 序列化并返回文章数据
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)