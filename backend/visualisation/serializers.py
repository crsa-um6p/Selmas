from rest_framework import serializers
from .models import soilSample, salinityAndSodicityGroup, soilQuality, Well
import math
from django.db.models import Avg, Count, FloatField, Min, Max
from django.db.models.functions import Cast
import pandas as pd

def safe_number(value):
    """Helper function to safely handle NaN and None values"""
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return 0
    return value

class SoilSampleGeoJSONSerializer(serializers.ModelSerializer):
    geometry = serializers.SerializerMethodField()
    properties = serializers.SerializerMethodField()

    class Meta:
        model = soilSample
        fields = ['geometry', 'properties']

  

    def get_geometry(self, obj):
        # Check if localisation exists and is valid
        if obj.localisation and hasattr(obj.localisation, 'x') and hasattr(obj.localisation, 'y'):
            return {
                "type": "Point",
                "coordinates": [obj.localisation.x, obj.localisation.y]
            }
        else:
            # Return null geometry if localisation is invalid or missing
            return None

    def get_properties(self, obj):
        texture_obj = obj.soiltexture_set.first()
        q = obj.soilquality_set.first()
        salinity_obj = obj.salinityandsodicitygroup_set.first()
        if salinity_obj:
            if salinity_obj.Ec_pate_sature < 0:
                ec = salinity_obj.Ec_pate_sature
            else:
                ec = 0
        else:
            ec = 0
    
        if salinity_obj:
            if salinity_obj.Ec_pate_sature < 0:
                ec = salinity_obj.Ec_pate_sature
            else:
                ec = 0
        else:
            ec = 0
    
        return {
            "Code_labo": obj.Code_labo,
            "Depth": obj.Depth,
            "Date_edition": obj.Date_edition,
            "type": "SoilSample",
            "texture": {
                "Argile": texture_obj.Argile if texture_obj else 0,
                "Lemon": texture_obj.Lemon if texture_obj else 0,
                "Sable": texture_obj.Sable if texture_obj else 0
            },
            "quality": {
                "Ph level": safe_number(q.Ph_level if q else 0),
                "Organic matter%": safe_number(q.Organic_matter if q else 0),
                "Cu": safe_number(q.Cu if q else 0),
                "Fe": safe_number(q.Fe if q else 0),
                "BORE": safe_number(q.BORE if q else 0),
                "Nt": safe_number(q.NT if q else 0),
                "CaCO3": safe_number(q.CaCO3 if q else 0),
                "Fe": safe_number(q.Fe if q else 0),
                "Nt": safe_number(q.NT if q else 0),
                "CaCO3": safe_number(q.CaCO3 if q else 0),
            },
            "salinity": {
                "classification": salinity_obj.Classification if salinity_obj else "",
                "sar": salinity_obj.Sar if salinity_obj else '',
                "esp": salinity_obj.Esp if salinity_obj else '',
                
            }
        }


class WellGeoJSONSerializer(serializers.ModelSerializer):
    geometry = serializers.SerializerMethodField()
    properties = serializers.SerializerMethodField()

    class Meta:
        model = Well
        fields = ['geometry', 'properties']


    
    def get_geometry(self, obj):
        if obj.localisation and hasattr(obj.localisation, 'x') and hasattr(obj.localisation, 'y'):
            return {
                "type": "Point",
                "coordinates": [obj.localisation.x, obj.localisation.y]
            }
        else:
            return None
        
    def get_properties(self, obj):
        return {
            "Id_well": obj.Id_well,
            "Date": obj.Date,
            "Depth": safe_number(obj.Depth) if obj.Depth else 0,
            "type": "Well",
            "Na": safe_number(obj.Na) if obj.Na else 0,
            "Ca": safe_number(obj.Ca) if obj.Ca else 0,
            "Mg": safe_number(obj.Mg) if obj.Mg else 0,
            "Cl": safe_number(obj.Cl) if obj.Cl else 0,
            "SO4": safe_number(obj.SO4) if obj.SO4 else 0,
            "NO3": safe_number(obj.NO3) if obj.NO3 else 0,
            "ec": safe_number(obj.Ec)/1000 if obj.Ec else 0,

    }
