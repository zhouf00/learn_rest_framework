from django.conf.urls import url

from . import views
urlpatterns = [
    url(r'^books/$', views.Book.as_view()),
    url(r'^books/(?P<pk>.*)/$', views.Book.as_view()),

    url(r'^publish/$', views.Publish.as_view()),
    url(r'^publish/(?P<pk>.*)/$', views.Publish.as_view()),

    url(r'^v2/books/$', views.V2Book.as_view()),
    url(r'^v2/books/(?P<pk>.*)/$', views.V2Book.as_view()),
]