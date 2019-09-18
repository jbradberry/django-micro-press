from django.db import models


class OneGame(models.Model):
    slug = models.SlugField(unique=True)
