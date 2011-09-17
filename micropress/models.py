from django.db import models
from django.contrib.contenttypes import generic


class Section(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        ordering = ("name",)

    def __unicode__(self):
        return self.name


class Article(models.Model):
    content_type = models.ForeignKey("contenttypes.ContentType")
    object_id = models.PositiveIntegerField()
    realm = generic.GenericForeignKey()

    author = models.ForeignKey("auth.User")

    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, unique=True)
    byline = models.CharField(max_length=64)
    section = models.ForeignKey(Section)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    body = models.TextField()
    body_html = models.TextField()
    # markup_type = models.

    class Meta:
        get_latest_by = "published"
        ordering = ("-published", "title")

    def __unicode__(self):
        return self.title
