from django import forms
from django.template.defaultfilters import slugify
from micropress.models import Article, Section, Press


class ArticleForm(forms.ModelForm):
    section = forms.ModelChoiceField(Section.objects.all(), empty_label=None)

    class Meta:
        model = Article
        fields = ('title', 'byline', 'section', 'body', 'markup_type')

    def clean(self):
        cleaned_data = self.cleaned_data
        press = self.instance.press
        title = cleaned_data.get('title', '')
        max_length = Article._meta.get_field('slug').max_length

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
        model = Press
        exclude = ('content_type', 'object_id', 'realm')
