from __future__ import absolute_import

from django.core.management import BaseCommand

from core.models import run, destroy


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in xrange(10000):
            run.delay(i)
            if i % 5 == 0:
                destroy.delay()
            if i % 100 == 0:
                print("{0} done".format(i))
