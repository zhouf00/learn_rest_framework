from django.db import models

# Create your models here.

class Book(models.Model):

    title = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'old_boy_book'
        verbose_name = '书籍'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '《%s》'%self.title