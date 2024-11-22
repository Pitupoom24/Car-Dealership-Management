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
from rest_framework import viewsets, permissions, status
from .serializer import CarsSerializer
from .models import *

# @api_view(['GET'])
# def get_cars(request):
#     limit = int(request.GET.get('limit', 10))  # Default limit = 10
#     offset = int(request.GET.get('offset', 0))  # Default offset = 0

#     # Use raw SQL query with limit and offset
#     query = f"SELECT * FROM Cars LIMIT {limit} OFFSET {offset}"

#     # Execute the raw query
#     with connection.cursor() as cursor:
#         cursor.execute(query)
#         columns = [col[0].lower() for col in cursor.description]  # Extract column names
#         results = [dict(zip(columns, row)) for row in cursor.fetchall()]

#     return Response(results)

class CarsViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = CarsSerializer

    def list(self, request):
        # Extract query parameters for limit and offset
        limit = int(request.GET.get('limit', 10))  # Default limit = 10
        offset = int(request.GET.get('offset', 0))  # Default offset = 0

        # Use raw SQL query with limit and offset
        query = f"SELECT * FROM Cars LIMIT {limit} OFFSET {offset}"

        # Execute the raw query
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0].lower() for col in cursor.description]  # Extract column names
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]  # Convert rows to dictionaries

        return Response(results)
    



    def create(self, request):
        # Extract data from the request
        data = request.data
        
        # Prepare the insert query with fields from the table description
        query = """
            INSERT INTO Cars (VIN, color, price, mileage, status, make, model, year, locationID, lastModifiedBy, warrantyID) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # Prepare the parameters to be inserted into the database
        params = [
            data.get('vin'),
            data.get('color', None),
            data.get('price', None),
            data.get('mileage', None),
            data.get('status', None),
            data.get('make'), 
            data.get('model'), 
            data.get('year'), 
            data.get('locationid'),
            data.get('lastmodifiedby'),
            data.get('warrantyid', None)
        ]

        # Execute the raw insert query
        with connection.cursor() as cursor:
            cursor.execute(query, params)

        # Return the newly created object data (or a success response)
        return Response(data, status=status.HTTP_201_CREATED)




    def update(self, request, pk=None):
        # Extract data from the request
        data = request.data

        # Prepare the update query
        query = """
            UPDATE Cars
            SET color=%s, price=%s, mileage=%s, status=%s, make=%s, model=%s, year=%s, locationID=%s, lastModifiedBy=%s, warrantyID=%s
            WHERE VIN=%s
        """

        # Prepare the parameters to be updated
        params = [
            data.get('color', None),
            data.get('price', None),
            data.get('mileage', None),
            data.get('status', None),
            data.get('make', None),
            data.get('model', None),
            data.get('year', None),
            data.get('locationid', None),
            data.get('lastmodifiedby', None),
            data.get('warrantyid', None),
            pk  # Use the primary key (VIN) from the URL parameter
        ]

        # Execute the raw update query
        with connection.cursor() as cursor:
            cursor.execute(query, params)

        # Return the updated object data as a response
        updated_data = {
            "vin": pk,
            "color": data.get('color', None),
            "price": data.get('price', None),
            "mileage": data.get('mileage', None),
            "status": data.get('status', None),
            "make": data.get('make', None),
            "model": data.get('model', None),
            "year": data.get('year', None),
            "locationid": data.get('locationid', None),
            "lastmodifiedby": data.get('lastmodifiedby', None),
            "warrantyid": data.get('warrantyid', None)
        }

        return Response(updated_data, status=status.HTTP_200_OK)
    


    def retrieve(self, request, pk=None):
        # Define the query to get a specific car based on its VIN
        query = """
            SELECT *
            FROM Cars
            WHERE VIN=%s
        """

        # Execute the query with the primary key (VIN)
        with connection.cursor() as cursor:
            cursor.execute(query, [pk])  # Pass the VIN as a parameter to prevent SQL injection
            columns = [col[0].lower() for col in cursor.description]  # Get the column names
            result = cursor.fetchone()  # Get a single row

        # If a result is found, format it into a dictionary
        if result:
            car_data = dict(zip(columns, result))
            return Response(car_data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Car not found."}, status=status.HTTP_404_NOT_FOUND)
        


    def destroy(self, request, pk=None):
        query = """
            DELETE FROM Cars
            WHERE VIN=%s
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [pk])
            return Response(status=status.HTTP_204_NO_CONTENT)


