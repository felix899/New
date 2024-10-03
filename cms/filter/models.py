from django.db import models
from sns.models import Package, RoomCategory

class FilterWidget(models.Model):
    name = models.CharField(max_length=100)