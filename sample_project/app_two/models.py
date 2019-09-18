from django.db import models


class TwoGame(models.Model):
    slug = models.SlugField(unique=True)


class TwoGameAlso(models.Model):
    slug = models.SlugField(unique=True)
