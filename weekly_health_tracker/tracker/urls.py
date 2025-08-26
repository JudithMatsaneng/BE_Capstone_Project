from django.urls import path
from .views import WeeklySummaryView

urlpatterns = [
    path("weekly-summary/", WeeklySummaryView.as_view(), name="weekly-summary"),
]
