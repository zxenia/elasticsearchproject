import requests
from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from elasticsearch_dsl import Document, Text, Date, Search
from django.shortcuts import render_to_response

from elasticsearch import Elasticsearch


# Create your views here.
# class SearchIndexView(TemplateView):
# 	template_name = 'elasticsearchapp/search.html'
# 	#form_class = SenderForm

# 	def get_context_data(self, **kwargs):
# 		context = super(SearchIndexView, self).get_context_data(**kwargs)
# 		return context


# 	def post(self, request):
# 		# page = request.GET.get('page', 1)
# 		# from_ = (int(page) - 1) * settings.ES_PAGE_SIZE
# 		query = self.request.POST.get('q', None)
# 		elastic_query = {}
# 		es = Elasticsearch()
# 		res = es.search(index='esdocument-index', body=elastic_query)
		
# 		context = {
# 		'tot_results': res['hits']['total'],
# 		'res': res['hits']['hits']}
# 		return render(request, self.template_name, context)


def essearch(request):
	context = {}
	if 'q' in request.GET:
		query = request.GET.get('q', '')
		es = Elasticsearch()
		results = es.search(index='esdocument-index', body={"query": {"match": {"content": query }}})
	else:
		query = None
		results = None
	context['query'] = query
	context['results'] = results
	return render(request, 'elasticsearchapp/search.html', context)
