from __future__ import unicode_literals

from django.db import models
import time
from random import random
import hues


class State(object):
    def __init__(self, *a, **kw):
        super(State, self).__init__(*a, **kw)
        self.db = {}
        hues.info("init")

    def __getitem__(self, key):
        return self.db[key]

    def __setitem__(self, key, value):
        self.db[key] = value


x = State()  # this variable represents a shared buffer between threads


class Store(models.Model):
    val = models.IntegerField(null=False)


from demo.celery import task


@task
def run(i):
    x["val"] = i
    time.sleep(random() / 5)
    val = x["val"]
    Store.objects.create(val=val)


@task
def destroy():
    x["val"] = None
