from django.db import models

# Create your models here.

# Model to save humidity info


class Humidity(models.Model):
    name = models.CharField(max_length=200, blank=False)
    min_rate = models.IntegerField()
    max_rate = models.IntegerField()

    def __str__(self):
        return f"{self.name}"
