from django.views.generic.list_detail import object_list, object_detail
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.db.models import get_model
from django.conf import settings
from functools import wraps
import models
from micropress.forms import ArticleForm


def limit_articles(f):
    @wraps(f)
    def func(request, realm_content_type=None, realm_object_id=None,
             realm_slug=None, realm_slug_field='slug', extra_context=None,
             *args, **kwargs):
        if realm_content_type is None:
            realm_content_type = settings.DEFAULT_REALM_TYPE
        app_label, model = realm_content_type.split('.')
        realm_model = get_model(app_label, model)
        if realm_object_id is not None:
            opts = {'pk': realm_object_id}
        elif realm_slug and realm_slug_field:
            opts = {realm_slug_field: realm_slug}
        else:
            raise AttributeError(
                "View must be called with either a realm_object_id or"
                " a realm_slug/realm_slug_field.")

        realm = get_object_or_404(realm_model, **opts)
        press = get_object_or_404(models.Press, object_id=realm.id,
                                  content_type__app_label=app_label,
                                  content_type__model=model.lower())
        qs = press.article_set.all()
        if extra_context is None:
            extra_context = {}
        extra_context.update(press=press, realm=realm)
        return f(request, queryset=qs, extra_context=extra_context, **kwargs)
    return func


@limit_articles
def article_list(request, queryset=None, extra_context=None, issue=None,
                 template_object_name='article', **kwargs):
    issue_pagination = kwargs.pop('issue_paginate_by', None)
    press = extra_context['press']
    if issue is None:
        issue = request.GET.get('issue', press.current_issue)

    if issue is not None:
        issue = int(issue)
        queryset = queryset.filter(issue=issue)
        extra_context['issue'] = get_object_or_404(
            press.issue_set,
            number=issue)
        kwargs['paginate_by'] = issue_pagination

    if (issue == press.current_issue and not press.closed
        and request.user.is_authenticated()):
        a = models.Article(press=press, issue=press.current_issue,
                           author=request.user, byline="Anonymous")
        form = ArticleForm(request.POST or None, instance=a)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path)
        extra_context.update(ADMIN_MEDIA_PREFIX=settings.ADMIN_MEDIA_PREFIX,
                             form=form)
    return object_list(request, queryset, extra_context=extra_context,
                       template_object_name=template_object_name, **kwargs)


@limit_articles
def article_detail(request, template_object_name='article', **kwargs):
    return object_detail(request, template_object_name=template_object_name,
                         **kwargs)
