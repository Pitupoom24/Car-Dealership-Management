from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('cars', CarsViewSet, basename='cars')
router.register('reviews', ReviewsViewSet, basename='reviews')
router.register('details', DetailsViewSet, basename='details')
router.register('advanced_queries', AdvancedQueriesViewSet, basename='advanced_queries')
router.register('users', UsersViewSet, basename='users')
router.register('employees', EmployeesViewSet, basename='employees')
router.register('locations', LocationsViewSet, basename='locations')
urlpatterns = router.urls



### edit pls
# urlpatterns = [
#     path('cars/', get_cars, name='get_cars'),
# ]
