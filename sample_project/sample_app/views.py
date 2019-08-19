from django.views.generic import DetailView

from .models import TestRealm


class RealmView(DetailView):
    model = TestRealm
