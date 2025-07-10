from django.db import models  
from django.contrib.gis.db import models 

#from django.contrib.gis.db import models

class soilSample(models.Model):
    Code_labo = models.CharField(max_length=30, primary_key=True)
    localisation = models.PointField()  # Latitude + Longitude
    Depth = models.CharField(max_length=50)
    Date_collect = models.DateField(null=True, blank=True)
    Date_edition = models.DateField(null=True, blank=True)


    def __str__(self):
        return self.Code_labo
    
class soilQuality(models.Model):
        Ph_level = models.FloatField()
        Organic_matter = models.FloatField()
        Cu = models.FloatField()
        Mn = models.FloatField()
        Fe = models.FloatField()
        Zn = models.FloatField()
        NNH4 = models.CharField(max_length=30)
        NO3 = models.FloatField()
        NT = models.FloatField()
        P2O5 = models.FloatField()
        k2o = models.FloatField()
        CaCO3 = models.FloatField()
        Code_labo = models.ForeignKey(soilSample, on_delete=models.CASCADE)

        def __str__(self):
         return f"SoilQuality - {self.Code_labo}"

class soilTexture(models.Model):
    Argile = models.FloatField()
    Lemon = models.FloatField()
    Sable = models.FloatField()
    Soil_texture_v4 = models.CharField(max_length=100)
    Code_labo = models.ForeignKey(soilSample, on_delete=models.CASCADE)

    def __str__(self):
        return f"Texture - {self.Code_labo}"
    
class salinityAndSodicityGroup(models.Model):
    Ec1_5 = models.FloatField()
    Ec_pate_sature = models.FloatField()
    Sar = models.FloatField()
    Sar_interpretation = models.CharField(max_length=100)
    Esp = models.FloatField()
    Esp_interpretation = models.CharField(max_length=100)
    Esp_Ec_interpretation = models.CharField(max_length=100)
    Cl = models.FloatField()
    Classification = models.CharField(max_length=100)
    Code_labo = models.ForeignKey(soilSample, on_delete=models.CASCADE)

    def __str__(self):
        return f"Salinity/Sodicity - {self.Code_labo}"


class Well(models.Model):
    Id_well = models.CharField(primary_key=True)
    Date = models.DateField(null=True, blank=True)
    localisation = models.PointField(null=True)  # Latitude + Longitude
    Depth = models.FloatField()
    Water_depth = models.FloatField()
    Pump_cal = models.FloatField()
    Temperature = models.FloatField()
    Ph = models.FloatField()
    Ec = models.FloatField()
    Tds_ppm = models.FloatField()
    Salinity = models.FloatField()
    Resistivity = models.FloatField()

    def __str__(self):
        return f"Well {self.Id_well}"
    
class Amendment(models.Model):
    Id_amendment = models.AutoField(primary_key=True)
    localisation = models.PointField()  # Latitude + Longitude
    Name = models.CharField(max_length=50)
    Lu_lc = models.CharField(max_length=50)
    Date_collect = models.DateField(null=True, blank=True)
    Ph = models.FloatField()
    Ec = models.FloatField()
    Salinity_level = models.CharField(max_length=50)
    Classe = models.IntegerField()
    Cao = models.FloatField()
    Sio2 = models.FloatField()
    Al2o3 = models.FloatField()
    Fe2o3 = models.FloatField()
    Mgo = models.FloatField()
    K2o = models.FloatField()
    Na2o = models.FloatField()
    Ttio2 = models.FloatField()
    P2o5 = models.FloatField()
    Mno = models.FloatField()
    S = models.FloatField()
    Clay = models.FloatField()
    Silt = models.FloatField()
    Sand = models.FloatField()
    Wc = models.FloatField()

    def __str__(self):
        return self.Name


    


 