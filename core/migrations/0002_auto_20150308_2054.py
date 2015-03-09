# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faq',
            options={'verbose_name_plural': 'FAQ Questions', 'verbose_name': 'FAQ Question'},
        ),
        migrations.RemoveField(
            model_name='faq',
            name='file_name',
        ),
        migrations.AddField(
            model_name='faq',
            name='question',
            field=models.CharField(max_length=100, default='', verbose_name='Question', unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='faq',
            name='slug',
            field=models.CharField(max_length=100, default='', verbose_name='Slug', unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='faq',
            name='author',
            field=models.CharField(max_length=100, blank=True, null=True, verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='faq',
            name='email',
            field=models.EmailField(max_length=100, blank=True, null=True, verbose_name='Email address'),
        ),
        migrations.AlterField(
            model_name='faq',
            name='twitter_handle',
            field=models.CharField(max_length=100, blank=True, null=True, verbose_name='Twitter name'),
        ),
    ]
