from django.core.management.base import BaseCommand
from visualisation.models import soilQuality, soilSample
import pandas as pd

class Command(BaseCommand):
    help = 'Importer les données depuis le fichier Excel vers la table soilTexture'

    def handle(self, *args, **kwargs):
        path = r'D:\Géoportail_SELMAS\backend\visualisation\data\sol_Quality.xlsx' 

        try:
            df = pd.read_excel(path)
            print(df.columns)
            self.stdout.write(self.style.SUCCESS(f"Lecture du fichier Excel réussie. Colonnes: {df.columns}"))

            for index, row in df.iterrows():
                try:
        
                    sample = soilSample.objects.get(Code_labo=row['code_Labo'])

                    soilQuality.objects.update_or_create(
                        Code_labo=sample,
                        defaults={
                            'Ph_level': row[' PH-eau'],
                            'Organic_matter': row['MO'],
                            'Cu': row['Cu'],
                            'Mn': row['Mn'],
                            'Fe': row['Fe'],
                            'Zn': row['Zn'],
                            'NNH4':row['NNH4 '],
                            'NO3' : row['NO3 '],
                            'NT': row['Nt'],
                            'P2O5': row['P2O5'],
                            'k2o': row['K2O'],
                        }
                    )
                except soilSample.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"code_Labo '{row['code_Labo']}' introuvable dans soilSample. Skipping."))

            self.stdout.write(self.style.SUCCESS("Importation des données dans soilTexture réussie !"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erreur lors de l'importation : {e}"))
