from django.template.defaultfilters import slugify
from django.contrib.contenttypes import fields
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import models
from jsonfield import JSONField

from . import markup


MICROPRESS_REALM_ARGS = getattr(settings, 'MICROPRESS_REALM_ARGS',
                                {'realm_slug': 'slug'})


class Press(models.Model):
    name = models.CharField(max_length=128)
    closed = models.BooleanField(default=False)

    content_type = models.ForeignKey("contenttypes.ContentType")
    object_id = models.PositiveIntegerField()
    realm = fields.GenericForeignKey()

    class Meta:
        verbose_name_plural = "presses"

    def __unicode__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name


class Article(models.Model):
    press = models.ForeignKey(Press)

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
    extra_data = JSONField(default={})

    class Meta:
        get_latest_by = "created"
        ordering = ("-created", "title")
        unique_together = ("press", "slug")

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.body_html = markup.process(self.body, self.markup_type)

        max_length = self._meta.get_field('slug').max_length
        slug, num, end = slugify(self.title), 1, ''
        if len(slug) > max_length:
            slug = slug[:max_length]

        while self.press.article_set.filter(slug=slug+end).exists():
            num += 1
            end = "-{0}".format(num)
            if len(slug) + len(end) > max_length:
                slug = slug[:max_length - len(end)]

        self.slug = slug + end
        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        opts = {'slug': self.slug}
        opts.update((key, getattr(self.press.realm, attr))
                    for key, attr in MICROPRESS_REALM_ARGS.iteritems())
        return reverse('micropress:article_detail', kwargs=opts,
                       current_app=self.press.content_type.app_label)
