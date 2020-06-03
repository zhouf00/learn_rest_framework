from rest_framework.views import APIView
from rest_framework.response import Response


from . import models, serializers
# Create your views here.

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