from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Document, Text, Date, Search
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from . import models

connections.create_connection()

class EsDocumentIndex(Document):
	author = Text()
	created = Date()
	title = Text()
	json_object = Text()

	class Meta:
		index = 'esdocument-index'


# feeding index with data
def bulk_indexing():
	EsDocumentIndex.init(index='esdocument-index')
	es = Elasticsearch()
	bulk(client=es, actions=(b.indexing() for b in models.EsDocument.objects.all().iterator()))


def search(author):
	s = Search().filter('term', author=author)
	response = s.execute()
	return response