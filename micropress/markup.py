from django.conf import settings

import markdown


MARKUP_FILTER_OPTS = getattr(settings, 'MARKUP_FILTER_OPTS', {})


def process(html):
    html = markdown.markdown(html)
    if html:
        return html
    return ''
