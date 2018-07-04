from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .search import EsDocumentIndex
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class EsDocument(models.Model):
	title = models.CharField(max_length=200)
	json_object = models.TextField(
		blank=True,
		help_text="JSON object on which annotation will be given"
		)
	author = models.ForeignKey(
		User, on_delete=models.CASCADE, related_name='esdocument'
		)
	created = models.DateTimeField(editable=False, default=timezone.now)
	modified = models.DateTimeField(editable=False, default=timezone.now)

	def save(self, *args, **kwargs):
		if not self.id:
			self.created = timezone.now()
		self.modified = timezone.now()
		return super(EsDocument, self).save(*args, **kwargs)

#everytime new instance of EsDocument created we add to an existing index
	def indexing(self):
		obj = EsDocumentIndex(
			meta={'id':self.id},
			author=self.author.username,
			created=self.created,
			title=self.title,
			json_object=self.json_object
			)
		obj.save(index='esdocument-index')
		return obj.to_dict(include_meta=True)

	def __str__(self):
		return "{}".format(self.title)

#adding to index on post_save signal
@receiver(post_save, sender=EsDocument)
def index_esdocument(sender, instance, **kwargs):
    instance.indexing()


class Category(models.Model):
	name = models.CharField(max_length=200)
	notation = models.CharField(max_length=200)
	note = models.TextField(
		blank=True,
		help_text="Note/Comment"
		)

	def __str__(self):
		return "{}".format(self.name)


class Annotation(models.Model):
	name = models.CharField(
        max_length=255,
        blank=True,
        help_text="Annotation name"
        )
	es_document = models.TextField(
		blank=True,
		help_text="JSON object on which annotation will be given, for now just TextField"
		)
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name="states",
		help_text="The user who created current annotation"
		)
	public = models.BooleanField(
		default=False,
		help_text="Public state or not. By default is not public."
		)
	comment = models.TextField(
		blank=True,
		help_text="Comment"
		)
	category = models.ManyToManyField(
        Category, blank=True, related_name="annotation",
        help_text="Tag"
    )
	created = models.DateTimeField(editable=False, default=timezone.now)
	modified = models.DateTimeField(editable=False, default=timezone.now)

	def save(self, *args, **kwargs):
		if not self.id:
			self.created = timezone.now()
		self.modified = timezone.now()
		return super(Annotation, self).save(*args, **kwargs)

	def __str__(self):
		return "{}".format(self.name)