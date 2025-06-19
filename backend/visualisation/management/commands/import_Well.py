from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from visualisation.models import Well
import pandas as pd
from datetime import datetime

class Command(BaseCommand):
    help = 'Importer les données depuis le fichier Excel vers la table soilSample'

    def handle(self, *args, **kwargs):
        
        path = r'D:\Géoportail_SELMAS\backend\visualisation\data\Wells.xlsx'
  

        try:
            df = pd.read_excel(path)
            print(df.columns)
            self.stdout.write(self.style.SUCCESS("Lecture du fichier Excel réussie."))


            for index, row in df.iterrows():
                # ca cest pour longitude et latitude
                point = Point(row['Longitude'], row['Latitude'], srid=4326)

                Well.objects.update_or_create(
                        Id_well=row['Id_well'],
                        defaults={
                            'Date': pd.to_datetime(row['Date']).date() if pd.notnull(row['Date']) else None,
                            'localisation': point,
                            'Depth': row['Depth'],
                            'Water_depth': row['Water_depth'],
                            'Pump_cal': row['Pump_cal'],
                            'Temperature': row['Temperature'],
                            'Ph': row['Ph'],
                            'Ec': row['Ec'],
                            'Tds_ppm': row['Tds_ppm'],
                            'Salinity': row['Salinity'],
                            'Resistivity': row['Resistivity'],
                        }
                    )

            self.stdout.write(self.style.SUCCESS("Importation réussie !"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erreur lors de l'importation : {e}"))
