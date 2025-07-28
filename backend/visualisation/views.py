from django.shortcuts import render
from django.http import HttpResponse, JsonResponse # Importer JsonResponse pour renvoyer des réponses JSON
import pandas
import json # Importer json pour traiter les données JSON
from .models import * # Importer ALL les modèles que vous avez créés
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .serializers import serialize_to_geojson, well_to_geojson
from django.db.models import F
from django.views.decorators.cache import cache_page
from django.contrib.gis.geos import Point
# Create your views here.

# @csrf_exempt
# def get_data(request):
#     parameters = json.loads(request.body) # Chargement la requête forma JSON au format dictionnaire pour accéder aux paramètres 
#     print("--------------------------------")
#     print(parameters) # Afficher requête JSON dans la console format dictionnaire
#     print("--------------------------------")
    
    
#     min_value = parameters['min_value'] # donne moi la valeur min_value
#     max_value = parameters['max_value'] # donne moi la valeur max_value
#     variable = parameters['variable']# Récupération de la variable et du filtre à partir des paramètres
#     filter = parameters['filter']# Récupération du filtre à partir des paramètres
    

#     # condition pour variable soiltexture
#     if variable == "soiltexture":
#         if filter == "Argile" :
#             data = soilTexture.objects.filter(Argile__range=(min_value, max_value))
            
#         elif filter == "Lemon":
#             data = soilTexture.objects.filter(Lemon__range=(min_value, max_value))

#         elif filter == "Sable":
#             data = soilTexture.objects.filter(Sable__range=(min_value, max_value)) 
    
#         data_list = list(data.values()) 

    


#     # condition pour variable soilsample
#     elif variable == "soilsample":
#         if filter == "date_edition":
#             data = soilSample.objects.filter(Date_edition__range=(min_value, max_value))

#         elif filter == "date_collect":
#             data = soilSample.objects.filter(Date_collect__range=(min_value, max_value))

#         data_list = list(data.values("Code_labo", "Depth", "Date_edition"))

#     # condition pour variable soilQuality
#     elif variable == "soilQuality":
#         if filter == "Ph_level":
#             data = soilQuality.objects.filter(Ph_level__range=(min_value, max_value))

#         elif filter == "Organic_matter":
#             data = soilQuality.objects.filter(Organic_matter__range=(min_value, max_value))

#         elif filter == "Cu":
#             data = soilQuality.objects.filter(Cu__range=(min_value, max_value))

#         elif filter == "Mn":
#             data = soilQuality.objects.filter(Mn__range=(min_value, max_value))

#         elif filter == "Fe":
#             data = soilQuality.objects.filter(Fe__range=(min_value, max_value))

#         elif filter == "Zn":
#             data = soilQuality.objects.filter(Zn__range=(min_value, max_value))

#         elif filter == "NNH4":
#             data = soilQuality.objects.filter(NNH4__range=(min_value, max_value))

#         elif filter == "NO3":
#             data = soilQuality.objects.filter(NO3__range=(min_value, max_value))

#         elif filter == "NT":
#             data = soilQuality.objects.filter(NT__range=(min_value, max_value))

#         elif filter == "P2O5":
#             data = soilQuality.objects.filter(P2O5__range=(min_value, max_value))

#         elif filter == "k2o":
#             data = soilQuality.objects.filter(k2o__range=(min_value, max_value))

#         data_list = list(data.values())

#     # condition pour variable salinityAndSodicityGroup
#     elif variable == "salinityAndSodicityGroup":
#         if filter == "Ec1_5":
#             data = salinityAndSodicityGroup.objects.filter(Ec1_5__range=(min_value, max_value))

#         elif filter == "Ec_pate_sature":
#             data = salinityAndSodicityGroup.objects.filter(Ec_pate_sature__range=(min_value, max_value))

#         elif filter == "Sar":
#             data = salinityAndSodicityGroup.objects.filter(Sar__range=(min_value, max_value))

