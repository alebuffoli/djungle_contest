from django.db import models
from django.utils import timezone
from datetime import datetime


class Contest(models.Model):
    code = models.CharField(max_length=30, null=False, blank=False, unique=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    start = models.DateField(null=False)
    end = models.DateField(null=False)
    prize = models.ForeignKey('api.Prize', null=False, on_delete=models.CASCADE)


class Prize(models.Model):
    code = models.CharField(max_length=30, null=False, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    perday = models.IntegerField(null=False)


class WinPerDay(models.Model):
    day = models.DateField(datetime.now())
    contest = models.ForeignKey('api.Contest', null=False, on_delete=models.CASCADE)
    winnings = models.IntegerField(default=0)
    attempts = models.IntegerField(default=0)
