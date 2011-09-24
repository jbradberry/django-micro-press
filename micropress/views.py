from django.contrib.contenttypes.models import ContentType
from django.views.generic.list_detail import object_list, object_detail
from django.conf import settings
from functools import wraps
import models


def limit_articles(f):
    @wraps(f)
    def func(request, realm_content_type=None, realm_object_id=None,
             realm_slug=None, realm_slug_field='slug', *args, **kwargs):
        if realm_content_type is None:
            realm_content_type = settings.DEFAULT_REALM_TYPE
        app_label, model = realm_content_type.split('.')
        realm_model = ContentType.objects.get(app_label=app_label,
                                              model=model.lower())

        if realm_slug and realm_slug_field:
            realm_object_id = realm_model.get_object_for_this_type(**
                {realm_slug_field: realm_slug}).id
        elif realm_object_id is None:
            raise AttributeError(
                "View must be called with either a realm_object_id or"
                " a realm_slug/realm_slug_field.")

        qs = models.Article.objects.filter(object_id=realm_object_id,
                                           content_type=realm_model)
        return f(request, *args, queryset=qs, **kwargs)
    return func


@limit_articles
def article_list(request, issue=None, queryset=None, **kwargs):
    if issue is not None:
        queryset = queryset.filter(issue=int(issue))
    return object_list(request, queryset, **kwargs)


@limit_articles
def article_detail(request, **kwargs):
    return object_detail(request, **kwargs)
