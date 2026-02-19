from django.urls import re_path

from kennitest import views as kenniviews

urlpatterns = [
	re_path('$', kenniviews.handler),
	re_path('response/$', kenniviews.receive),
]
