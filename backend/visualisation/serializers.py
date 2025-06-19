from rest_framework import serializers
from .models import soilSample
import math

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
                "coordinates": [obj.localisation.y, obj.localisation.x]
            }
        else:
            # Return null geometry if localisation is invalid or missing
            return None

    def get_properties(self, obj):
        texture_obj = obj.soiltexture_set.first()
        q = obj.soilquality_set.first()
        salinity_obj = obj.salinityandsodicitygroup_set.first()
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
                "Ph_level": safe_number(q.Ph_level if q else 0),
                "Organic_matter": safe_number(q.Organic_matter if q else 0),
                "Cu": safe_number(q.Cu if q else 0),
                "Zn": safe_number(q.Zn if q else 0),
                "NO3": safe_number(q.NO3 if q else 0),
                "P2O5": safe_number(q.P2O5 if q else 0),
            },
            "salinity": {
                "classification": salinity_obj.Classification if salinity_obj else "",
                "sar": salinity_obj.Sar if salinity_obj else '',
                "esp": salinity_obj.Esp if salinity_obj else '',
            }
        }


def serialize_to_geojson(queryset):
    """Convert a queryset to GeoJSON FeatureCollection format"""
    features = SoilSampleGeoJSONSerializer(queryset, many=True).data
    return {
        "type": "FeatureCollection",
        "features": features
    } 