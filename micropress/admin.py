from django.contrib import admin
from micropress.models import Press, Issue, Section, Article


class PressAdmin(admin.ModelAdmin):
    list_display = ('name', 'realm')


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
