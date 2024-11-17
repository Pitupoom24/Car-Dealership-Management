from django.urls import path
from .views import get_cars
### edit pls
urlpatterns = [
    path('cars/', get_cars, name='get_cars'),
]
