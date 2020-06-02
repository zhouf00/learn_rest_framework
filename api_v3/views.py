from rest_framework.views import APIView
from rest_framework.response import Response


from . import models, serializers
# Create your views here.

class Book(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            try:
                pass
            except:
                pass
        else:
            pass