from django.db import models
from django.contrib.auth.hashers import make_password
class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # 在保存用户时加密密码
        if not self.pk:  # 仅在创建用户时加密
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title