from django.db import models
from accounts.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from datetime import datetime
from taggit.managers import TaggableManager
from django.forms import ModelForm
from django.db.models import Avg, Count
from django.db.models.signals import post_save


class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub',
                                     verbose_name='دسته بندی')
    sub_cat = models.BooleanField(default=False, verbose_name='زیر مجموعه')
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name='اسم')
    slug = models.SlugField(allow_unicode=True, unique=True, null=True, blank=True, verbose_name='نامک')
    image = models.ImageField(upload_to='category', null=True, blank=True, verbose_name='عکس')

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home:category', args=[self.pk, self.slug])


class Product(models.Model):
    VARIANT = (
        ('None', 'هیچکدام'),
        ('Size', 'سایز'),
        ('Color', 'رنگ'),
        ('Both', 'هر دو'),
    )
    category = models.ManyToManyField(Category, blank=True, related_name='cat_product', verbose_name='دسته بندی')
    name = models.CharField(max_length=200, verbose_name='اسم')
    amount = models.IntegerField(verbose_name='تعداد')
    unit_price = models.IntegerField(verbose_name='قیمت واحد')
    discount = models.IntegerField(blank=True, null=True, verbose_name='تخفیف')
    total_price = models.IntegerField(verbose_name='قیمت کل', default=0)
    information = RichTextUploadingField(blank=True, null=True, verbose_name='اطلاعات')
    status = models.CharField(default='None', max_length=200, choices=VARIANT, verbose_name='وضعیت')
    color = models.ManyToManyField('Color', blank=True, verbose_name="رنگ")
    size = models.ManyToManyField('Size', blank=True, related_name='s_product', verbose_name="سایز")
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, blank=True, null=True, verbose_name="برند")
    create = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ')
    update = models.DateTimeField(verbose_name='بروزرسانی')
    tags = TaggableManager(blank=True, verbose_name='تگ')
    available = models.BooleanField(default=True, verbose_name='موجودی')
    image = models.ImageField(upload_to='product', verbose_name='عکس')

    def save(self, *args, **kwargs):
        if not self.discount:
            self.total_price = self.unit_price
        elif self.discount:
            total = (self.discount * self.unit_price) / 100
            self.total_price = int(self.unit_price - total)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "محصولات"
        verbose_name_plural = "محصول"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home:details', args=[self.pk])

    def average(self):
        data = Comment.objects.filter(product=self, is_reply=False).aggregate(avg=Avg('rate'))
        star = 0
        if data['avg'] is not None:
            star = round(data['avg'], 1)
        return star

    def num_comments(self):
        data = Comment.objects.filter(product=self).aggregate(counts=Count('comment'))
        star = 0
        if data['counts'] is not None:
            star = int(data['counts'])
        return star


class Size(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "سایز"
        verbose_name_plural = "سایز"


class Color(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "رنگ"
        verbose_name_plural = "رنگ"


class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "برند"
        verbose_name_plural = "برند"


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='img_product', verbose_name='محصول')
    image = models.ImageField(upload_to='image/', blank=True, verbose_name='عکس')


class Variants(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام')
    update = models.DateTimeField(verbose_name='بروزرسانی')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pr_var', verbose_name='محصول')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True, related_name='v_size',
                             verbose_name='سایز')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True, verbose_name='رنگ')
    amount = models.PositiveIntegerField(verbose_name='تعداد')
    unit_price = models.PositiveIntegerField(verbose_name='قیمت واحد')
    discount = models.PositiveIntegerField(blank=True, null=True, verbose_name='تخفیف')
    total_price = models.PositiveIntegerField(verbose_name='قیمت کل')
    available = models.BooleanField(default=True, verbose_name='موجودی')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._price_dirty = self.unit_price

    def save(self, *args, **kwargs):
        if self._price_dirty != self.unit_price:
            self.update = datetime.now()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "تنوع"
        verbose_name_plural = "تنوع"

    def __str__(self):
        return self.name

    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price
        elif self.discount:
            total = (self.discount * self.unit_price) / 100
            return int(self.unit_price - total)
        return self.total_price


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments_product',
                                verbose_name='محصول')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    create = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ')
    comment = models.TextField(verbose_name='نظر')
    rate = models.PositiveIntegerField(default=1, verbose_name='امتیاز')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='comment_reply',
                              verbose_name='پاسخ')
    is_reply = models.BooleanField(default=False, verbose_name='ایا پاسخ')

    class Meta:
        verbose_name = "پیام"
        verbose_name_plural = "پیام"

    def __str__(self):
        return self.product.name


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'rate']


class ReplyForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']


class UserWishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, related_name='user_favourite')
    products = models.ManyToManyField(Product, related_name='product_favourite', blank=True, )

    class Meta:
        verbose_name = "علاقه مندی"
        verbose_name_plural = "علاقه مندی ها"

    def __str__(self):
        return self.user.email


class Chart(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    unit_price = models.IntegerField(default=0)
    update = models.DateTimeField(auto_now=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pr_update', blank=True, null=True)
    variant = models.ForeignKey(Variants, on_delete=models.CASCADE, related_name='v_update', blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        old_data = Chart.objects.filter(product__exact=self.product, unit_price__exact=self.unit_price)
        if not old_data.exists():
            return super(Chart, self).save(*args, **kwargs)


def product_post_saved(sender, instance, created, *args, **kwargs):
    data = instance
    Chart.objects.create(product=data, unit_price=data.unit_price, update=data.update, name=data.name)


post_save.connect(product_post_saved, sender=Product)


def variant_post_saved(sender, instance, created, *args, **kwargs):
    data = instance
    Chart.objects.create(variant=data, product=data.product, unit_price=data.unit_price, update=data.update,
                         name=data.name,
                         size=data.size, color=data.color)


post_save.connect(variant_post_saved, sender=Variants)
