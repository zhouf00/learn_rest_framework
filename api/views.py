from django.http import JsonResponse

from django.views import View
from . import models

# 六大基础接口：获取一个 获取所有 增加一个 删除一个 整体更新一个 局部更新一个
# 十大基础接口： 群增、群删除、整体改群改、局部改群改
class Book(View):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not pk:  # 群查
            # 操作数据库
            book_obj_list = models.Book.objects.all()
            # 序列化过程
            book_list = []
            for obj in book_obj_list:
                dic = {}
                dic['title'] = obj.title
                dic['price'] = obj.price
                book_list.append(dic)
            # 响应数据
            return JsonResponse({
                'status': 0,
                'msg': 'ok',
                'results': book_list
            }, json_dumps_params={'ensure_ascii': False})
            pass
        else:   # 单查
            book_dic = models.Book.objects.filter(pk=pk).values('title', 'price').first()
            if book_dic:
                return JsonResponse({
                    'status': 0,
                    'msg': 'ok',
                    'results': book_dic
                }, json_dumps_params={'ensure_ascii': False})
            return JsonResponse({
                'status': 2,
                'msg': '无结果',
            }, json_dumps_params={'ensure_ascii': False})

    # postman 可以完成不同方式的请求 get | post |  put
    # postman 发送数据包有三种方式： form-data | urlencoding   | json
    # 原生django对urlencoding方式数据兼容最好
    def post(self, request, *args, **kwargs):
        # 前台通过urlencoding方式提交数据
        try:
            print(request.POST)
            book_obj = models.Book.objects.create(**request.POST.dict())
            print(book_obj)
            if book_obj:
                return JsonResponse({
                    'status': 0,
                    'msg': 'ok',
                    'results': {'title': book_obj.title, 'price': book_obj.price}
                }, json_dumps_params={'ensure_ascii': False})
        except:
            return JsonResponse({
                'status': 1,
                'msg': '参数有误',
            }, json_dumps_params={'ensure_ascii': False})
        return JsonResponse({
            'status': 2,
            'msg': '新增失败',
        }, json_dumps_params={'ensure_ascii': False})


# drf框架的封装风格
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.serializers import Serializer
from rest_framework.settings import APISettings
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication

# 总结
# 1 drf对原生的request做了二次封装，reuqest._request就是原生request
# 2 原生request对象的属性和方法都可以被drf的request对象直接访问（兼容）
# 3 drf请求的所有url拼接参数均被解析到query_params中，所有数据包数据都被解析到data中
class Test(APIView):

    def get(self, request, *args, **kwargs):
        # url拼接的参数
        print(request._request.GET) # 二次封装
        print(request.GET) # 兼容
        print(request.query_params) # 拓展
        return Response('drf get ok')

    def post(self, request, *args, **kwargs):
        print(request._request.POST)  # 二次封装
        print(request.POST)  # 兼容
        print(request.data)  # 拓展

        print(request.query_params)
        return Response('drf post ok')


# 在settings.py中配置REST_FRAMEWORK，完成的是全局配置，所有接口统一处理
# 如果只有部分接口特殊化，可以完成 - 局部配置
from rest_framework.renderers import JSONRenderer
class Test2(APIView):
    renderer_classes = [JSONRenderer]
    def get(self, request, *args, **kwargs):

        return Response('drf get ok')

    def post(self, request, *args, **kwargs):

        return Response('drf post ok')