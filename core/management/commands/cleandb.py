#!/usr/bin/env python
# This file is part of ZUKS-Website.
#
# ZUKS-Website is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ZUKS-Website is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ZUKS-Website. If not, see <http://www.gnu.org/licenses/>.

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
