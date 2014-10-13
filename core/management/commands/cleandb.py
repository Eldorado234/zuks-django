#!/usr/bin/env python

from django.core.management.base import BaseCommand, CommandError
from core.models import NewsletterRecipient
from datetime import timedelta
from django.utils import timezone
import logging

class Command(BaseCommand):
    help = 'Cleans all newsletter recipients that not confirmed her adress for the configured time'
    clean_after_days = 6

    def handle(self, *args, **options):
        filter_date = timezone.now() - timedelta(days=self.clean_after_days)
        recp = NewsletterRecipient.objects.filter(confirmed=False, register_date__lte=filter_date)

        logtext = 'Cleaned: {0}'.format(recp)
        recp.delete()

        logging.info(logtext)
        self.stdout.write(logtext)
