from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, CreateView
from django.http import Http404
from django.conf import settings

from . import models
from . import forms


class PressMixin(object):
    model = models.Article

    realm_slug_field = 'slug'

    slug_realm_kwarg = 'realm_slug'
    pk_realm_kwarg = 'realm_pk'

    def get_realm(self):
        realm = None

        realm_content_type = self.kwargs.get('realm_content_type')
        if realm_content_type is None:
            realm_content_type = getattr(settings, 'DEFAULT_REALM_TYPE', '')

        try:
            app_label, model = realm_content_type.split('.')
            model = model.lower()
            self.realm_type = ContentType.objects.get(app_label=app_label,
                                                      model=model)
        except (ObjectDoesNotExist, ValueError) as e:
            raise ImproperlyConfigured(
                "{0} is missing a valid realm_content_type.".format(
                    self.__class__.__name__))

        realm_pk = self.kwargs.get(self.pk_realm_kwarg)
        realm_slug = self.kwargs.get(self.slug_realm_kwarg)

        if realm_pk is not None:
            opts = {'pk': realm_pk}
        elif realm_slug is not None:
            opts = {self.realm_slug_field: realm_slug}
        else:
            opts = None

        if opts:
            try:
                realm = self.realm_type.get_object_for_this_type(**opts)
            except ObjectDoesNotExist:
                raise Http404("No %s found matching this query."
                              % self.realm_type.__class__.__name__)

        return realm

    def get_press(self):
        press = None

        if self.realm:
            try:
                press = models.Press.objects.get(
                    content_type=self.realm_type, object_id=self.realm.id)
            except ObjectDoesNotExist:
                raise Http404("No Press found matching this query.")

        return press

    def get_queryset(self):
        self.realm = self.get_realm()
        self.press = self.get_press()

        queryset = super(PressMixin, self).get_queryset()

        if self.press:
            return queryset.filter(press=self.press)
        return queryset

    def get_context_data(self, **kwargs):
        context = {'press': self.press,
                   'realm': self.realm}
        context.update(kwargs)
        return super(PressMixin, self).get_context_data(**context)


class ArticleListView(PressMixin, ListView):
    pass

class ArticleDetailView(PressMixin, DetailView):
    pass


class ArticleCreateView(PressMixin, CreateView):
    form_class = forms.ArticleForm
