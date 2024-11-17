# from django.shortcuts import render
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Cars
# from .serializer import CarsSerializer

# # # Create your views here.
# @api_view(['GET'])                  # GET >> read data
# def get_cars(request):
#     cars = Cars.objects.raw('SELECT * FROM Cars LIMIT 10')
#     serializedData = CarsSerializer(cars, many=True).data      # since books = array of object (so many!)
#     return Response(serializedData)

from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import CarsSerializer

@api_view(['GET'])
def get_cars(request):
    limit = int(request.GET.get('limit', 10))  # Default limit = 10
    offset = int(request.GET.get('offset', 0))  # Default offset = 0

    # Use raw SQL query with limit and offset
    query = f"SELECT * FROM Cars LIMIT {limit} OFFSET {offset}"

    # Execute the raw query
    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0].lower() for col in cursor.description]  # Extract column names
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return Response(results)
