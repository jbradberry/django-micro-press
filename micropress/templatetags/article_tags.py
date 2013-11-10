from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.tag
def article_content(parser, token):
    bits = token.split_contents()
    tagname = bits.pop(0)
    if len(bits) > 1:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % tagname
    if bits and bits[0] == 'links':
        return ArticleNode(True)
    return ArticleNode()


@register.inclusion_tag("micropress/headline_list.html", takes_context=True)
def most_recent(context, number=None):
    articles = context['press'].article_set.all()
    if number is not None:
        articles = articles[:int(number)]
    return {'headlines': articles}


class ArticleNode(template.Node):
    def __init__(self, links=False):
        self.links = links

    def render(self, context):
        realm = context['realm']
        app_name = realm._meta.app_label
        context['links'] = self.links

        template_list = ["micropress/{0}article_card.html".format(name)
                         for name in ("site_{0}_".format(app_name), "site_",
                                      "{0}_".format(app_name), "")]
        return render_to_string(template_list, context)
