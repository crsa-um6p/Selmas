from django.core.management.base import BaseCommand
from visualisation.models import salinityAndSodicityGroup, soilSample
import pandas as pd

class Command(BaseCommand):
    help = 'Importer les données depuis le fichier Excel vers la table soilTexture'

    def handle(self, *args, **kwargs):
        path = r'D:\Géoportail_SELMAS\backend\visualisation\data\salinity_Sodicity.xlsx' 

        try:
            df = pd.read_excel(path)
            print(df.columns)
            self.stdout.write(self.style.SUCCESS(f"Lecture du fichier Excel réussie. Colonnes: {df.columns}"))

            for index, row in df.iterrows():
                try:
        
                    sample = soilSample.objects.get(Code_labo=row['code_Labo'])

                    salinityAndSodicityGroup.objects.update_or_create(
                        Code_labo=sample,
                        defaults={
                            'Ec1_5': row['Ec1_5'],
                            'Ec_pate_sature': row['Ec_pate_sature'],
                            'Sar': row['Sar'],
                            'Sar_interpretation': row['Sar_interpretation'],
                            'Esp': row['Esp'],
                            'Esp_interpretation': row['Esp_interpretation'],
                            'Esp_Ec_interpretation': row['Esp_Ec_interpretation'],
                            'Cl': row['Cl'],
                            'Classification': row['Classification'],
                        }
                    )
                except soilSample.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"code_Labo '{row['code_Labo']}' introuvable dans soilSample. Skipping."))

            self.stdout.write(self.style.SUCCESS("Importation des données dans soilTexture réussie !"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erreur lors de l'importation : {e}"))
