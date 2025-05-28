from django.shortcuts import render
from django.http import HttpResponse, JsonResponse # Importer JsonResponse pour renvoyer des réponses JSON
import pandas
import json # Importer json pour traiter les données JSON
from .models import * # Importer ALL les modèles que vous avez créés
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def get_data(request):
    parameters = json.loads(request.body) # Chargement la requête forma JSON au format dictionnaire pour accéder aux paramètres 
    print("--------------------------------")
    print(parameters) # Afficher requête JSON dans la console format dictionnaire
    print("--------------------------------")
    



    
    min_value = parameters['min_value'] # donne moi la valeur min_value
    max_value = parameters['max_value'] # donne moi la valeur max_value
    variable = parameters['variable']# Récupération de la variable et du filtre à partir des paramètres
    filter = parameters['filter']# Récupération du filtre à partir des paramètres
    

    # condition pour variable soiltexture
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

    


    # condition pour variable soilsample
    elif variable == "soilsample":
        if filter == "date":
            data = soilSample.objects.filter(Date_edition__range=(min_value, max_value))
        elif filter == "depth":
            data = soilSample.objects.filter(Depth__range=(min_value, max_value))
        elif filter == "code_labo":
            data = soilSample.objects.filter(Code_labo__range=(min_value, max_value))
        data_list = list(data.values("Code_labo", "Depth", "Date_edition"))

    # condition pour variable soilQuality
    elif variable == "soilQuality":
        if filter == "Ph_level":
            data = soilQuality.objects.filter(Ph_level__range=(min_value, max_value))

        elif filter == "Organic_matter":
            data = soilQuality.objects.filter(Organic_matter__range=(min_value, max_value))

        elif filter == "Cu":
            data = soilQuality.objects.filter(Cu__range=(min_value, max_value))

        elif filter == "Mn":
            data = soilQuality.objects.filter(Mn__range=(min_value, max_value))

        elif filter == "Fe":
            data = soilQuality.objects.filter(Fe__range=(min_value, max_value))

        elif filter == "Zn":
            data = soilQuality.objects.filter(Zn__range=(min_value, max_value))

        elif filter == "NNH4":
            data = soilQuality.objects.filter(NNH4__range=(min_value, max_value))

        elif filter == "NO3":
            data = soilQuality.objects.filter(NO3__range=(min_value, max_value))

        elif filter == "NT":
            data = soilQuality.objects.filter(NT__range=(min_value, max_value))

        elif filter == "P2O5":
            data = soilQuality.objects.filter(P2O5__range=(min_value, max_value))

        elif filter == "k2o":
            data = soilQuality.objects.filter(k2o__range=(min_value, max_value))

        data_list = list(data.values())

    # condition pour variable salinityAndSodicityGroup
    elif variable == "salinityAndSodicityGroup":
        if filter == "Ec1_5":
            data = salinityAndSodicityGroup.objects.filter(Ec1_5__range=(min_value, max_value))

        elif filter == "Ec_pate_sature":
            data = salinityAndSodicityGroup.objects.filter(Ec_pate_sature__range=(min_value, max_value))

        elif filter == "Sar":
            data = salinityAndSodicityGroup.objects.filter(Sar__range=(min_value, max_value))

        elif filter == "Sar_interpretation":
            data = salinityAndSodicityGroup.objects.filter(Sar_interpretation__range=(min_value, max_value))

        elif filter == "Esp":
            data = salinityAndSodicityGroup.objects.filter(Esp__range=(min_value, max_value))

        elif filter == "Esp_interpretation":
            data = salinityAndSodicityGroup.objects.filter(Esp_interpretation__range=(min_value, max_value))

        elif filter == "Esp_Ec_interpretation":
            data = salinityAndSodicityGroup.objects.filter(Esp_Ec_interpretation__range=(min_value, max_value))

        elif filter == "Cl":
            data = salinityAndSodicityGroup.objects.filter(Cl__range=(min_value, max_value))

        elif filter == "Classification":
            data = salinityAndSodicityGroup.objects.filter(Classification__range=(min_value, max_value))

        data_list = list(data.values())

    
    # condition pour variable Well
    elif variable == "Well":
        if filter == "Id_well":
            data = Well.objects.filter(Id_well__range=(min_value, max_value))

        elif filter == "Date":
            data = Well.objects.filter(Date__range=(min_value, max_value))

        elif filter == "Depth":
            data = Well.objects.filter(Depth__range=(min_value, max_value))

        elif filter == "Water_depth":
            data = Well.objects.filter(Water_depth__range=(min_value, max_value))

        elif filter == "Pump_cal":
            data = Well.objects.filter(Pump_cal__range=(min_value, max_value))
        

        elif filter == "Temperature":
            data = Well.objects.filter(Temperature__range=(min_value, max_value))

        elif filter == "Ph":
            data = Well.objects.filter(Ph__range=(min_value, max_value))

        elif filter == "Ec":
            data = Well.objects.filter(Ec__range=(min_value, max_value))

        elif filter == "Tds_ppm":
            data = Well.objects.filter(Tds_ppm__range=(min_value, max_value))

        elif filter == "Salinity":
            data = Well.objects.filter(Salinity__range=(min_value, max_value))

        elif filter == "Resistivity":
            data = Well.objects.filter(Resistivity__range=(min_value, max_value))
        data_list = list(data.values())

    # condition pour variable Amendment
    elif variable == "Amendment":
        if filter == "Id_amendment":
            data = Amendment.objects.filter(Id_amendment__range=(min_value, max_value))

        elif filter == "Name":
            data = Amendment.objects.filter(Name__range=(min_value, max_value))

        elif filter == "Lu_lc":
            data = Amendment.objects.filter(Lu_lc__range=(min_value, max_value))

        elif filter == "Date_collect":
            data = Amendment.objects.filter(Date_collect__range=(min_value, max_value))

        elif filter == "Ph":
            data = Amendment.objects.filter(Ph__range=(min_value, max_value))

        elif filter == "Ec":
            data = Amendment.objects.filter(Ec__range=(min_value, max_value))

        data_list = list(data.values())

    




    

    


    
    return JsonResponse(data_list, safe=False)

