# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Cars(models.Model):
    vin = models.CharField(db_column='VIN', primary_key=True, max_length=17)  # Field name made lowercase.
    color = models.CharField(max_length=30, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    mileage = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)

    # make = models.CharField(max_length=50, blank=True, null=True)
    # model = models.CharField(max_length=50, blank=True, null=True)
    # year = models.IntegerField(blank=True, null=True)
    make = models.ForeignKey('Details', on_delete=models.SET_NULL, db_column='make', blank=True, null=True)
    model = models.ForeignKey('Details', on_delete=models.SET_NULL, db_column='model', related_name='cars_model_set', blank=True, null=True)
    year = models.ForeignKey('Details', on_delete=models.SET_NULL, db_column='year', related_name='cars_year_set', blank=True, null=True)

    locationid = models.ForeignKey('Locations', on_delete=models.CASCADE, db_column='locationID')  # Field name made lowercase.
    lastmodifiedby = models.ForeignKey('Employees', on_delete=models.CASCADE, db_column='lastModifiedBy')  # Field name made lowercase.
    warrantyid = models.ForeignKey('Warranties', on_delete=models.SET_NULL, db_column='warrantyID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Cars'

# class Cars(models.Model):
#     vin = models.CharField(db_column='VIN', primary_key=True, max_length=17)
#     color = models.CharField(max_length=30, blank=True, null=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     mileage = models.IntegerField(blank=True, null=True)
#     status = models.CharField(max_length=50, blank=True, null=True)
#     details = models.ForeignKey('Details', on_delete=models.DO_NOTHING, db_column='details')
#     locationid = models.ForeignKey('Locations', on_delete=models.DO_NOTHING, db_column='locationID')
#     lastmodifiedby = models.ForeignKey('Employees', on_delete=models.DO_NOTHING, db_column='lastModifiedBy')
#     warrantyid = models.ForeignKey('Warranties', on_delete=models.DO_NOTHING, db_column='warrantyID', blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'Cars'

class Details(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly define the primary key
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    numberofcylinders = models.IntegerField(db_column='numberOfCylinders', blank=True, null=True)
    transmission = models.CharField(max_length=50, blank=True, null=True)
    drivewheel = models.CharField(db_column='driveWheel', max_length=50, blank=True, null=True)

    class Meta:
        managed = False  # Django will not manage the creation or modification of this table
        db_table = 'Details'  # Map to the existing 'Details' table in the database
        # unique_together = ('make', 'model', 'year')  # Enforce uniqueness on these fields
        constraints = [
            models.UniqueConstraint(fields=['make', 'model', 'year'], name='unique_details')
        ]

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"

# class Details(models.Model):
#     make = models.CharField(primary_key=True, max_length=50)  # The composite primary key (make, model, year) found, that is not supported. The first column is selected.
#     model = models.CharField(max_length=50)
#     year = models.IntegerField()
#     numberofcylinders = models.IntegerField(db_column='numberOfCylinders', blank=True, null=True)  # Field name made lowercase.
#     transmission = models.CharField(max_length=50, blank=True, null=True)
#     drivewheel = models.CharField(db_column='driveWheel', max_length=50, blank=True, null=True)  # Field name made lowercase.

#     class Meta:
#         managed = False
#         db_table = 'Details'
#         unique_together = (('make', 'model', 'year'),)
        # constraints = [
        #     models.UniqueConstraint(fields=['make', 'model', 'year'], name='unique_details')
        # ]


class Employees(models.Model):
    employeeid = models.IntegerField(db_column='employeeID', primary_key=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='firstName', max_length=50)  # Field name made lowercase.
    lastname = models.CharField(db_column='lastName', max_length=50)  # Field name made lowercase.
    email = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=255)
    locationid = models.ForeignKey('Locations', on_delete=models.CASCADE, db_column='locationID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Employees'


class Locations(models.Model):
    locationid = models.IntegerField(db_column='locationID', primary_key=True)  # Field name made lowercase.
    address = models.CharField(max_length=255, blank=True, null=True)
    phonenumber = models.CharField(db_column='phoneNumber', max_length=15, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Locations'


class Reviews(models.Model):
    reviewid = models.IntegerField(db_column='reviewID', primary_key=True)  # Field name made lowercase.
    rating = models.IntegerField(blank=True, null=True)
    comment = models.CharField(max_length=1000, blank=True, null=True)
    # details = models.ForeignKey('Details', on_delete=models.DO_NOTHING, db_column='details')
    make = models.ForeignKey(Details, on_delete=models.CASCADE, db_column='make')
    model = models.ForeignKey(Details, on_delete=models.CASCADE, db_column='model', related_name='reviews_model_set')
    year = models.ForeignKey(Details, on_delete=models.CASCADE, db_column='year', related_name='reviews_year_set')

    class Meta:
        managed = False
        db_table = 'Reviews'


class Warranties(models.Model):
    warrantyid = models.IntegerField(db_column='warrantyID', primary_key=True)  # Field name made lowercase.
    startdate = models.DateField(db_column='startDate')  # Field name made lowercase.
    enddate = models.DateField(db_column='endDate')  # Field name made lowercase.
    coveragedetail = models.CharField(db_column='coverageDetail', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    vin = models.ForeignKey(Cars, on_delete=models.CASCADE, db_column='VIN')  # Field name made lowercase.
    reviewid = models.ForeignKey(Reviews, on_delete=models.CASCADE, db_column='reviewID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Warranties'


# class AuthGroup(models.Model):
#     name = models.CharField(unique=True, max_length=150)

#     class Meta:
#         managed = False
#         db_table = 'auth_group'


# class AuthGroupPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#     permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'auth_group_permissions'
#         unique_together = (('group', 'permission'),)


# class AuthPermission(models.Model):
#     name = models.CharField(max_length=255)
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
#     codename = models.CharField(max_length=100)

#     class Meta:
#         managed = False
#         db_table = 'auth_permission'
#         unique_together = (('content_type', 'codename'),)


# class AuthUser(models.Model):
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.IntegerField()
#     username = models.CharField(unique=True, max_length=150)
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     email = models.CharField(max_length=254)
#     is_staff = models.IntegerField()
#     is_active = models.IntegerField()
#     date_joined = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'auth_user'


# class AuthUserGroups(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'auth_user_groups'
#         unique_together = (('user', 'group'),)


# class AuthUserUserPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'auth_user_user_permissions'
#         unique_together = (('user', 'permission'),)


# class DjangoAdminLog(models.Model):
#     action_time = models.DateTimeField()
#     object_id = models.TextField(blank=True, null=True)
#     object_repr = models.CharField(max_length=200)
#     action_flag = models.PositiveSmallIntegerField()
#     change_message = models.TextField()
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'django_admin_log'


# class DjangoContentType(models.Model):
#     app_label = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)

#     class Meta:
#         managed = False
#         db_table = 'django_content_type'
#         unique_together = (('app_label', 'model'),)


# class DjangoMigrations(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'django_migrations'


# class DjangoSession(models.Model):
#     session_key = models.CharField(primary_key=True, max_length=40)
#     session_data = models.TextField()
#     expire_date = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'django_session'
