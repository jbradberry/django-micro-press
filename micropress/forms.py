from django import forms
from micropress.models import Article, Section


class ArticleForm(forms.ModelForm):
    section = forms.ModelChoiceField(Section.objects.all(), empty_label=None)

    class Meta:
        model = Article
        fields = ('title', 'slug', 'byline', 'section', 'body', 'markup_type')
