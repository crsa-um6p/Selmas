from django.urls import path
from . import views

urlpatterns = [
    path("get_data/", views.get_data, name="get_data"),
    path("dashboard_data/", views.dashboard_data, name="dashboard_data"),
    # path("dashboard_data_optimized/", views.dashboard_data_optimized, name="dashboard_data_optimized"),
    path("fill_soil_sample_table/", views.fill_soil_sample_table, name="fill_soil_sample_table"),
    path("fill_soil_texture/", views.fill_soil_texture, name="fill_soil_texture"),
    path("fill_soil_quality/", views.fill_soil_quality, name="fill_soil_quality"),
    path("fill_salinityandsodicitygroup/", views.fill_salinityandsodicitygroup, name="fill_salinityandsodicitygroup"),
]

