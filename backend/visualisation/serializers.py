from rest_framework import serializers
from .models import soilSample, salinityAndSodicityGroup
import math
from django.db.models import Avg, Count, FloatField, Min, Max
from django.db.models.functions import Cast

def safe_number(value):
    """Helper function to safely handle NaN and None values"""
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return 0
    return value

class SoilSampleGeoJSONSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    geometry = serializers.SerializerMethodField()
    properties = serializers.SerializerMethodField()

    class Meta:
        model = soilSample
        fields = ['type', 'geometry', 'properties']

    def get_type(self, obj):
        return "Feature"

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
    
        return {
            "Code_labo": obj.Code_labo,
            "Depth": obj.Depth,
            "Date_edition": obj.Date_edition,
            "texture": {
                "Argile": texture_obj.Argile if texture_obj else 0,
                "Lemon": texture_obj.Lemon if texture_obj else 0,
                "Sable": texture_obj.Sable if texture_obj else 0
            },
            "quality": {
                "Ph level": safe_number(q.Ph_level if q else 0),
                "Organic matter": safe_number(q.Organic_matter if q else 0),
                "Cu": safe_number(q.Cu if q else 0),
                "Fe": safe_number(q.Fe if q else 0),
                "NNH4": safe_number(q.NNH4 if q else 0),
                "Nt": safe_number(q.NT if q else 0),
                "CaCO3": safe_number(q.CaCO3 if q else 0),
            },
            "salinity": {
                "classification": salinity_obj.Classification if salinity_obj else "",
                "sar": salinity_obj.Sar if salinity_obj else '',
                "esp": salinity_obj.Esp if salinity_obj else '',
                "ec": ec,
            }
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
                    "Organic matter": queryset.aggregate(
                        mean_organic_matter=Avg('soilquality__Organic_matter') if queryset.exists() else 0
                    )["mean_organic_matter"],

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