#         elif filter == "Esp":
#             data = salinityAndSodicityGroup.objects.filter(Esp__range=(min_value, max_value))

#         elif filter == "Cl":
#             data = salinityAndSodicityGroup.objects.filter(Cl__range=(min_value, max_value))


#         data_list = list(data.values())

    
#     # condition pour variable Well
#     elif variable == "Well":
#         if filter == "Date":
#             data = Well.objects.filter(Date__range=(min_value, max_value))

#         elif filter == "Depth":
#             data = Well.objects.filter(Depth__range=(min_value, max_value))

#         elif filter == "Water_depth":
#             data = Well.objects.filter(Water_depth__range=(min_value, max_value))

#         elif filter == "Pump_cal":
#             data = Well.objects.filter(Pump_cal__range=(min_value, max_value))
        

#         elif filter == "Temperature":
#             data = Well.objects.filter(Temperature__range=(min_value, max_value))

#         elif filter == "Ph":
#             data = Well.objects.filter(Ph__range=(min_value, max_value))

#         elif filter == "Ec":
#             data = Well.objects.filter(Ec__range=(min_value, max_value))

#         elif filter == "Tds_ppm":
#             data = Well.objects.filter(Tds_ppm__range=(min_value, max_value))

#         elif filter == "Salinity":
#             data = Well.objects.filter(Salinity__range=(min_value, max_value))

#         elif filter == "Resistivity":
#             data = Well.objects.filter(Resistivity__range=(min_value, max_value))
#         data_list = list(data.values("Id_well", "Date", "Depth", "Ph", "Ec", "Tds_ppm", "Salinity", "Resistivity"))

#     # condition pour variable Amendment
#     elif variable == "Amendment":
#         if filter == "Id_amendment":
#             data = Amendment.objects.filter(Id_amendment__range=(min_value, max_value))

#         elif filter == "Date_collect":
#             data = Amendment.objects.filter(Date_collect__range=(min_value, max_value))

#         elif filter == "Ph":
#             data = Amendment.objects.filter(Ph__range=(min_value, max_value))

#         elif filter == "Ec":
#             data = Amendment.objects.filter(Ec__range=(min_value, max_value))

#         elif filter == "classe":
#             data = Amendment.objects.filter(classe__range=(min_value, max_value))

#         elif filter == "cao":
#             data == Amendment.objects.filter(cao__range=(min_value, max_value))

#         elif filter == "sio2":
#             data = Amendment.objects.filter(sio2__range=(min_value, max_value))
#         data_list = list(data.values( "Id_amendment", "Date_collect", "Ph", "Ec", "classe", "cao", "sio2", "al2o3", "fe2o3", "mgo", "k2o", "na2o", "ttio2", "p2o5", "mno", "s", "clay", "silt", "sand", "wc"))

        

    


#         if 'data_list' not in locals():
#             return JsonResponse({'error': 'Aucune donnée trouvée. Vérifie les paramètres "variable" et "filter".'}, status=400)

#     return JsonResponse(data_list, safe=False)

@csrf_exempt
def get_data(request):
    parameters = json.loads(request.body)
    print("--------------------------------")
    print(parameters)
    print("--------------------------------")
    variable = parameters['variable']
    filter = parameters['filter']
    polygon_geom=None # Initialisation de geojson_polygon à None pour éviter les erreurs si le polygone n'est pas fourni
    
    if "polygon" in parameters:
        geojson_polygon = parameters["polygon"]  # Récupération du polygone GeoJSON depuis les paramètres``
        shape_poly = shape(geojson_polygon) 
        polygon_geom = GEOSGeometry(shape_poly.wkt, srid=4326)  # Convertir le polygone GeoJSON en GEOSGeometry pour filtrer les données géospatiales



    
