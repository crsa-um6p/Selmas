from django.shortcuts import render

from .models import Puit
from django.contrib.gis.geos import Point
from datetime import date

import pandas

from django.http import HttpResponse

# Create your views here.


# def add_puit(request):

#     # Puit.objects.create(geometry=Point(1, 1), date=date.today())

#     data = pandas.read_excel("data.xlsx")

#     for index, row in data.iterrows():
#         Puit.objects.create(geometry=Point(row['x'], row['y']), date=row['date'])

#     return HttpResponse("Puits added")
