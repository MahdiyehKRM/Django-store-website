from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Permission, _user_get_permissions
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, f_name, l_name, phone, create, password):
        user = self.model(email=self.normalize_email(email), f_name=f_name, l_name=l_name, phone=phone,
                          create=create, )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, f_name, l_name, phone, create, password):
        user = self.create_user(email, f_name, l_name, phone, create, password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    f_name = models.CharField(max_length=50, verbose_name='نام', blank=True, null=True, )
    l_name = models.CharField(max_length=50, verbose_name='فامیلی', blank=True, null=True, )
    email = models.EmailField(unique=True, verbose_name='ایمیل', blank=True, null=True, )
    phone = models.BigIntegerField(verbose_name='موبایل', blank=True, null=True, )
    create = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ', blank=True, null=True, )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    permission = models.ManyToManyField(Permission, related_name='users')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'f_name', 'l_name', 'create']
    objects = UserManager()

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_user_permissions(self, obj=None):
        return _user_get_permissions(self, obj, 'user')

    def get_all_permissions(self, obj=None):
        return _user_get_permissions(self, obj, 'all')

    @property
    def is_staff(self):
        return self.is_admin


class Mobile(models.Model):
    phone_number = models.CharField(max_length=11, unique=True)
    code = models.IntegerField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone_number


class PhoneLoginUser(models.Model):
    phone_number = models.CharField(max_length=11, unique=True)
    code = models.IntegerField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone_number
