# from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin

from utils.response import APIResponse
from api_v3 import models

from . import serializers

from rest_framework.views import APIView
class BookAPIView(APIView):
    def get(self, request, *args, **kwargs):
        book_query = models.Book.objects.filter(is_delete=False)
        book_ser = serializers.BookModelSerializer(book_query, many=True)
        book_data = book_ser.data
        return APIResponse(results=book_data)

    # def post(self, request, *args, **kwargs):
    #     # request_data = request.data
    #     response = self.create(request, *args, **kwargs)
    #     return APIResponse(results=response)


# GenericAPIView是继承APIView的，使用完全兼容APIVivew
# 重点：GenericAPIView在APIView基础上完成了哪些
# 1 get_queryset()：从类属性queryset中获取model的queryset数据
# 2 get_object()：从类属性queryset中获得model的queryset数据，再通过有名分组pk确定唯一操作对象
# # get_serializer()：从类属性serializer_class中获得serializer的序列化类
from rest_framework.generics import GenericAPIView
class BookGenericAPIViewew(GenericAPIView):
    queryset = models.Book.objects.filter(is_delete=False)
    serializer_class = serializers.BookModelSerializer

    # 群取
    # def get(self, request, *args, **kwargs):
    #     book_query = self.get_queryset()
    #     book_ser = self.get_serializer(book_query, many=True)
    #     book_data = book_ser.data
    #     return APIResponse(results=book_data

    # 单取
    def get(self, request, *args, **kwargs):
        book_query = self.get_object()
        book_ser = self.get_serializer(book_query)
        book_data = book_ser.data
        return APIResponse(results=book_data)


from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
class BookMixinGenericAPIViewew(GenericAPIView, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin):
    queryset = models.Book.objects.filter(is_delete=False)
    serializer_class = serializers.BookModelSerializer

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            response = self.retrieve(request, *args, **kwargs)
        # mixins提供的list方法的响应对象是Response，想将该对象格式化为APIResponse
        else:
            response = self.list(self, request, *args, **kwargs)
        return APIResponse(results=response.data)


    def post(self, request, *args, **kwargs):

        response = self.create(request, *args, **kwargs)
        return APIResponse(results=response.data)

    def put(self, request, *args, **kwargs):
        response = self.partial_update(request, *args, **kwargs)
        return APIResponse(results=response.data)


# 工具视图
# 1 工具视图都是GenericAPIView的子类，且不同的子类继承了不听的工具类，重写了请求方法
# 2 工具视力的功能如果奈，只需要继承工具视图，提供queryset与serizlizer_class即可
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
class BookListCreateAPIView(ListCreateAPIView, UpdateAPIView):
    queryset = models.Book.objects.filter(is_delete=False)
    serializer_class = serializers.BookModelSerializer


# 视图集
# 1 视图集都是优先继承ViewSetMixin类，再继承一个视图类(GenericAPIView或APIView)
#   GenericViewSet、ViewSet
# 2 ViewSetMixin提供了重写的as_view()方法，继承视力集的视图类，配置路由时调用as_view()必须传入，请求名-函数名 映射
#    eg: url(r'^v5/books/$', views.BookGenericViewSet.as_view({'get': 'my_get_list'})),
#    表示get请求会交给my_get_list视力函数处理
from rest_framework.viewsets import GenericViewSet
class BookGenericViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = models.Book.objects.filter(is_delete=False)
    serializer_class = serializers.BookModelSerializer

    def my_get_list(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def my_get_obj(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

# GenericViewSet 与 APIView 两大继承视图的区别
# 1 GenericViewSet和ViewSet都继承了ViewSetMixin， as_view都可以配置 请求-函数 映射
# 2 GenericViewSet继承的是GenericAPIView视图类， 用来完成标准的model类操作接口
# 3 ViewSet继承的是APIView的视图类， 用来完成不需要model参与，或是非标准的model类操作接口
#       post请求在标准的model类操作下就是新增接口，登陆的post不满足
#       post请求验证码的接口，不需要model类的参与
# 案例： 登陆的post请求，并不是完成数据的新增，只是用post提交数据，得到的结果也不是登陆的用户信息，而是登陆认证信息

# 拥有六大接口：单查、群查、单增、单删、单整体改、单局部改
# 注： 一般肯定会重写destroy
from rest_framework.viewsets import ModelViewSet
class BookModelViewSet(ModelViewSet):
    queryset = models.Book.objects.filter(is_delete=False)
    serializer_class = serializers.BookModelSerializer

    # 删不是数据库，而是该记录中的删除字段
    def destroy(self, request, *args, **kwargs):
        instance =  self.get_object() # type : models.book
        if not instance:
            return APIResponse(1, '删除失败')
        instance.is_delete = True
        instance.save()
        return APIResponse(0, '删除成功')