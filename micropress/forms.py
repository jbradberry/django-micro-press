from django import forms
from django.template.defaultfilters import slugify

from . import models


class ArticleForm(forms.ModelForm):
    section = forms.ModelChoiceField(models.Section.objects.all(),
                                     empty_label=None)

    class Meta:
        model = models.Article
        fields = ('title', 'byline', 'section', 'body', 'markup_type')

    def clean(self):
        cleaned_data = self.cleaned_data
        press = self.instance.press
        title = cleaned_data.get('title', '')
        max_length = models.Article._meta.get_field('slug').max_length

        slug, num, end = slugify(title), 1, ''
        if len(slug) > max_length:
            slug = slug[:max_length]
        while press.article_set.filter(slug=slug+end).exists():
            num += 1
            end = "-{0}".format(num)
            if len(slug) + len(end) > max_length:
                slug = slug[:max_length - len(end)]

        self.instance.slug = slug + end
        return cleaned_data


class CreatePressForm(forms.ModelForm):
    class Meta:
        model = models.Press
        exclude = ('content_type', 'object_id', 'realm')
