"""learn_rest_framework URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 路由分发
    url(r'^api/', include('api.urls')),
    url(r'^apiv2/', include('api_v2.urls')),
    url(r'^apiv3/', include('api_v3.urls')),
    url(r'^apiv4/', include('api_v4.urls')),
    url(r'^apiv5/', include('api_v5.urls')),


    url(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),
]
