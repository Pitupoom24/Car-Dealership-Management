from django.db import connection
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from .serializer import *
from .models import *



############################################################################################################
################################################### Cars ###################################################
############################################################################################################
class CarsViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = CarsSerializer

    def list(self, request):
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))
        query = f"SELECT * FROM Cars LIMIT {limit} OFFSET {offset}"

        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0].lower() for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()] 

        return Response(results, status=status.HTTP_200_OK)
        
    
    def create(self, request):
        data = request.data
        
        query = """
            INSERT INTO Cars (VIN, color, price, mileage, status, make, model, year, locationID, lastModifiedBy, warrantyID) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
    
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

        with connection.cursor() as cursor:
            cursor.execute(query, params)

        return Response(data, status=status.HTTP_201_CREATED)


    def update(self, request, pk=None):
        data = request.data

        query = """
            UPDATE Cars
            SET VIN=%s, color=%s, price=%s, mileage=%s, status=%s, make=%s, model=%s, year=%s, locationID=%s, lastModifiedBy=%s, warrantyID=%s
            WHERE VIN=%s
        """

        params = [
            data.get('vin', None),
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
            pk # use pk for VIN
        ]

        with connection.cursor() as cursor:
            cursor.execute(query, params)


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
        query = """
            SELECT *
            FROM Cars
            WHERE VIN=%s
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [pk]) 
            columns = [col[0].lower() for col in cursor.description]
            result = cursor.fetchone()

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
        


