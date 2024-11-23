from rest_framework import serializers
from .models import Cars, Details, Employees, Locations, Reviews, Warranties

class CarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cars
        fields = '__all__'

    def validate_warrantyid(self, value):
        if value == '':
            return None  # or raise a ValidationError
        return value


class DetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = '__all__'


class EmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},  # Passwords should not be returned in API responses
        }


class LocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = '__all__'


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = '__all__'


class WarrantiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warranties
        fields = '__all__'
