from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('cars', CarsViewSet, basename='cars')
urlpatterns = router.urls



### edit pls
# urlpatterns = [
#     path('cars/', get_cars, name='get_cars'),
# ]
