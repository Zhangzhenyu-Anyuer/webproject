from django.db import models

# Create your models here.

class BaseModel(models.Model):
    is_show = models.BooleanField(default=False,verbose_name='是否展示')
    orders = models.IntegerField(default=1,verbose_name='排序')
    is_delete = models.BooleanField(default=False,verbose_name='是否删除')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')

    class Meta:
        abstract = True


class Banner(BaseModel):
    """轮播图"""
    img = models.ImageField(upload_to='banner',verbose_name='轮播图')
    title = models.CharField(max_length=200,verbose_name='图片标题')
    link = models.CharField(max_length=300,verbose_name='图片链接')

    class Meta:
        db_table = 'edu_banner'
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

class Nav(BaseModel):
    """导航栏"""
    POSITION_OPTION = (
        (1,'顶部导航'),
        (2,'底部导航'),
    )

    title = models.CharField(max_length=200,verbose_name='导航标题')
    link = models.CharField(max_length=300,verbose_name='导航链接')
    position = models.IntegerField(choices=POSITION_OPTION,default=1,verbose_name='导航位置')
    is_site = models.BooleanField(default=False,verbose_name='是否是外部链接')

    class Meta:
        db_table = 'edu_nav'
        verbose_name = '导航栏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title