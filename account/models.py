#==>Library Import
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.db.models.signals import post_save
from django.dispatch import receiver
#==>Local Import
from .manager import UserManager


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='ایمیل کاربر',
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=50, unique=True, verbose_name='نام کاربری')
    phone = models.CharField(max_length=11, verbose_name='شماره تلفن کاربر')
    is_active = models.BooleanField(default=True, verbose_name='مجوز ورود به سایت؟')
    is_admin = models.BooleanField(default=False, verbose_name='ادمین سایت؟')
    is_author = models.BooleanField(default=False, verbose_name='نویسنده سایت؟')
    email_activate = models.BooleanField(default=False, verbose_name=' ایا ایمیل فعال شده ؟')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone']

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='کاربر')
    first_name = models.CharField(max_length=100, verbose_name='نام')
    last_name = models.CharField(max_length=100, verbose_name='نام خانوادگی')
    national_code = models.CharField(max_length=11, verbose_name='کد ملی')
    bio = models.TextField(max_length=500, verbose_name='توضیحاتی درباره خود')
    image = models.ImageField(verbose_name='تصویر')
    
    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل ها'
    
    def __str__(self):
        return self.user.username

    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    

class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11, unique=True, verbose_name='شماره تلفن')
    code = models.PositiveSmallIntegerField(verbose_name='کد اعتبار سنجی')
    created = models.DateTimeField(auto_now=True, verbose_name='زمان ساخت')

    class Meta:
        verbose_name = 'کد یکبار مصرف'
        verbose_name_plural = 'کد های یکبار مصرف'

    def __str__(self):
        return f'{self.phone_number} - {self.code} - {self.created}'


# ==> Signals
@receiver(post_save, sender=User)
def user_profile(created, sender, instance, **kwargs):
    if created:
        Profile.objects.create(user=instance)