from django.db import models


class TestRealm(models.Model):
    slug = models.SlugField(unique=True)
