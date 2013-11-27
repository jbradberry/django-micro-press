from django import forms
from django.template.defaultfilters import slugify

from . import models


class ArticleForm(forms.ModelForm):
    section = forms.ModelChoiceField(models.Section.objects.all(),
                                     empty_label=None)

    class Meta:
        model = models.Article
        fields = ('title', 'byline', 'section', 'body', 'markup_type')


class CreatePressForm(forms.ModelForm):
    class Meta:
        model = models.Press
        exclude = ('content_type', 'object_id', 'realm')
