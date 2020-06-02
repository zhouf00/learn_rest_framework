from django.conf.urls import url

from . import views
urlpatterns = [
    url(r'^books/$', views.Book.as_view()),
    url(r'^books/(?P<pk>.*)/$', views.Book.as_view()),

    url(r'^test/', views.Test.as_view()),
    url(r'^test2/', views.Test2.as_view()),


]