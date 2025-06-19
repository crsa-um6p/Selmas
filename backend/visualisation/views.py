from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import pandas
import json
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .serializers import serialize_to_geojson
from django.db.models import F
from django.views.decorators.cache import cache_page
from django.contrib.gis.geos import Point
# Create your views here.

@csrf_exempt
def get_data(request):
    parameters = json.loads(request.body)
    print("--------------------------------")
    print(parameters)
    print("--------------------------------")
    min_value = parameters['min_value']
    max_value = parameters['max_value']
    variable = parameters['variable']
    filter = parameters['filter']

    if variable == "soiltexture":
        if filter == "Argile":
            data = soilTexture.objects.filter(Argile__range=(min_value, max_value))
            
        elif filter == "Lemon":
            data = soilTexture.objects.filter(Lemon__range=(min_value, max_value))
        elif filter == "Sable":
            data = soilTexture.objects.filter(Sable__range=(min_value, max_value))
        elif filter == "Soil_texture_v4":
            data = soilTexture.objects.filter(Soil_texture_v4__range=(min_value, max_value))
        data_list = list(data.values("Code_labo_id", "Argile", "Lemon", "Sable", "Soil_texture_v4"))
    
    elif variable == "soilsample":
        if filter == "date":
            data = soilSample.objects.filter(Date_edition__range=(min_value, max_value))
        elif filter == "depth":
            data = soilSample.objects.filter(Depth__range=(min_value, max_value))
        elif filter == "code_labo":
            data = soilSample.objects.filter(Code_labo__range=(min_value, max_value))
        data_list = list(data.values("Code_labo", "Depth", "Date_edition"))
    

    


    
    return JsonResponse(data_list, safe=False)



@csrf_exempt
@require_http_methods(["GET"])
def dashboard_data(request):
    print("--------------------------------")
    print("dashboard_data")
    print("--------------------------------")
    data = soilSample.objects.all().order_by('Code_labo')
    geojson_data = serialize_to_geojson(data)
    
    response = JsonResponse(geojson_data, safe=False)
    # response["Access-Control-Allow-Origin"] = "*"
    # response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    # response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response


@csrf_exempt
@require_http_methods(["GET"])
def dashboard_data_optimized(request):
    """Alternative approach using Django ORM without serializers"""
    # Use values() to get only the fields we need
    samples = soilSample.objects.values(
        'Code_labo', 'Depth', 'Date_edition'
    ).annotate(
        longitude=F('localisation__x'),
        latitude=F('localisation__y')
    )
    
    geojson_data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [sample['longitude'], sample['latitude']]
                },
                "properties": {
                    "Code_labo": sample['Code_labo'],
                    "Depth": sample['Depth'],
                    "Date_edition": sample['Date_edition']
                }
            }
            for sample in samples
        ]
    }
    
    response = JsonResponse(geojson_data, safe=False)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response




def fill_soil_sample_table(request):
    soilSample.objects.all().delete()
    import pandas as pd
    data_file = pd.read_excel("new_data.xlsx")
    for index, row in data_file.iloc[0:337].iterrows():
        if row["Prélèvement"] != "" and row["Prélèvement"] is not None:
            soilSample.objects.create(
                Code_labo=row['Code labo'],
                localisation=Point(row['Longitude'], row["Latitude"]),
                Depth=row['Prélèvement'],
                Date_collect=row['Date réception '],
                Date_edition=row["Date d'édition "]
            )

def fill_soil_texture(request):
    soilTexture.objects.all().delete()
    import pandas as pd
    data_file = pd.read_excel("new_data.xlsx")
    for index, row in data_file.iloc[0:337].iterrows():
        soilsample = soilSample.objects.get(Code_labo=row['Code labo'])
        soilTexture.objects.create(
            Code_labo=soilsample,
            Argile=row['Argile %'],
            Lemon=row['Limon %'],
            Sable=row['Sable %'],
            Soil_texture_v4=row['Soil_Tex_V4']
        )


def fill_soil_quality(request):
    soilQuality.objects.all().delete()
    import pandas as pd
    data_file = pd.read_excel("new_data.xlsx")
    for index, row in data_file.iloc[0:337].iterrows():
        soilsample = soilSample.objects.get(Code_labo=row['Code labo'])
        try:
            soilQuality.objects.create(
                Code_labo=soilsample,
                Ph_level=row[' PH-eau'],
                Organic_matter=row['MO %'],
                Cu=row['Cu  mg/kg'],
                Mn=row['Mn mg/kg'],
                Fe=row['Fe  mg/kg'],
                Zn=row['Zn  mg/kg'],
                NNH4=row['[NNH4 mg/kg]'],
                NO3=row['[NO3 mg/kg]'],
                NT=row['Nt %'],
                P2O5=row['P2O5 mg/kg'],
                k2o=row['K2O mg/kg'],
            )
        except ValueError as e:
            print("--------------------------------")
            print(e)
            print("--------------------------------")
            continue


def fill_salinityandsodicitygroup(request):
    salinityAndSodicityGroup.objects.all().delete()
    import pandas as pd
    data_file = pd.read_excel("new_data.xlsx")
    for index, row in data_file.iloc[0:337].iterrows():
        soilsample = soilSample.objects.get(Code_labo=row['Code labo'])
        try:
            salinityAndSodicityGroup.objects.create(
                Code_labo=soilsample,
                Ec1_5 = row['EC 1:5 ms/cm'],
                Ec_pate_sature = row['EC ms/cm (pate saturée) Mésurée'],
                Sar = row['SAR'],
                Sar_interpretation = row['intéprétation'],
                Esp = row['ESP'],
                Esp_interpretation = row['Intéprétation (Sodicity)'],
                Esp_Ec_interpretation = row['Intérprétation ESP and EC'],
                    Cl = row['[Cl mg/kg]'],
                    Classification = row['Soil Type'],
                )
        except ValueError as e:
            print("--------------------------------")
            print(e)
            print("--------------------------------")
            continue