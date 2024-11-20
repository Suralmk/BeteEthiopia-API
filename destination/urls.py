from django.urls import path
from . views import *

urlpatterns = [
    path("destinations/", DestinationView.as_view(), name="destination_list"),
    path("destinations/<int:id>/", DestinationDetailView.as_view(), name="destination_detail"),
    path("prices/<int:destination_id>/<int:agent_id>/", PricesView.as_view(), name="price_view"),
    path("categories/", CategoriesView.as_view(), name="categories"),
]