#_________________________________________________________________
    if variable == "soilSample":
        filter_kwargs = {}

        for key, value in parameters.items():
            if key not in ["variable", "filter","polygon"]:
                filter_kwargs[f"{key}__range"] = (value["min"], value["max"])

            

        data= soilSample.objects.all() # Si aucun filtre n'est appliqué, récupérer toutes les données
        
        if polygon_geom:
            data = data.filter(localisation__within=polygon_geom)  # Filtrer les données géospatiales par le polygone
        
        
        if filter_kwargs:
            data = data.filter(**filter_kwargs)  # Appliquer les filtres
          
        
        data_list = list(data.values("Code_labo", "Depth", "Date_edition", "Date_collect"))
#__________________________________________________________________
    elif variable == "soilQuality":
    
        filter_kwargs = {} # Dictionnaire pour stocker les filtres

        for key, value in parameters.items():
         if key not in ["variable", "filter"]: # Exclure les clés 'variable' et 'filter' 
            filter_kwargs[f"{key}__range"] = (value["min"], value["max"])

    
        if filter_kwargs:
            data = soilQuality.objects.filter(**filter_kwargs)

        #else: 
            #data = soilQuality.objects.all() 

        data_list = list(data.values())
#__________________________________________________________________
    elif variable == "soilTexture":
        filter_kwargs = {}

        for key, value in parameters.items():
            if key not in ["variable", "filter"]:
                filter_kwargs[f"{key}__range"] = (value["min"], value["max"])

        if filter_kwargs:
            data = soilTexture.objects.filter(**filter_kwargs)

        #else:
            #data = soilTexture.objects.all()
        data_list = list(data.values())
#__________________________________________________________________
    elif variable == "salinityAndSodicityGroup":
        filter_kwargs = {}

        for key, value in parameters.items():
            if key not in ["variable", "filter"]:
                filter_kwargs[f"{key}__range"] = (value["min"], value["max"])

        if filter_kwargs:
            data = salinityAndSodicityGroup.objects.filter(**filter_kwargs)
        #else:
            #data = salinityAndSodicityGroup.objects.all()
        data_list = list(data.values())
#__________________________________________________________________
    elif variable == "Well":
        filter_kwargs = {}

        for key, value in parameters.items():
            if key not in ["variable", "filter"]:
                filter_kwargs[f"{key}__range"] = (value["min"], value["max"])

        if filter_kwargs:
            data = Well.objects.filter(**filter_kwargs)

        #else:
            #data = Well.objects.all()

        data_list = list(data.values( "Id_well", "Date", "Depth", "Ph", "Ec", "Tds_ppm", "Salinity", "Resistivity", "Water_depth", "Pump_cal", "Temperature"))
#__________________________________________________________________
    elif variable == "Amendment":
        filter_kwargs = {}

        for key, value in parameters.items():
            if key not in ["variable", "filter"]:
                filter_kwargs[f"{key}__range"] = (value["min"], value["max"])

            if filter_kwargs:
             data = Amendment.objects.filter(**filter_kwargs)

        #else:
            #data = Amendment.objects.all()

        data_list = list(data.values( "Id_amendment", "Date_collect", "Ph", "Ec", "Classe", "Cao", "Sio2", "Al2o3","Salinity_level","Fe2o3", "Mgo", "K2o", "Na2o", "Ttio2", "P2o5", "Mno", "S", "Clay", "Silt", "Sand", "Wc", "Name", "Lu_lc"))

    return JsonResponse(data_list, safe=False)



@csrf_exempt
@require_http_methods(["GET"])
def dashboard_data(request):
    print("--------------------------------")
    print("dashboard_data")
    print("--------------------------------")
    soil_data = soilSample.objects.all().order_by('Code_labo')
    geojson_data = serialize_to_geojson(soil_data)
    water_data = Well.objects.all().order_by('Id_well')
    geojson_data_water = well_to_geojson(water_data)
    
    
    response = JsonResponse({"soil_data": geojson_data, "water_data": geojson_data_water}, safe=False)
    # response["Access-Control-Allow-Origin"] = "*"
    # response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    # response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
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
                CaCO3=row['CaCO3 en%']
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