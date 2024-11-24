from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('cars', CarsViewSet, basename='cars')
router.register('reviews', ReviewsViewSet, basename='reviews')
router.register('details', DetailsViewSet, basename='details')
router.register('advanced_queries', AdvancedQueriesViewSet, basename='advanced_queries')
urlpatterns = router.urls



### edit pls
# urlpatterns = [
#     path('cars/', get_cars, name='get_cars'),
# ]
