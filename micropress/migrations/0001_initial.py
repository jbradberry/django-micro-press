# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('slug', models.SlugField(max_length=128)),
                ('byline', models.CharField(max_length=128)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('body', models.TextField()),
                ('body_html', models.TextField()),
                ('markup_type', models.CharField(default=b'restructuredtext', max_length=32, choices=[(b'textile', b'textile'), (b'restructuredtext', b'restructuredtext'), (b'markdown', b'markdown')])),
                ('extra_data', jsonfield.fields.JSONField(default={})),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created', 'title'),
                'get_latest_by': 'created',
            },
        ),
        migrations.CreateModel(
            name='Press',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('closed', models.BooleanField(default=False)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name_plural': 'presses',
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='press',
            field=models.ForeignKey(to='micropress.Press'),
        ),
        migrations.AddField(
            model_name='article',
            name='section',
            field=models.ForeignKey(to='micropress.Section'),
        ),
        migrations.AlterUniqueTogether(
            name='article',
            unique_together=set([('press', 'slug')]),
        ),
    ]
