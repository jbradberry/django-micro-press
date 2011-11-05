from django.contrib import admin
from django.forms import ModelChoiceField
from django.contrib.contenttypes.models import ContentType
from micropress.models import Press, Issue, Section, Article


class GenericModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return u"{0}.{1}".format(obj.app_label, obj.model)


class PressAdmin(admin.ModelAdmin):
    list_display = ('name', 'realm')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'content_type':
            kwargs['form_class'] = GenericModelChoiceField
        return super(PressAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)


class IssueAdmin(admin.ModelAdmin):
    list_display = ('subname', 'press', 'number')


class ArticleAdmin(admin.ModelAdmin):
    fields = ('press', 'issue', 'author', 'title', 'slug', 'byline',
              'section', 'body', 'markup_type')
    list_display = ('title', 'author', 'byline', 'section', 'press', 'issue',
                    'created', 'modified')
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Press, PressAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Section)
admin.site.register(Article, ArticleAdmin)
