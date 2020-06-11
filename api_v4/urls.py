from django.conf.urls import url,include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('v6/books', views.BookModelViewSet)

urlpatterns = [
    url(r'^v1/books/$', views.BookAPIView.as_view()),
    url(r'^v1/books/(?P<pk>.*)/$', views.BookAPIView.as_view()),

    url(r'^v2/books/$', views.BookGenericAPIViewew.as_view()),
    url(r'^v2/books/(?P<pk>.*)/$', views.BookGenericAPIViewew.as_view()),

    url(r'^v3/books/$', views.BookMixinGenericAPIViewew.as_view()),
    url(r'^v3/books/(?P<pk>.*)/$', views.BookMixinGenericAPIViewew.as_view()),

    url(r'^v4/books/$', views.BookListCreateAPIView.as_view()),
    url(r'^v4/books/(?P<pk>.*)/$', views.BookListCreateAPIView.as_view()),

    # 使用 视图集
    # View的as_view()将get请求映射到视图类的get方法
    ## View的as_view({'get': 'my_get_list'})：将get请求映射到视图类的my_get_list方法
    url(r'^v5/books/$', views.BookGenericViewSet.as_view({'get': 'my_get_list'})),
    url(r'^v5/books/(?P<pk>.*)/$', views.BookGenericViewSet.as_view({'get': 'my_get_obj'})),

    # url(r'^v6/books/$', views.BookModelViewSet.as_view({'get': 'list', 'post': 'create', })),
    # url(r'^v6/books/(?P<pk>.*)/$', views.BookModelViewSet.as_view({
    #     'get': 'retrieve',
    #     'put': 'update',
    #     'patch': 'partial_update',
    #     'delete': 'destroy'
    # })),
    url(r'^', include(router.urls))

]