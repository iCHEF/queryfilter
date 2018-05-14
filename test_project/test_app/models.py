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
    name = models.TextField(default="")
    price = models.IntegerField(default=10)
    type = models.IntegerField(default=0)
    age = models.IntegerField(default=22)