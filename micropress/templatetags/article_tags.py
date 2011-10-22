from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.tag
def article_content(parser, token):
    return ArticleNode()


class ArticleNode(template.Node):
    def render(self, context):
        realm = context['realm']
        app_name = realm._meta.app_label

        template_list = ["micropress/{0}article_card.html".format(name)
                         for name in ("site_{0}_".format(app_name), "site_",
                                      "{0}_".format(app_name), "")]
        return render_to_string(template_list, context)
