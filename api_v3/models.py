from django.db import models

# 图书管理系统 book、author、authorDetail、Publish
"""
Book表：name、price、img、authors、publish、is_delete、create_time
Publish表：name、address、is_delete、create_time
Author表：name、age、is_delete、create_time
authorDetail表：mobile、author、is_delete、create_time
"""

# 1、基表
class BaseModel(models.Model):

    is_delete = models.BooleanField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)

    # 作为基表的Model不能 数据库中形成对的表、设置abstract = True
    class Meta:
        abstract = True


class Book(BaseModel):

    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    img = models.ImageField(upload_to='img', default='img/default.jpg')
    publish = models.ForeignKey(
        to='Publish',
        db_constraint=False,
        related_name='books',
        on_delete=models.DO_NOTHING
    )
    authors = models.ManyToManyField(
        to='Author',
        db_constraint=False,
        related_name='books'
    )
    @property
    def publish_name(self):
        return self.publish.name

    @property
    def author_list(self):
        return self.authors.values('name', 'age', 'detail__mobile').all()

    class Meta:
        db_table = 'v3_book'
        verbose_name = '书籍'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Publish(BaseModel):

    name = models.CharField(max_length=64)
    address = models.CharField(max_length=64)

    class Meta:
        db_table = 'v3_publish'
        verbose_name = '出版社详情'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Author(BaseModel):

    name = models.CharField(max_length=64)
    age = models.IntegerField()

    class Meta:
        db_table = 'v3_author'
        verbose_name = '作者'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class AuthorDetail(BaseModel):

    mobile = models.CharField(max_length=11)
    author = models.OneToOneField(
        to='Author',
        db_constraint=False,
        related_name='detail',
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = 'v3_author_detail'
        verbose_name = '作者详情'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s的情况'%self.author.name