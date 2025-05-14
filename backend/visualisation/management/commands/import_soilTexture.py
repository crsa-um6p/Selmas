from django.core.management.base import BaseCommand
from visualisation.models import soilTexture, soilSample
import pandas as pd

class Command(BaseCommand):
    help = 'Importer les données depuis le fichier Excel vers la table soilTexture'

    def handle(self, *args, **kwargs):
        path = 'D:/Géoportail_SELMAS/backend/visualisation/data/soilTexture.xlsx' 

        try:
            df = pd.read_excel(path)
            print(df.columns)
            self.stdout.write(self.style.SUCCESS(f"Lecture du fichier Excel réussie. Colonnes: {df.columns}"))

            for index, row in df.iterrows():
                try:
        
                    sample = soilSample.objects.get(Code_labo=row['code_Labo'])

                    soilTexture.objects.update_or_create(
                        Code_labo=sample,
                        defaults={
                            'Argile': row['Argile'],
                            'Lemon': row['Lemon'],
                            'Sable': row['Sable'],
                            'Soil_texture_v4': row['Soil_Texture_v4'],
                        }
                    )
                except soilSample.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"code_Labo '{row['code_Labo']}' introuvable dans soilSample. Skipping."))

            self.stdout.write(self.style.SUCCESS("Importation des données dans soilTexture réussie !"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erreur lors de l'importation : {e}"))
