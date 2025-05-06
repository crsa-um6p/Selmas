from django.contrib.gis.db import models

# Create your models here.


class Puit(models.Model):
    geometry = models.PointField()
    date = models.DateField()

    


class Sample(models.Model):
    code_labo = models.CharField(primary_key=True)
    reference = models.CharField(max_length=255)
    nature = models.CharField(max_length=255)
    geometry = models.PointField()
    date_collecte = models.DateField()
    date_reception = models.DateField()
    date_edition = models.DateField()


class Texture(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    


