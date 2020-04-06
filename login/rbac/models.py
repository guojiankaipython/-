from django.db import models
# Create your models here.


class Menu(models.Model):
    title = models.CharField(max_length=32,verbose_name='菜单名称')   #财务管理
    weight = models.IntegerField(default=100,verbose_name='权重')
    icon = models.CharField(max_length=32, null=True, blank=True, verbose_name='图标')
    def __str__(self):
        return self.title

class Role(models.Model):

    role_name = models.CharField(max_length=16)
    permissions = models.ManyToManyField('Permission')

    def __str__(self):
        return self.role_name

class Userinfo(models.Model):

    # username = models.CharField(max_length=32)
    # password = models.CharField(max_length=32)

    roles = models.ManyToManyField(Role)

    # def __str__(self):
    #     return self.username

    class Meta:
        abstract = True       #不让这个类去生成数据库中的表







class Permission(models.Model):

    url = models.CharField(max_length=1200,verbose_name='url')  #/customers/
    title = models.CharField(max_length=32,verbose_name='名称')  # 客户展示
    # is_menu = models.BooleanField(default=False)    #通过这个字段判断左侧菜单权限
    icon = models.CharField(max_length=32,null=True,blank=True,verbose_name='图标')   #菜单图标
    url_name = models.CharField(max_length=32,null=True,blank=True,verbose_name='url别名')
    parent = models.ForeignKey('self',null=True,blank=True,verbose_name='二级菜单')
    menu = models.ForeignKey('Menu',null=True,blank=True,verbose_name='一级菜单')

    def __str__(self):
        return self.title






