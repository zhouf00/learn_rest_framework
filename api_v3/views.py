from rest_framework.views import APIView
from rest_framework.response import Response


from . import models, serializers
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
                book_obj = models.Book.objects.get(pk=pk)
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
            book_query = models.Book.objects.filter(is_delete=False).all()
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
            pass
        else:
            pks = request.data.get('pks')
        if models.Book.objects.filter(pk__in=pks).update(is_delete=True):
            return Response({
                'status': 0,
                'msg': '删除成功'
            })
        return Response({
            'status': 1,
            'msg': '删除失败'
        })

