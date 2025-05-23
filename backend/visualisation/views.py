from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import pandas
import json
from .models import *
from django.views.decorators.csrf import csrf_exempt
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

