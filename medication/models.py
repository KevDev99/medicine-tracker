import re
from django.db import models
from django.utils.translation import gettext_lazy as _
from pkg_resources import require
from multiselectfield import MultiSelectField
import datetime as dt
from django.conf import settings


class Medication(models.Model):

    class DosageUnit(models.TextChoices):
        MG = 'MG', _('mg')
        ML = 'ML', _('ml')

    DAY_CHOICES = (
        ("MON", "Monday"),
        ("TUE", "Tuesday"),
        ("WED", "Wednesday"),
        ("THU", "Thursday"),
        ("FRI", "Friday"),
        ("SAT", "Saturday"),
        ("SUN", "Sunday"),
    )

    HOUR_CHOICES = [
        (dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]

    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.CASCADE
    )
    dosage = models.IntegerField()
    dosage_unit = models.CharField(
        max_length=2,
        choices=DosageUnit.choices,
        default=DosageUnit.MG
    )
    day = MultiSelectField(choices=DAY_CHOICES)
    time = MultiSelectField(choices=HOUR_CHOICES)
  
