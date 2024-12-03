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
        
        query1 = """
            INSERT INTO Cars (VIN, color, price, mileage, status, make, model, year, locationID, lastModifiedBy) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
    
        params1 = [
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
        ]

        query2 = """
            INSERT INTO Warranties (warrantyID, startDate, endDate, coverageDetail, VIN) 
            VALUES (%s, %s, %s, %s, %s)
        """
        
        if data.get('warrantyid', None) is not None:
            param2 = [
                data.get('warrantyid', None),
                data.get('startdate'),
                data.get('enddate'),
                data.get('coveragedetail', None),
                data.get('vin'),
            ]

        with connection.cursor() as cursor:
            cursor.execute(query1, params1)
            if data.get('warrantyid', None) is not None:
                cursor.execute(query2, param2)
                cursor.execute("UPDATE Cars SET warrantyID = %s WHERE VIN = %s", [data.get('warrantyid', None), data.get('vin')])
 

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
    
    ##################################################
    ##################################################
    ##################################################
    # Combined Advanced Queries - calculate the total score
    # ex http://127.0.0.1:8000/api/advanced_queries/total_score/?weight1=0.2&weight2=0.3&weight3=0.1&weight4=0.4&higher_price=5000&higher_mileage=150000&transmission=Automatic&drivewheel=Front&limit=10&offset=0
    @action(detail=False, methods=['GET'], url_path='total_score')
    def total_score(self, request):
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))

        data = request.GET

        params = (
            data.get('weight1'),
            data.get('weight2'),
            data.get('weight3'),
            data.get('weight4'),
            data.get('higher_price'),
            data.get('higher_mileage'),
            data.get('transmission'),
            data.get('drivewheel'),
        )

        with connection.cursor() as cursor:
            cursor.execute("CALL VehicleDisplayOptimizer(%s, %s, %s, %s, %s, %s, %s, %s);", params)

            cursor.execute("""
                SELECT *
                FROM Cars c NATURAL JOIN TempDisplayScores s
                ORDER BY s.totalScore DESC
                LIMIT %s
                OFFSET %s;
            """, (limit, offset))

            columns = [col[0].lower() for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return Response(results, status=status.HTTP_200_OK)
    
    ##################################################
    ##################################################
    ##################################################
    # Adjust Prices
    # ex http://127.0.0.1:8000/api/advanced_queries/adjust_car_prices/
    @action(detail=False, methods=['put'], url_path='adjust_car_prices')
    def adjust_car_prices(self, request):
        data = request.data

        percent_increase = data.get('percent_increase')
        percent_decrease = data.get('percent_decrease')

        if not percent_increase or not percent_decrease:
            return Response({"detail": "Percent Increase/Percent Decrease must be provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        with connection.cursor() as cursor:
            cursor.execute("CALL AdjustCarPrices(%s, %s)", [percent_increase, percent_decrease])

        return Response({"Success": "Prices have already been adjusted."}, status=status.HTTP_200_OK)
    


    
    # For Search Bar
    # ex http://127.0.0.1:8000/api/advanced_queries/?make=bmw&limit=10&higher_year=2005&lower_rating=2&higher_rating=4
    def list(self, request):

        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))

        data = request.GET

        make = data.get('make')
        model = data.get('model')
        lower_year = data.get('lower_year')
        higher_year = data.get('higher_year')
        lower_numberofcylinders = data.get('lower_numberofcylinders')
        higher_numberofcylinders = data.get('higher_numberofcylinders')
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
        lower_rating = data.get('lower_rating')
        higher_rating = data.get('higher_rating')


        query = f"""
            SELECT c.vin, c.make, c.model, c.year, c.color, c.price, c.mileage, c.status, c.locationid, c.lastmodifiedby, c.warrantyid, r.averageRating
            FROM Cars c
                LEFT JOIN Details d ON c.make=d.make AND c.model=d.model AND c.year=d.year 
                LEFT JOIN 
                (
                SELECT AVG(re.rating) AS averageRating, re.make, re.model, re.year
                FROM Reviews re
                GROUP BY re.make, re.model, re.year
                ) AS r ON r.make=c.make AND r.model=c.model AND r.year=c.year
                LEFT JOIN Employees e ON c.lastModifiedBy=e.employeeID
                LEFT JOIN Locations l ON l.locationID=c.locationID
                LEFT JOIN Warranties w ON w.warrantyID=c.warrantyID
            WHERE 411=411
        """

        parameters = []

        if make:
            query += " AND c.make=%s"
            parameters.append(make)
        if model:
            query += " AND c.model=%s"
            parameters.append(model)
        if lower_year:
            query += " AND c.year>=%s"
            parameters.append(lower_year)
        if higher_year:
            query += " AND c.year<=%s"
            parameters.append(higher_year)
        if lower_numberofcylinders:
            query += " AND d.numberofcylinders>=%s"
            parameters.append(lower_numberofcylinders)
        if higher_numberofcylinders:
            query += " AND d.numberofcylinders<=%s"
            parameters.append(higher_numberofcylinders)
        if transmission:
            query += " AND d.transmission=%s"
            parameters.append(transmission)
        if drivewheel:
            query += " AND d.drivewheel=%s"
            parameters.append(drivewheel)
        if vin:
            query += " AND c.vin=%s"
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
        if lower_rating:
            query += " AND averageRating >= %s"
            parameters.append(lower_rating)
        if higher_rating:
            query += " AND averageRating <= %s"
            parameters.append(higher_rating)

        query += f" LIMIT {limit}"
        query += f" OFFSET {offset}"

        with connection.cursor() as cursor:
            cursor.execute(query, parameters)
            columns = [col[0].lower() for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()] 

        return Response(results, status=status.HTTP_200_OK)
    

############################################################################################################
############################################### User Queries ###############################################
############################################################################################################
class UsersViewSet(viewsets.ViewSet):

    permission_classes = [permissions.AllowAny]

    def create(self, request):
        data = request.data
        
        query = """
            INSERT INTO Employees (employeeID, firstName, lastName , email, password, locationID) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
    
        params = [
            data.get('employeeid'),
            data.get('firstName'), 
            data.get('lastName'), 
            data.get('email'), 
            data.get('password'), 
            data.get('locationid'), 
        ]

        with connection.cursor() as cursor:
            cursor.execute(query, params)

        return Response(data, status=status.HTTP_201_CREATED)
    

    # ex http://127.0.0.1:8000/api/users/login/?employeeid=1&password=smithjosh123
    @action(detail=False, methods=['GET'], url_path='login')
    def login(self, request):
        employeeid = request.GET.get('employeeid')
        password = request.GET.get('password')

        # if is_valid = 1, it's valid. Otherwise, it's invalid
        query = """
            SELECT e.employeeID, COUNT(*) AS is_valid
            FROM Employees e
            WHERE e.employeeID = %s AND e.password = %s
        """


        with connection.cursor() as cursor:
            cursor.execute(query, [employeeid, password]) 
            columns = [col[0].lower() for col in cursor.description]
            result = cursor.fetchone()

        if result:
            user_data = dict(zip(columns, result))
            return Response(user_data, status=status.HTTP_200_OK)
        else:
            return Response({"result": "user/password is not correct"}, status=status.HTTP_404_NOT_FOUND)

