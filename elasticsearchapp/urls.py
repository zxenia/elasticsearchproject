from django.urls import path
from . import views

app_name = 'elasticsearchapp'

urlpatterns = [
	# path('search/', views.SearchIndexView.as_view(), name='search')
	path('search/', views.essearch, name='search'),
	path('dsl-search/', views.dsl_search, name='dsl-search'),
	]