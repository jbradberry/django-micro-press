from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.tag
def article_content(parser, token):
    return ArticleNode()


@register.inclusion_tag("micropress/headline_list.html", takes_context=True)
def most_recent(context, issue=None, number=None):
    articles = context['press'].article_set.all()
    if issue is not None:
        articles = articles.filter(issue=issue)
    if number is not None:
        articles = articles[:int(number)]
    return {'headlines': articles}


class ArticleNode(template.Node):
    def render(self, context):
        realm = context['realm']
        app_name = realm._meta.app_label

        template_list = ["micropress/{0}article_card.html".format(name)
                         for name in ("site_{0}_".format(app_name), "site_",
                                      "{0}_".format(app_name), "")]
        return render_to_string(template_list, context)
