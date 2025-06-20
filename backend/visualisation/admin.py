from django.contrib import admin
from .models import soilSample, soilQuality, soilTexture, salinityAndSodicityGroup, Well,Amendment


# Register your models here.

# from import_export.admin import ImportExportModelAdmin
# from .models import soilSample, soilQuality, soilTexture, salinityAndSodicityGroup, Well
# from .resources import soilSampleResource

# class soilSampleAdmin(ImportExportModelAdmin):
#     resource_class = soilSampleResource
#     list_display = ('Code_labo', 'Latitude', 'Longitude', 'Depth', 'Date_collect', 'Date_edition')

# class soilQualityAdmin(ImportExportModelAdmin):
#     pass

# class soilTextureAdmin(ImportExportModelAdmin):
#     pass

# class salinityAndSodicityGroupAdmin(ImportExportModelAdmin):
#     pass

# class WellAdmin(ImportExportModelAdmin):
#     pass

# admin.site.register(soilSample, soilSampleAdmin)
# admin.site.register(soilQuality, soilQualityAdmin)
# admin.site.register(soilTexture, soilTextureAdmin)
# admin.site.register(salinityAndSodicityGroup, salinityAndSodicityGroupAdmin)
# admin.site.register(Well, WellAdmin)

admin.site.register(soilSample)
admin.site.register(soilQuality)
admin.site.register(soilTexture)
admin.site.register(salinityAndSodicityGroup)
admin.site.register(Well)
admin.site.register(Amendment)



