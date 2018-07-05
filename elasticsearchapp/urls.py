from django.urls import path
from . import views

app_name = 'elasticsearchapp'

urlpatterns = [
	# path('search/', views.SearchIndexView.as_view(), name='search')
	path('search/', views.essearch, name='search'),
	# path('simple-search', views.simple_search, name='simple-search'),
	]