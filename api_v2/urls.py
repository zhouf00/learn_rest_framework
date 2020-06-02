from django.conf.urls import url

from . import views
urlpatterns = [
    url(r'^books/$', views.Book.as_view()),
    url(r'^books/(?P<pk>.*)/$', views.Book.as_view()),

    url(r'^users/$', views.User.as_view()),
    url(r'^users/(?P<pk>.*)/$', views.User.as_view()),


]