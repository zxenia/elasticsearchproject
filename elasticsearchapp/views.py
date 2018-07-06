import requests
from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from elasticsearch_dsl import Document, Text, Date, Search, MultiSearch
from django.shortcuts import render_to_response

from elasticsearch import Elasticsearch
import json
from json import load, dumps


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
# 		es = Elasticsearch()
# 		res = es.search(index='esdocument-index', body={"query": {"match": {"author": query }}})
		
# 		context = {
# 		'tot_results': res['hits']['total'],
# 		'res': res['hits']['hits']}
# 		return render(request, self.template_name, context)


#this is elasticsearch-py - low level client
def essearch(request):
	context = {}
	q = request.GET.get('q')
	if q:
		es = Elasticsearch()
		results = es.search(index="esdocument-index",
			body={"query": {"match": {"author": q }}})
		context = {
		'es_total_results': results['hits']['total'],
		'es_results': results['hits']['hits']}
	return render(request, 'elasticsearchapp/search.html', context)


#this is elasticsearch-dsl - hign level client
def dsl_search(request):
	client = Elasticsearch()
	q = request.GET.get('q')
	if q:
		results = Search(using=client, index="esdocument-index")\
		.query("match", author=q).execute()
		hits = results.hits.total
	else:
		results = 'empty'

	return render(request, 'elasticsearchapp/search.html',
		{'results': results, 'hits': hits})


#Multisearch in several fields
def multi_search(request):
	client = Elasticsearch()
	q = request.GET.get('q')
	if q:
		ms = MultiSearch(using=client, index="esdocument-index")
		ms = ms.add(Search().query("match", author=q))
		ms = ms.add(Search().query("match", title=q))
		ms = ms.add(Search().query("match", json_object=q))
		responses = ms.execute()
		hits = []
		for response in responses:
			for hit in response:
				hit = hit.title
				hits.append(hit)
	else:
		responses = 'empty'

	return render(request, 'elasticsearchapp/search.html',
		{'responses': responses, 'hits': hits})