############################################################################################################
################################################ Employees #################################################
############################################################################################################
class EmployeesViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, pk=None):
        query = """
            SELECT *
            FROM Employees e
            WHERE e.employeeID=%s
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [pk]) 
            columns = [col[0].lower() for col in cursor.description]
            result = cursor.fetchone()

        if result:
            employee_data = dict(zip(columns, result))
            return Response(employee_data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)
        
############################################################################################################
################################################ Locations #################################################
############################################################################################################
class LocationsViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, pk=None):
        query = """
            SELECT *
            FROM Locations l
            WHERE l.locationID=%s
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [pk]) 
            columns = [col[0].lower() for col in cursor.description]
            result = cursor.fetchone()

        if result:
            location_data = dict(zip(columns, result))
            return Response(location_data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Location not found."}, status=status.HTTP_404_NOT_FOUND)
        
############################################################################################################
################################################ Warranties ################################################

############################################################################################################
class WarrantiesViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, pk=None):
        query = """
            SELECT *
            FROM Warranties w
            WHERE w.warrantyID=%s
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [pk]) 
            columns = [col[0].lower() for col in cursor.description]
            result = cursor.fetchone()

        if result:
            warranty_data = dict(zip(columns, result))
            return Response(warranty_data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Warranty not found."}, status=status.HTTP_404_NOT_FOUND)