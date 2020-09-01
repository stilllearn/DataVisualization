from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin, BaseUserManager
from django.utils import timezone
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class MyUserManager(BaseUserManager):
    def create_user(self, id_card=None, email=None, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not id_card:
            raise ValueError('Users must have an id_card')

        user = self.model(
            id_card=id_card,
            email=email,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id_card=None, email=None, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            id_card,
            email,
            password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class BaseUser(AbstractBaseUser, PermissionsMixin):
    id_card = models.CharField(verbose_name="身份证号", max_length=18, unique=True)
    email = models.EmailField(verbose_name="邮箱", null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    telephone = models.CharField(max_length=30, verbose_name="联系方式", blank=True, null=True)
    name = models.CharField(max_length=30, verbose_name="姓名")
    gender_choices = (
        ('male', '男'),
        ('female', '女'),
    )
    sex = models.CharField(max_length=30, null=True, verbose_name="性别", choices=gender_choices, blank=True)
    province = models.CharField(max_length=30, null=True, blank=True, verbose_name="省份")
    city = models.CharField(max_length=30, null=True, blank=True, verbose_name="城市")
    district = models.CharField(max_length=30, null=True, blank=True, verbose_name="地区")
    specific = models.CharField(max_length=200, null=True, blank=True, verbose_name="详细地址")
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间', db_index=True)
    last_login = models.DateTimeField(default=timezone.now, verbose_name='上次登录')
    delete_status = models.BooleanField(default=False, verbose_name="删除状态")
    objects = MyUserManager()

    USERNAME_FIELD = 'id_card'
    REQUIRED_FIELDS = ()

    class Meta:
        ordering = ('pk',)

    def __unicode__(self):
        return self.id_card

    def __str__(self):
        return self.id_card

    def get_last_login(self):
        return self.last_login

    def get_full_name(self):
        return self.id_card

    def get_short_name(self):
        return self.id_card

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin


class Student(BaseUser):
    """
    学生模型
    """
    eid = models.CharField(max_length=30, verbose_name="学籍号", blank=True, null=True)

    def __str__(self):
        return self.name

    '''class Meta:
        default_permissions = []
        permissions = [
            ("add_student", "新增学生"),
            ("change_student", "编辑学生"),
            ("delete_student", "删除学生"),
            ("view_student", "查看学生"),
        ]'''

