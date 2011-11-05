from django import forms
from micropress.models import Article, Section, Press


class ArticleForm(forms.ModelForm):
    section = forms.ModelChoiceField(Section.objects.all(), empty_label=None)

    class Meta:
        model = Article
        fields = ('title', 'slug', 'byline', 'section', 'body', 'markup_type')


class CreatePressForm(forms.ModelForm):
    class Meta:
        model = Press
        exclude = ('content_type', 'object_id', 'realm')
