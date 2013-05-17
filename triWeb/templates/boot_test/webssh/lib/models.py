#!/usr/bin/env python
#-*- coding:UTF-8 -*-
from django.db import models

# Create your models here.
class Servers(models.Model):
    ip = models.IPAddressField()
    username= models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    port = models.CharField(max_length=6)
    hostname = models.CharField(max_length=40)

