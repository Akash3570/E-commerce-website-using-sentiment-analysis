from django.urls import path

from .views import review_analysis


app_name = "reviews"

urlpatterns = [
    path("analysis/", review_analysis, name="review_analysis"),
]