def well_to_geojson(queryset):
    features = WellGeoJSONSerializer(queryset, many=True).data
    return {
        "type": "FeatureCollection",
        "features": features
    }


def serialize_to_geojson(queryset):
    """Convert a queryset to GeoJSON FeatureCollection format"""
    features = SoilSampleGeoJSONSerializer(queryset, many=True).data
    
    total_samples = queryset.count()
    
    # Use Django's aggregation to get classification counts in one query
    classification_stats = salinityAndSodicityGroup.objects.filter(
        Code_labo__in=queryset.values_list('Code_labo', flat=True)
    ).exclude(
        Classification__isnull=True
    ).exclude(
        Classification__exact=''
    ).values('Classification').annotate(
        count=Count('Classification')
    ).order_by('-count')
    
    # Convert to the required format without loops
    classification_percentages = {
        stat['Classification']: {
            'count': stat['count'],
            'percentage': round((stat['count'] / total_samples) * 100, 2)
        }
        for stat in classification_stats
    }

    sar_stats_profondeur = queryset.filter(Depth="Profondeur").aggregate(
        mean_sar=Avg('salinityandsodicitygroup__Sar')
    )

    sar_stats_surface = queryset.filter(Depth="Surface").aggregate(
        mean_sar=Avg('salinityandsodicitygroup__Sar')
    )

    esp_stats_profondeur = queryset.filter(Depth="Profondeur").aggregate(
        mean_esp=Avg(Cast('salinityandsodicitygroup__Esp', FloatField()))
    )

    esp_stats_surface = queryset.filter(Depth="Surface").aggregate(
        mean_esp=Avg(Cast('salinityandsodicitygroup__Esp', FloatField()))
    )

    min_date = queryset.aggregate(
        min_date=Min('Date_edition')
    )
    max_date = queryset.aggregate(
        max_date=Max('Date_edition')
    )
    soil_quality_stats = soilQuality.objects.all()
    df = pd.DataFrame(soil_quality_stats.values("CaCO3","NNH4","NT","Fe","Cu","BORE"))
    
    return {
        "type": "FeatureCollection",
        "features": features,
        "aggregated_data": {
            "properties":{
                "texture":{
                    "Argile": queryset.aggregate(
                        mean_argile=Avg('soiltexture__Argile') if queryset.exists() else 0
                    )["mean_argile"],
                    "Lemon": queryset.aggregate(
                        mean_lemon=Avg('soiltexture__Lemon') if queryset.exists() else 0
                    )["mean_lemon"],
                    "Sable": queryset.aggregate(
                        mean_sable=Avg('soiltexture__Sable') if queryset.exists() else 0
                    )["mean_sable"],
                },
                "quality":{
                    "Ph level": queryset.aggregate(
                        mean_ph_level=Avg('soilquality__Ph_level') if queryset.exists() else 0
                    )["mean_ph_level"],
                    "Organic matter%": queryset.aggregate(
                        mean_organic_matter=Avg('soilquality__Organic_matter') if queryset.exists() else 0
                    )["mean_organic_matter"],

                
                    "Cu": df["Cu"].mean() if "Cu" in df.columns else 0,
                    "Fe": df["Fe"].mean() if "Fe" in df.columns else 0,
                    "BORE": df["BORE"].mean() if "BORE" in df.columns else 0,
                    "NT": df["NT"].mean() if "NT" in df.columns else 0,
                    "CaCO3": df["CaCO3"].mean() if "CaCO3" in df.columns else 0,

                    
                },


            },
            "total_samples": total_samples,
            "classification_percentages": classification_percentages,
            "sar_stats_profondeur": sar_stats_profondeur,
            "sar_stats_surface": sar_stats_surface,
            "esp_stats_profondeur": esp_stats_profondeur,
            "esp_stats_surface": esp_stats_surface,
            "min_date": min_date,
            "max_date": max_date,
        }
    } 