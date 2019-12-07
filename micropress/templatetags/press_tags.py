from django import template
from django.contrib.contenttypes.models import ContentType

from ..models import Press

register = template.Library()


@register.simple_tag(takes_context=True)
def get_press(context, realm):
    ct = ContentType.objects.get_for_model(realm)
    qs = Press.objects.filter(content_type=ct, object_id=realm.pk)

    press = None
    if qs:
        press = qs.get()

    return press
