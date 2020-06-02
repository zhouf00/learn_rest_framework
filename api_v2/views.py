from rest_framework.views import APIView
from rest_framework.response import Response

from . import models, serializers

from rest_framework.parsers import JSONParser

class Book(APIView):
    # 局部解析类配置
    parser_classes = [JSONParser]
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            book_dic = models.Book.objects.get(pk=pk).values('title', 'price').first()
            return Response({
                'status':0,
                'msg': 'ok',
                'results': book_dic
            })
        return  Response('get ok')

    def post(self, request, *args, **kwargs):
        # url拼接参数：只能一种传参方式就是拼接参数
        print(request.query_params)
        # 数据包参数： 有三种传参方式，form-data、urlencoding、json
        print(request.data)
        return Response('post ok')


class User(APIView):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            try:
                user_obj = models.User.objects.get(pk=pk)
                # 序列化一下用户对象
                user_ser = serializers.UserSerializers(user_obj)
                return Response({
                    'status': 0,
                    'msg': 0,
                    'result': user_ser.data
                })
            except:
                return Response({
                    'status': 2,
                    'msg': '用户不存在',
                })
        else:
            # 用户对象列表(queryset)不能直接作为数据返回给前台
            user_obj_list = models.User.objects.all()
            # 序列化一下用户对象
            user_ser_data = serializers.UserSerializers(user_obj_list, many=True).data
            return Response({
                'status': 0,
                'msg': 0,
                'results': user_ser_data
            })

    def post(self, request, *args, **kwargs):
        request_data = request.data
        # 数据是否合法（增加对象需要一个字典数据）
        if not isinstance(request_data,dict) or request_data == {}:
            return Response({
                'status': 1,
                'msg': '数据有误'
            })
        # 数据类型合法，但数据内容不一定合法，需要校验数据，校验（参与反序列化）的数据需要赋值给data
        book_ser = serializers.UserDeserializer(data=request_data)
        print(book_ser)
        # 序列化对象调用is_valid()完成检验，校验失败的失败信息都会被存储在序列化对象.errors
        if book_ser.is_valid():
            # 校验通过，完成新增
            book_obj = book_ser.save()
            return Response({
                'status': 0,
                'msg': 'ok',
                'results': serializers.UserSerializers(book_obj).data
            })
        else:
            return Response({
                'status': 1,
                'msg': book_ser.errors,
            })
        # 总结：
        # 1、 book_ser = serializers.UserDeserializer(data=request_data) 数据必须赋值data
        # 2、 book_ser.is_valid() 结果为通过 | 不通过
        # 3、 不通过返回 book_ser.errors给前台，通过book_obj = book_ser.save()得到新增的对象，再正常返回



