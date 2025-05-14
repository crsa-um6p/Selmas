from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from visualisation.models import Amendment
import pandas as pd
from datetime import datetime

class Command(BaseCommand):
    help = 'Importer les données depuis le fichier Excel vers la table soilSample'

    def handle(self, *args, **kwargs):
        
        path = r'D:\Géoportail_SELMAS\backend\visualisation\data\Amendemenet.xlsx'
  

        try:
            df = pd.read_excel(path)
            print(df.columns)
            self.stdout.write(self.style.SUCCESS("Lecture du fichier Excel réussie."))


            for index, row in df.iterrows():
                # ca cest pour longitude et latitude
                point = Point(row['X'], row['Y'], srid=4326)

                Amendment.objects.update_or_create(

                    Id_amendment=row['ID'],  

                    defaults={
                        'localisation': point,
                        'Name': row['Name'],
                        'Lu_lc': row['LU/LC'],
                        'Date_collect': pd.to_datetime(row['Date de collecte']).date() if pd.notnull(row['Date de collecte']) else None,
                        'Ph': row['PH'],
                        'Ec': row['EC'],
                        'Salinity_level': row['Salinity level'],
                        'Classe': row['Classe'],
                        'Cao': row['CaO'],
                        'Sio2': row['SiO2'],
                        'Al2o3': row['Al2o3'],
                        'Fe2o3': row['Fe2o3'],
                        'Mgo': row['MgO'],
                        'K2o': row['K2O'],
                        'Na2o': row['Na2O'],
                        'Ttio2': row['TiO2'],
                        'P2o5': row['P2O5'],
                        'Mno': row['MnO'],
                        'S': row['S'],
                        'Clay': row['clay'],
                        'Silt': row['silt'],
                        'Sand': row['sand'],
                        'Wc': row['wc'],
                    }
                )

            self.stdout.write(self.style.SUCCESS("Importation réussie !"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erreur lors de l'importation : {e}"))
