from django.db import models

from django.contrib.auth.hashers import make_password

# Create your models here.

class User(models.Model):
    nickname = models.CharField(max_length=64, unique=True, null=False, blank=False)
    password = models.CharField(max_length=64, null=False, blank=False)
    head = models.ImageField()
    age = models.IntegerField()
    sex = models.IntegerField()

    @property
    def password(self):
        raise AttributeError('密码是不可读属性')

    @password.setter
    def password(self, password):
        self.password = make_password(password)

    # 设置密码存储
    # def save(self):
    #     if not self.password.startswith('pbkdf2_'):
    #         self.password = make_password(self.password)
    #     super().save()