from django.conf import settings
from django.db import models
from django.contrib.contenttypes import generic
from template_utils.markup import formatter


FORMATTERS = tuple((f, f) for f in formatter._filters.iterkeys())
MARKUP_FILTER_OPTS = getattr(settings, 'MARKUP_FILTER_OPTS', {})


class Press(models.Model):
    name = models.CharField(max_length=128)

    content_type = models.ForeignKey("contenttypes.ContentType")
    object_id = models.PositiveIntegerField()
    realm = generic.GenericForeignKey()

    class Meta:
        verbose_name_plural = "presses"

    def __unicode__(self):
        return self.name

    @property
    def current_issue(self):
        if self.issue_set.exists():
            return self.issue_set.reverse()[0]


class Issue(models.Model):
    subname = models.CharField(max_length=128)
    number = models.IntegerField(default=0)
    press = models.ForeignKey(Press)

    class Meta:
        ordering = ("number",)
        unique_together = ("press", "number")

    def __unicode__(self):
        return self.subname


class Section(models.Model):
    name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name


class Article(models.Model):
    press = models.ForeignKey(Press)
    issue = models.IntegerField(null=True)

    author = models.ForeignKey("auth.User")
    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, unique=True)
    byline = models.CharField(max_length=128)
    section = models.ForeignKey(Section)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    body = models.TextField()
    body_html = models.TextField()
    markup_type = models.CharField(max_length=32, choices=FORMATTERS)

    class Meta:
        get_latest_by = "created"
        ordering = ("-created", "title")
        unique_together = ("press", "slug")

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.body_html = formatter(
            self.body, filter_name=self.markup_type,
            **MARKUP_FILTER_OPTS.get(self.markup_type, {}))
        super(Article, self).save(*args, **kwargs)
