from django.db import models

# Create your models here.


class district_info(models.Model):
    name = models.CharField(max_length=40, primary_key = True)
    city = models.CharField(max_length=20)
    district = models.CharField(max_length = 20)
    
class school_info(models.Model):
    id = models.CharField(max_length=15, primary_key = True)
    name = models.CharField(max_length=40)
    type = models.CharField(max_length=20)
    public = models.CharField(max_length=10)
    branch = models.CharField(max_length=10)
    state = models.CharField(max_length=10)
    addr = models.CharField(max_length=100)
    load_addr = models.CharField(max_length=100)
    office_code = models.IntegerField()
    office_name = models.CharField(max_length=40)
    support_code = models.IntegerField()
    support_name = models.CharField(max_length=40)
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)
    
class school_detail_info(models.Model):
    name = models.CharField(max_length = 40)
    load_addr = models.CharField(max_length=100, primary_key = True)
    homepage = models.CharField(max_length = 100)
    tel = models.CharField(max_length = 20)
    gender = models.CharField(max_length = 20)
    highschool_type = models.CharField(max_length = 20)
    establishment = models.CharField(max_length = 20)
    