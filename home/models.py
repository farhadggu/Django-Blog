#==>Library Import
from django.db import models
from django.urls import reverse
from django.conf import settings
from extensions.utils import jalali_converter


class TimeStamp(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def jcreated(self):
        return jalali_converter(self.created)
    jcreated.short_description = 'تاریخ'

    def jupdated(self):
        return jalali_converter(self.updated)


class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name='آی پی آدرس')

    class Meta:
        verbose_name = 'آی پی آدرس'
        verbose_name_plural = 'آی پی آدرس ها'
    
    def __str__(self):
        return self.ip_address


class Category(TimeStamp):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='category_parent', null=True, blank=True, verbose_name='سر دسته')
    is_sub = models.BooleanField(default=False, verbose_name='زیر مجموعه (فرزند) می باشد؟')
    title = models.CharField(max_length=100, verbose_name='نام')
    slug = models.SlugField(max_length=100, verbose_name='اسلاگ')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        ordering = ('-created',)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('home:category', args=[self.slug,])

class Post(TimeStamp):
    STATUS = (
        ('p', 'منتشر شده'),
        ('d', 'پیش نویس'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_user', verbose_name='کاربر')
    category = models.ManyToManyField(Category, related_name='post_category', verbose_name='دسته بندی')
    title = models.CharField(max_length=100, verbose_name='تیتر مقاله')
    slug = models.SlugField(max_length=100, verbose_name='اسلاگ')
    description = models.TextField(verbose_name='توضیحات')
    image = models.ImageField(verbose_name='تصویر')
    slider_show = models.BooleanField(default=False, verbose_name='در اسلایدر نمایش داده شود؟')
    vip = models.BooleanField(default=False, verbose_name='مقاله ویژه می باشد؟', help_text='فقط 2 مقاله از کل میتواند ویژه باشد')
    visit_count = models.ManyToManyField(IPAddress, blank=True, related_name='visit_count', verbose_name='تعداد بازدید')
    status = models.CharField(choices=STATUS, max_length=1, verbose_name='وضعیت')

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home:detail', args=[self.slug,])

    def get_categories(self):
        return [category.title for category in self.category.all()]
    get_categories.short_description = 'دسته بندی ها'

    @property
    def get_visit_count(self):
        return self.visit_count.count()


class Like(TimeStamp):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='like_user', verbose_name='کاربر')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like_post', verbose_name='مقاله')

    class Meta:
        verbose_name = 'لایک'
        verbose_name_plural = 'لایک ها'

    def __str__(self):
        return f"{self.user.username} liked {self.post}"
    

class Comment(TimeStamp):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comment_user', verbose_name='کاربر')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_post', verbose_name='مقاله')
    body = models.TextField(verbose_name='متن')
    is_reply = models.BooleanField(default=False, verbose_name='پاسخ داده شده؟')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='comment_reply', verbose_name='پاسخ داده شده به کامنت')

    class Meta:
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user.username} commented {self.body[:10]}'
    