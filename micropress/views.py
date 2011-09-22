from django.views.generic.list_detail import object_list, object_detail
import models


def _limit_articles(realm_object_id=None, realm_slug=None,
                    realm_slug_field='realm__slug', **kwargs):
    queryset = models.Article.objects.all()
    if realm_object_id:
        queryset = queryset.filter(realm__pk=realm_object_id)
    elif realm_slug and realm_slug_field:
        queryset = queryset.filter(**{realm_slug_field: realm_slug})
    else:
        raise AttributeError(
            "View must be called with either a realm_object_id or"
            " a realm_slug/realm_slug_field.")
    return queryset


def article_list(request, issue=None, **kwargs):
    qs = _limit_articles(**kwargs)
    if issue is not None:
        qs = qs.filter(issue=int(issue))
    return object_list(request, qs, **kwargs)


def article_detail(request, **kwargs):
    qs = _limit_articles(**kwargs)
    return object_detail(request, qs, **kwargs)
