from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
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
        queryset = super(PressMixin, self).get_queryset()

        if self.press:
            return queryset.filter(press=self.press)
        return queryset

    def get_context_data(self, **kwargs):
        context = {'press': self.press,
                   'realm': self.realm,
                   'current_app': self.press.content_type.app_label}
        context.update(kwargs)
        return super(PressMixin, self).get_context_data(**context)

    def get(self, request, *args, **kwargs):
        self.realm = self.get_realm()
        self.press = self.get_press()
        return super(PressMixin, self).get(request, *args, **kwargs)


class ArticleListView(ListView, PressMixin):
    paginate_by = 10

    def get_template_names(self):
        templates = []
        if self.template_name is not None:
            templates.append(self.template_name)

        templates.extend(
            ['micropress/%s_%s_article_list.html' % (self.realm_type.app_label, self.realm_type.model),
             'micropress/%s_article_list.html' % (self.realm_type.app_label),
             'micropress/article_list.html']
        )
        return templates


class ArticleDetailView(DetailView, PressMixin):
    def get_template_names(self):
        templates = []
        if self.template_name is not None:
            templates.append(self.template_name)

        templates.extend(
            ['micropress/%s_%s_article_detail.html' % (self.realm_type.app_label, self.realm_type.model),
             'micropress/%s_article_detail.html' % (self.realm_type.app_label),
             'micropress/article_detail.html']
        )
        return templates


MICROPRESS_EXTRA_DATA = getattr(settings, 'MICROPRESS_EXTRA_DATA', {})


class ArticleCreateView(CreateView, PressMixin):
    form_class = forms.ArticleForm

    def form_valid(self, form):
        form.instance.press = self.press
        form.instance.author = self.request.user

        form.instance.extra_data = self.capture_extra_data()

        return super(ArticleCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.realm = self.get_realm()
        self.press = self.get_press()
        return super(ArticleCreateView, self).post(request, *args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ArticleCreateView, self).dispatch(*args, **kwargs)

    def get_template_names(self):
        templates = []
        if self.template_name is not None:
            templates.append(self.template_name)

        templates.extend(
            ['micropress/%s_%s_article_form.html' % (self.realm_type.app_label, self.realm_type.model),
             'micropress/%s_article_form.html' % (self.realm_type.app_label),
             'micropress/article_form.html']
        )
        return templates

    def capture_extra_data(self):
        extras = MICROPRESS_EXTRA_DATA.get(
            '%s.%s' % (self.press.content_type.app_label,
                       self.press.content_type.model),
            {}
        )

        data = {}
        for name, attr in extras.iteritems():
            if callable(attr):
                data[name] = attr(self.press.realm, self.request)
            else:
                attr_list = attr.split('.')[1:]
                item = self.press.realm
                for a in attr_list:
                    item = getattr(item, a, None)
                data[name] = item

        return data
