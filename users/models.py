from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Profile(models.Model):
    """
    OneToOneField: 1:1 관계
    user 를 기본키로 설정.
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    nickname = models.CharField(max_length=128)   # 닉네임
    position = models.CharField(max_length=128)   # 직종
    subjects = models.CharField(max_length=128)   # 관심사
    image = models.ImageField(upload_to='profile/', default='default.png')   # 프로필 사진


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)