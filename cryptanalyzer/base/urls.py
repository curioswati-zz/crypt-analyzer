from django.conf.urls import url

from . import views


app_name = 'base'
urlpatterns = [
    url(r'^contact/', views.ContactView.as_view(), name='contact'),
    url(r'^decrypt/', views.Decrypt, name='decrypt'),
    url(r'^result/', views.VisualAnalysis, name='visual_analysis'),
    url(r'^select_algorithm/(?P<analysis_type>[\w]+)/(?P<varying>[\w]+)/',
        views.SelectAlgorithm, name='select_algorithm'),
    url(r'^vary_file_size/', views.VaryFileSize, name='vary_file_size'),
    url(r'^vary_key_size/', views.VaryKeySize, name='vary_key_size'),
    url(r'^$', views.IndexView.as_view(), name='index'),
]
