from django import forms

from . import models


class ArticleForm(forms.ModelForm):
    section = forms.ModelChoiceField(models.Section.objects.all(),
                                     empty_label=None)

    class Meta:
        model = models.Article
        fields = ('title', 'byline', 'section', 'body')


class CreatePressForm(forms.ModelForm):
    class Meta:
        model = models.Press
        fields = ('name', 'closed')
