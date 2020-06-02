# Django脚本化启动
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learn_rest_framework.settings')
django.setup()

from api_v3 import models

# author = models.Author.objects.first()
# print(author)
# print(author.detail.mobile)
#
# detail = models.AuthorDetail.objects.first()
#
# print(detail.mobile)
# print(detail.author.name)

# models.AuthorDetail.objects.filter(pk=1).delete()

# 1 作者删除，详情级联 - on_delete=models.CASCADE
# 2 作者删除，详情置空 - null=True,on_delete=models.SET_NULL
# 3 作者删除，详情重置 - default=0, on_delete=models.SET_DEFAULT
# 4 作者删除，详情不动 - on_delete=models.DO_NOTHING
models.Author.objects.filter(pk=1).delete()

