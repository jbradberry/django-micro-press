from template_utils.markup import formatter
from lxml.html.clean import clean_html
from django.conf import settings


FORMATTERS = [(f, f) for f in formatter._filters.keys()]
DEFAULT_MARKUP = getattr(settings, 'DEFAULT_MARKUP', "restructuredtext")
MARKUP_FILTER_OPTS = getattr(settings, 'MARKUP_FILTER_OPTS', {})
LXML_CLEAN_OPTS = getattr(settings, 'LXML_CLEAN_OPTS', {})


def process(html, filter_name):
    html = formatter(html, filter_name=filter_name,
                     **MARKUP_FILTER_OPTS.get(filter_name, {}))
    if html:
        return clean_html(html, **LXML_CLEAN_OPTS)
    return u''
