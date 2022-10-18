
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('search/', views.search_results, name="search"),
    path('fetch_address_of_city', views.fetch_address_of_city, name="fetch_address_of_city")


]
