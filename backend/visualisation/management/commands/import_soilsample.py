from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from visualisation.models import soilSample
import pandas as pd
from datetime import datetime

class Command(BaseCommand):
    help = 'Importer les données depuis le fichier Excel vers la table soilSample'

    def handle(self, *args, **kwargs):
        
        path = 'D:/Géoportail_SELMAS/backend/visualisation/data/soilSample.xlsx'
  

        try:
            df = pd.read_excel(path)
            print(df.columns)
            self.stdout.write(self.style.SUCCESS("Lecture du fichier Excel réussie."))


            for index, row in df.iterrows():
                # ca cest pour longitude et latitude
                point = Point(row['Latitude'], row['Longitude'], srid=4326)

                soilSample.objects.update_or_create(
                    Code_labo=row['code_Labo'],
                    defaults={
                        'localisation': point,
                        'Depth': row['Depth'],
                        'Date_collect': pd.to_datetime(row['date_Collect']).date() if pd.notnull(row['date_Collect']) else None,
                        'Date_edition': pd.to_datetime(row['date_edition']).date() if pd.notnull(row['date_edition']) else None,

                    }
                )

            self.stdout.write(self.style.SUCCESS("Importation réussie !"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erreur lors de l'importation : {e}"))
