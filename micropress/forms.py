from django import forms
from micropress.models import Article, Section, Press


class ArticleForm(forms.ModelForm):
    section = forms.ModelChoiceField(Section.objects.all(), empty_label=None)

    class Meta:
        model = Article
        fields = ('title', 'slug', 'byline', 'section', 'body', 'markup_type')

    def clean_slug(self):
        slug = self.cleaned_data.get('slug', '')
        press = self.instance.press
        if Article.objects.filter(press=press, slug=slug).exists():
            raise forms.ValidationError(
                "Article with slug '{0}' already exists.".format(slug))
        return slug


class CreatePressForm(forms.ModelForm):
    class Meta:
        model = Press
        exclude = ('content_type', 'object_id', 'realm')
