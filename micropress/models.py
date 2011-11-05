from django.db import models
from django.conf import settings
from django.utils.decorators import wraps
from django.contrib.contenttypes import generic
from micropress import markup


def permalink(func):
    """
    Decorator that calls urlresolvers.reverse() to return a URL using
    parameters returned by the decorated function "func".

    "func" should be a function that returns a tuple in one of the
    following formats:
        (viewname, viewargs)
        (viewname, viewargs, viewkwargs)
        (viewname, viewargs, viewkwargs, current_app)
    """
    from django.core.urlresolvers import reverse
    @wraps(func)
    def inner(*args, **kwargs):
        bits = func(*args, **kwargs)
        return reverse(bits[0], None, *bits[1:3],
                       current_app=bits[3] if bits[3:] else None)
    return inner


class Press(models.Model):
    name = models.CharField(max_length=128)
    closed = models.BooleanField(default=False)

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
            return self.issue_set.reverse()[0].number


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
    slug = models.SlugField(max_length=128)
    byline = models.CharField(max_length=128)
    section = models.ForeignKey(Section)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    body = models.TextField()
    body_html = models.TextField()
    markup_type = models.CharField(max_length=32, choices=markup.FORMATTERS,
                                   default=markup.DEFAULT_MARKUP)

    class Meta:
        get_latest_by = "created"
        ordering = ("-created", "title")
        unique_together = ("press", "slug")

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.body_html = markup.process(self.body, self.markup_type)
        super(Article, self).save(*args, **kwargs)

    @permalink
    def get_absolute_url(self):
        return ('micropress:article_detail', (),
                {'realm_slug': self.press.realm.slug,
                 'slug': self.slug},
                self.press.content_type.app_label)
