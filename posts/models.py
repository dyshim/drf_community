from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from users.models import Profile

# Create your models here.


class Post(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')   # 작성자
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, blank=True)   # 프로필 정보
    title = models.CharField(max_length=128)   # 제목
    category = models.CharField(max_length=128)   # 분류
    body = models.TextField()   # 내용
    image = models.ImageField(
        upload_to='post/', default='default.png')   # 이미지 파일
    likes = models.ManyToManyField(
        User, related_name='list_posts', blank=True)   # 좋아요를 누른 유저
    published_date = models.DateTimeField(default=timezone.now)   # 글이 올라간 시간


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
