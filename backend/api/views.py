from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Cars
from .serializer import CarsSerializer

# Create your views here.
@api_view(['GET'])                  # GET >> read data
def get_cars(request):
    cars = Cars.objects.all()
    serializedData = CarsSerializer(cars, many=True).data      # since books = array of object (so many!)
    return Response(serializedData)