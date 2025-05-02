from django.contrib.gis.db import models

# Create your models here.


class Puit(models.Model):
    geometry = models.PointField()
    date = models.DateField()

    

