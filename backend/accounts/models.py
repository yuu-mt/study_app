from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
  def create_user(self, email, username, password=None):
    if not email:
      raise ValueError('メールアドレスは必須です')
    email = self.normalize_email(email)
    user = self.model(email=email, username=username)
    user.set_password(password)
    user.save(using=self._db)
    return user
  
  def create_superuser(self, email, username, password=None):
    user = self.create_user(email, username, password)
    user.is_staff = True
    user.is_superuser = True
    user.save(using=self._db)
    return user
  

class User(AbstractBaseUser, PermissionsMixin):
  email = models.EmailField(unique=True, verbose_name='メールアドレス')
  username = models.CharField(max_length=50, verbose_name='ユーザー名')
  avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)

  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)

  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username']

  class Meta:
    verbose_name = 'ユーザー'
    verbose_name_plural = 'ユーザー'
  
  def __str__(self):
    return self.email
  

class Friendship(models.Model):
  """友達関係モデル"""
  from_user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
  to_user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

  class Meta:
    unique_together = ('from_user', 'to_user')
    verbose_name = '友達関係'

  def __str__(self):
    return f'{self.from_user} → {self.to_user}'
