# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


'''
get_user_from_request
    "name": "A",
    "price": 100,
    "type": 0,
    "category": "X",
    "birthday": "05/20"
'''


class Data(models.Model):
    name = models.TextField(default="", null=True)
    price = models.IntegerField(default=10, null=True)
    type = models.IntegerField(default=0, null=True)
    age = models.IntegerField(default=22, null=True)
    address = models.TextField(default="", null=True)


class DataWithoutName(models.Model):
    address = models.TextField(default="")


class DatetimeFilterTestingModel(models.Model):
    datetime = models.DateTimeField()
