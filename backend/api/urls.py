from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('cars', CarsViewSet, basename='cars')
router.register('reviews', ReviewsViewSet, basename='reviews')
router.register('details', DetailsViewSet, basename='details')
router.register('advanced_queries', AdvancedQueriesViewSet, basename='advanced_queries')
router.register('users', UsersViewSet, basename='users')
router.register('employees', EmployeeViewSet, basename='employees')
router.register('locations', LocationViewSet, basename='locations')
router.register('warranties', WarrantiesViewSet, basename='warranties')

urlpatterns = [
    path('', include(router.urls)),
]

#urlpatterns = router.urls



### edit pls
# urlpatterns = [
#     path('cars/', get_cars, name='get_cars'),
# ]
