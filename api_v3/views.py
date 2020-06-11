from rest_framework.views import APIView
from rest_framework.response import Response


from . import models, serializers

from utils.response import APIResponse
# Create your views here.


class Publish(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            try:
                publish_obj = models.Publish.objects.get(pk=pk, is_delete=False)
                publish_data = serializers.PulishModelSerializer(publish_obj).data
            except:
                return Response({
                    'status': 1,
                    'msg': '出版社不存在'
                })
        else:
            publish_query = models.Publish.objects.filter(is_delete=False).all()
            publish_data = serializers.PulishModelSerializer(publish_query, many=True).data
        return Response({
            'status': 0,
            'msg': 'OK',
            'results': publish_data
        })


class Book(APIView):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            try:
                book_obj = models.Book.objects.get(pk=pk)
                book_data = serializers.BookModelSerializer(book_obj).data
                return Response({
                    'status': 1,
                    'msg': 'OK',
                    'results': book_data
                })
            except:
                return Response({
                    'status': 1,
                    'msg': '书籍不存在'
                })
        else:
            book_query = models.Book.objects.filter(is_delete=False).all()
            book_data = serializers.BookModelSerializer(book_query, many=True).data
            return Response({
                'status': 1,
                'msg': 'OK',
                'results': book_data
            })

    def post(self, request, *args, **kwargs):

        request_data = request.data
        print(request_data)
        book_ser = serializers.BookModelDeserializer(data=request_data)
        # 当校验失败，马上终止当前视图方法，抛异常返回给前台
        book_ser.is_valid(raise_exception=True)
        book_obj = book_ser.save()
        return Response({
            'status': 0,
            'msg': 'ok',
            'results': serializers.BookModelSerializer(book_obj).data
        })


class V2Book(APIView):

    # 单查：有pk
    # 群查：无pk
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            try:
                book_obj = models.Book.objects.get(pk=pk, is_delete=False)
                book_data = serializers.V2BookModelSerializer(book_obj).data
                return Response({
                    'status': 1,
                    'msg': 'OK',
                    'results': book_data
                })
            except:
                return Response({
                    'status': 1,
                    'msg': '书籍不存在'
                })
        else:
            book_query = models.Book.objects.filter(is_delete=False)
            print(book_query)
            book_data = serializers.V2BookModelSerializer(book_query, many=True).data
            return Response({
                'status': 1,
                'msg': 'OK',
                'results': book_data
            })

    # 单增：传的数据是与model对应的字典
    # 群增：传的数据是装多个model对应字典的列表
    def post(self, request, *args, **kwargs):

        request_data = request.data
        print(request_data)
        if isinstance(request_data, dict):
            print('单增')
            many = False
        elif isinstance(request_data, list):
            print('群增')
            many = True

        else:
            return Response({
                'status': 1,
                'msg': '数据有误'
            })
        book_ser = serializers.V2BookModelSerializer(data=request_data, many=many)
        # 当校验失败，马上终止当前视图方法，抛异常返回给前台
        book_ser.is_valid(raise_exception=True)
        book_result = book_ser.save()
        return Response({
            'status': 0,
            'msg': 'ok',
            'results': serializers.V2BookModelSerializer(book_result, many=many).data
        })

    # 单查：有pk
    # 群查：有pks
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            pks = [pk]
        else:
            pks = request.data.get('pks')
        if models.Book.objects.filter(pk__in=pks, is_delete=False).update(is_delete=True):
            return Response({
                'status': 0,
                'msg': '删除成功'
            })
        return Response({
            'status': 1,
            'msg': '删除失败'
        })

    # 单整体改：对v2/books/(pk)/传的数据是与model对应的字典{name|price|publish|authors}
    def put(self, request, *args, **kwargs):
        request_data = request.data
        pk = kwargs.get('pk')
        old_book_obj = models.Book.objects.filter(pk=pk).first()

        book_ser = serializers.V2BookModelSerializer(instance=old_book_obj, data=request_data)
        book_ser.is_valid(raise_exception=True)
        # 校验通过，完成数据的更新：要更新的目标，用来更新新的数据
        book_obj = book_ser.save()
        return Response({
            'status': 0,
            'msg': 'ok',
            'results': serializers.V2BookModelSerializer(book_obj).data
        })

    # 单局部改：对v2/books/(pk)/传的数据，数据字段key都是选填
    # 群局部心：
    # 请求数据 - [{pk:1, name:123},{pk:3, price:7},{pk:3, publish:2}]
    def patch(self, request, *args, **kwargs):
        request_data = request.data
        pk = kwargs.get('pk')
        # 将单改，群发的数据都格式化成pks=[需要的对象主键标识] |request_data=[每个修改的对象对应的修改数据]
        if pk and isinstance(request_data, dict): # 单改
            print('单改')
            pks = [pk, ]
            request_data = [request_data, ]
        elif isinstance(request_data, list): # 群改
            print('群发')
            pks = []
            for dic in request_data:
                # 默认每个字段中都有pk
                pk = dic.pop('pk', None)
                if pk:
                    pks.append(pk)
                else:
                    return Response({
                        'status': 1,
                        'msg': '数据有误'
                    })
        else:
            return Response({
                'status': 1,
                'msg': '数据有误'
            })

        # pks与request_data数据筛选
        # 1 将pks中的没有对应数据的pk与数据删除的pk移除，request_data对应索引位上的数据也移除
        # 2 将合理的pks转换为objs
        objs = []
        new_request_data = []
        for index, pk in enumerate(pks):
            try:
                # pk对应的数据合理，将合理的对象存储 - 数据得存在
                obj = models.Book.objects.get(pk=pk, is_delete=False)
                objs.append(obj)
                # 对应索引的数据就需要保存下来
                new_request_data.append(request_data[index])
            except:
                # 重点： 反而教程- pk对应的数据有误，将对应索引的data中request_data中移除
                # index = pks.index(pk)
                # request_data.pop(index)
                continue
        # 需求：
        # 1 在视图类中，可以通过request得到登陆用户request
        # 2 在序列化类中，要完成数据库数据的校验与入库操作，可能会需要知道当前用户，但序列化类无法访问request
        # 3 在视图类中实例化序列化对象时，将request对象传出去
        book_ser = serializers.V2BookModelSerializer(context={'request': request}, instance=objs, data=request_data, partial=True, many=True)
        book_ser.is_valid(raise_exception=True)
        book_objs = book_ser.save()

        # return Response({
        #     'status': 0,
        #     'msg': 'put ok',
        #     'results': serializers.V2BookModelSerializer(book_objs, many=True).data
        # })
        book_objs_data = serializers.V2BookModelSerializer(book_objs, many=True).data
        return APIResponse(2,results=book_objs_data)



    # 总结：
    """
    1 单整体修改：
    V2BookModelSerializer(
          instance=要被更新的对象,
          data=用来更新的数据,
          partial=默认False，必须的字段全部参与校验
      )
    
    """
