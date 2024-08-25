from django.urls import include
from django.urls import re_path
from django.contrib.staticfiles.views import serve
from django.urls import path

from core import dataviews
from core import views as core_views

from django.views.generic.base import TemplateView

urlpatterns = [
    re_path(r'^$', core_views.home, name='home'),
    re_path(r'^service-worker.js', TemplateView.as_view(
            template_name="service-worker.js",
            content_type='application/javascript'),
        name='service-worker.js'),
    re_path(r'^gen/manifest.json', core_views.manifest, name='manifest'),
    re_path(r'^OneSignalSDKWorker.js', serve, kwargs={
            'path': 'js/OneSignalSDKWorker.js'}),
    re_path(r'^OneSignalSDKUpdaterWorker.js', serve, kwargs={
            'path': 'js/OneSignalSDKWorker.js'}),
    re_path(r'^terms/', include('termsandconditions.urls')),

    path('api/recent-activity/', dataviews.recent_activity),
]
