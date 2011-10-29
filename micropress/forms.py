from django import forms
from micropress.models import Article, Section, Press


class ArticleForm(forms.ModelForm):
    section = forms.ModelChoiceField(Section.objects.all(), empty_label=None)

    class Meta:
        model = Article
        fields = ('title', 'slug', 'byline', 'section', 'body', 'markup_type')


class CreatePressForm(forms.ModelForm):
    create = forms.BooleanField(initial=True, required=False)

    class Meta:
        model = Press
        exclude = ('content_type', 'object_id', 'realm')

    def full_clean(self):
        if self.data.get('create', False):
            super(CreatePressForm, self).full_clean()
        else:
            self.cleaned_data = {}
            self._errors = forms.util.ErrorDict()

    def save(self, *args, **kwargs):
        if self.cleaned_data:
            return super(CreatePressForm, self).save(*args, **kwargs)