############################################################################################################
################################################# Reviews ##################################################
############################################################################################################
class ReviewsViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = ReviewsSerializer

    def list(self, request):
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))
        query = f"SELECT * FROM Reviews ORDER BY reviewID LIMIT {limit} OFFSET {offset}"

        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0].lower() for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()] 

        return Response(results, status=status.HTTP_200_OK)
    

    def create(self, request):
        data = request.data
        
        query = """
            INSERT INTO Reviews (rating, comment, make, model, year) 
            VALUES (%s, %s, %s, %s, %s)
        """
    
        params = [
            data.get('rating'),
            data.get('comment', None),
            data.get('make'),
            data.get('model'), 
            data.get('year'), 
        ]

        with connection.cursor() as cursor:
            cursor.execute(query, params)

        return Response(data, status=status.HTTP_201_CREATED)
    

    def update(self, request, pk=None):
        data = request.data

        query = """
            UPDATE Reviews
            SET rating=%s, comment=%s, make=%s, model=%s, year=%s
            WHERE reviewID=%s
        """

        params = [
            data.get('rating', None),
            data.get('comment', None),
            data.get('make', None),
            data.get('model', None),
            data.get('year', None),
            pk # use pk for reviewID
        ]

        with connection.cursor() as cursor:
            cursor.execute(query, params)


        updated_data = {
            "reviewID": pk,
            "rating": data.get('rating'),
            "comment": data.get('comment', None),
            "make": data.get('make'),
            "model": data.get('model'),
            "year": data.get('year'),
        }

        return Response(updated_data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        query = """
            SELECT *
            FROM Reviews
            WHERE reviewID=%s
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [pk]) 
            columns = [col[0].lower() for col in cursor.description]
            result = cursor.fetchone()

        if result:
            car_data = dict(zip(columns, result))
            return Response(car_data, status=status.HTTP_200_OK)
        else:
            return Response({"reviewID": "reviewID not found."}, status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request, pk=None):
        query = """
            DELETE FROM Reviews
            WHERE reviewID=%s
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [pk])
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='retrieve_by_make_model_year')    
    def retrieve_by_make_model_year(self, request):
        make = request.GET.get('make')
        model = request.GET.get('model')
        year = request.GET.get('year')

        if not make or not model or not year:
            return Response({"detail": "Make, model, and year must be provided."}, status=status.HTTP_400_BAD_REQUEST)

        query = """
            SELECT *
            FROM Reviews
            WHERE make=%s AND model=%s AND year=%s
        """
        
        with connection.cursor() as cursor:
            cursor.execute(query, [make, model, year])
            columns = [col[0].lower() for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        if results:
            return Response(results, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No reviews found for the given make, model, and year."}, status=status.HTTP_404_NOT_FOUND)



############################################################################################################
################################################# Details ##################################################
############################################################################################################
class DetailsViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = DetailsSerializer

    def list(self, request):
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))
        query = f"SELECT * FROM Details LIMIT {limit} OFFSET {offset}"

        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0].lower() for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()] 

        return Response(results, status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data
        
        query = """
            INSERT INTO Details (make, model, year, numberOfCylinders, transmission, drivewheel) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
    
        params = [
            data.get('make'),
            data.get('model'), 
            data.get('year'), 
            data.get('numberofcylinders'), 
            data.get('transmission'), 
            data.get('drivewheel'), 
        ]

        with connection.cursor() as cursor:
            cursor.execute(query, params)

        return Response(data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        query = """
            SELECT *
            FROM Details
            WHERE id=%s
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [pk]) 
            columns = [col[0].lower() for col in cursor.description]
            result = cursor.fetchone()

        if result:
            car_data = dict(zip(columns, result))
            return Response(car_data, status=status.HTTP_200_OK)
        else:
            return Response({"id": "id not found."}, status=status.HTTP_404_NOT_FOUND)
        

    def destroy(self, request, pk=None):
        query = """
            DELETE FROM Details
            WHERE id=%s
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [pk])
            return Response(status=status.HTTP_204_NO_CONTENT)
        

    # ex. http://127.0.0.1:8000/api/details/retrieve_by_make_model_year/?make=acura&model=mdx&year=2011
    @action(detail=False, methods=['get'], url_path='retrieve_by_make_model_year')  
    def retrieve_by_make_model_year(self, request):
        make = request.GET.get('make')
        model = request.GET.get('model')
        year = request.GET.get('year')

        if not make or not model or not year:
            return Response({"detail": "Make, model, and year must be provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        query = """
            SELECT *
            FROM Details
            WHERE make=%s AND model=%s AND year=%s
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [make, model, year]) 
            columns = [col[0].lower() for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        if results:
            return Response(results, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No details found for the given make, model, and year."}, status=status.HTTP_404_NOT_FOUND)

    # ex. http://127.0.0.1:8000/api/details/destroy_by_make_model_year/?make=acura&model=mdx&year=2011    
    @action(detail=False, methods=['delete'], url_path='destroy_by_make_model_year')
    def destroy_by_make_model_year(self, request):
        make = request.GET.get('make')
        model = request.GET.get('model')
        year = request.GET.get('year')

        if not make or not model or not year:
            return Response({"detail": "Make, model, and year must be provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        query = """
            DELETE FROM Details
            WHERE make=%s AND model=%s AND year=%s
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [make, model, year])
            return Response(status=status.HTTP_204_NO_CONTENT)
        

    # ex http://127.0.0.1:8000/api/details/update_by_make_model_year/?make=test%20make&model=test%20model&year=9999
    @action(detail=False, methods=['put'], url_path='update_by_make_model_year')
    def update_by_make_model_year(self, request):
        data = request.data

        make = data.get('make')
        model = data.get('model')
        year = data.get('year')

        if not make or not model or not year:
            return Response({"detail": "Make, model, and year must be provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        query = """
            UPDATE Details
            SET numberOfCylinders=%s, transmission=%s, drivewheel=%s
            WHERE make=%s AND model=%s AND year=%s
        """

        params = (
            data.get('numberofcylinders') if data.get('numberofcylinders') else None,
            data.get('transmission') if data.get('transmission') else None,
            data.get('drivewheel') if data.get('drivewheel') else None,
            make,
            model,
            year,
        )

        with connection.cursor() as cursor:
            cursor.execute(query, params)
        
        updated_data = {
            "make": make,
            "model": model,
            "year": year,
            "numberofcylinders": data.get('numberofcylinders', None),
            "transmission": data.get('transmission', None),
            "drivewheel": data.get('drivewheel', None),
        }

        return Response(updated_data, status=status.HTTP_200_OK)



############################################################################################################
############################################# Advanced Queries #############################################
############################################################################################################
class AdvancedQueriesViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    # serializer_class = CarsSerializer

    # Advanced Query 1
    @action(detail=False, methods=['GET'])
    def top_of_list(self, request):
        query = """
            SELECT r.make, r.model, r.year, AVG(r.rating) AS averageRating
            FROM Reviews r
            GROUP BY r.make, r.model, r.year
            HAVING AVG(r.rating) >= ALL(
            SELECT AVG(r.rating)
            FROM Reviews r
            GROUP BY r.make, r.model, r.year) AND COUNT(r.rating) >= 3
        """

        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0].lower() for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return Response(results, status=status.HTTP_200_OK)
    

    # Advanced Query 2
    @action(detail=False, methods=['GET'])
    def vehicle_features_score(self, request):
        query = """
            SELECT c.VIN, (COUNT(c.mileage < 150000) + COUNT(c.year>2003) + COUNT(r.rating>=4)) / 3 AS Vehicle_Feature_Score
            FROM Cars c NATURAL JOIN Reviews r
            GROUP BY c.VIN
            ORDER BY c.VIN
            LIMIT 15
        """

        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0].lower() for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return Response(results, status=status.HTTP_200_OK)
    

    # Advanced Query 3
    @action(detail=False, methods=['GET'])
    def sales_trend_score(self, request):
        query = """
            SELECT c.VIN, temp2.Sales_Trend_Score
            FROM Cars c NATURAL JOIN
            (SELECT c.make, c.model, c.year, (COUNT(c.VIN) / temp.total) AS Sales_Trend_Score
            FROM Cars c JOIN
            (SELECT c.make, c.model, c.year, COUNT(c.VIN) AS total
            FROM Cars c GROUP BY c.make, c.model, c.year) AS temp
            ON (c.make = temp.make AND c.model = temp.model AND c.year = temp.year)
            WHERE c.status != 'available'
            GROUP BY c.make, c.model, c.year) AS temp2
            ORDER BY c.VIN
            LIMIT 15;
        """

        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0].lower() for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return Response(results, status=status.HTTP_200_OK)
    

    # Advanced Query 4
    @action(detail=False, methods=['GET'])
    def inventory_score(self, request):
        query = """
            SELECT c.VIN, temp2.Inventory_Score 
            FROM Cars c NATURAL JOIN 
            (SELECT c.make, c.model, c.year, (70* COUNT(c.VIN) / AVG(temp.total_not_sold)) AS Inventory_Score
            FROM Cars c, 
            (SELECT COUNT(*) AS total_not_sold
            FROM Cars c
            WHERE c.status = 'available') AS temp
            WHERE c.status = 'available'
            GROUP BY c.make, c.model, c.year) AS temp2
            ORDER BY c.VIN
            LIMIT 15;
        """

        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0].lower() for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return Response(results, status=status.HTTP_200_OK)
    
    # For Search Bar
    def list(self, request):

        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))

        data = request.GET

        make = data.get('make')
        model = data.get('model')
        year = data.get('year')
        numberofcylinders = data.get('numberofcylinders')
        transmission = data.get('transmission')
        drivewheel = data.get('drivewheel')
        vin = data.get('vin')
        color = data.get('color')
        lower_price = data.get('lower_price')
        higher_price = data.get('higher_price')
        lower_mileage = data.get('lower_mileage')
        higher_mileage = data.get('higher_mileage')
        _status = data.get('status')
        locationid = data.get('locationid')
        lastmodifiedby = data.get('lastmodifiedby')
        rating = data.get('rating')

        # INSERT INTO Warranties before using; otherwise, delete JOIN Warranties ...
        query = f"""
            SELECT *
            FROM Cars c JOIN Details d ON c.make=d.make AND c.model=d.model AND c.year=d.year 
                JOIN Warranties w ON c.warrantyID=w.warrantyID
                JOIN Reviews r ON r.make=d.make AND r.model=d.model AND r.year=d.year
                JOIN Employees e ON c.lastModifiedBy=e.employeeID
                JOIN Locations l ON l.locationID=c.locationID 
            WHERE 411=411
        """
        parameters = []

        # Dynamically add conditions
        if make:
            query += " AND d.make=%s"
            parameters.append(make)
        if model:
            query += " AND d.model=%s"
            parameters.append(model)
        if year:
            query += " AND d.year=%s"
            parameters.append(year)
        if numberofcylinders:
            query += " AND d.numberofcylinders=%s"
            parameters.append(numberofcylinders)
        if transmission:
            query += " AND d.transmission=%s"
            parameters.append(transmission)
        if drivewheel:
            query += " AND d.drivewheel=%s"
            parameters.append(drivewheel)
        if vin:
            query += " AND vin=%s"
            parameters.append(vin)
        if color:
            query += " AND color=%s"
            parameters.append(color)
        if lower_price:
            query += " AND price >= %s"
            parameters.append(lower_price)
        if higher_price:
            query += " AND price <= %s"
            parameters.append(higher_price)
        if lower_mileage:
            query += " AND mileage >= %s"
            parameters.append(lower_mileage)
        if higher_mileage:
            query += " AND mileage <= %s"
            parameters.append(higher_mileage)
        if _status:
            query += " AND status=%s"
            parameters.append(_status)
        if locationid:
            query += " AND locationid=%s"
            parameters.append(locationid)
        if lastmodifiedby:
            query += " AND lastmodifiedby=%s"
            parameters.append(lastmodifiedby)
        if rating:
            query += " AND rating=%s"
            parameters.append(rating)

        query += f" LIMIT {limit}"
        query += f" OFFSET {offset}"

        with connection.cursor() as cursor:
            cursor.execute(query, parameters)
            columns = [col[0].lower() for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()] 

        return Response(results, status=status.HTTP_200_OK)
    




