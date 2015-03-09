# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMail',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(verbose_name='Name', max_length=100)),
                ('sender', models.EmailField(verbose_name='Email address', max_length=128)),
                ('contact_date', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('sendersubject', models.CharField(verbose_name='Subject', max_length=100)),
                ('content', models.TextField(verbose_name='Text')),
            ],
            options={
                'verbose_name_plural': 'Contact Mails',
                'verbose_name': 'Contact Mail',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('file_name', models.CharField(verbose_name='File name', max_length=100)),
                ('author', models.CharField(verbose_name='Author', max_length=100)),
                ('email', models.EmailField(verbose_name='Email address', max_length=100)),
                ('twitter_handle', models.CharField(verbose_name='Twitter name', max_length=100)),
                ('consistent', models.BooleanField(default=False, verbose_name='FAQ consistency')),
            ],
            options={
                'verbose_name_plural': 'FAQs',
                'verbose_name': 'FAQ',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('content', models.TextField(verbose_name='Content')),
                ('subject', models.CharField(verbose_name='Subject', max_length=100)),
                ('send_date', models.DateTimeField(auto_now_add=True, verbose_name='Send date')),
            ],
            options={
                'verbose_name_plural': 'Newsletters',
                'verbose_name': 'Newsletter',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NewsletterRecipient',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('email', models.EmailField(unique=True, verbose_name='Email address', max_length=75)),
                ('confirm_id', models.CharField(help_text='Id the recipient could use to confirm his Email address and unregister the newsletter', unique=True, verbose_name='Confirmation identifier', max_length=40)),
                ('register_date', models.DateTimeField(auto_now_add=True, verbose_name='Registration date')),
                ('confirmed', models.BooleanField(default=False, verbose_name='Confirmation status')),
                ('confirm_date', models.DateTimeField(null=True, blank=True, verbose_name='Confirmation date')),
            ],
            options={
                'verbose_name_plural': 'Newsletter Recipients',
                'verbose_name': 'Newsletter Recipient',
            },
            bases=(models.Model,),
        ),
    ]
