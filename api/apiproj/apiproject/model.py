from django.db import models


class CvdModel(models.Model):
    age = models.IntegerField()
    body_max_index = models.DecimalField(decimal_places=2,max_digits=6)
    blood_pressure = models.DecimalField(decimal_places=2,max_digits=6)
    gender = models.CharField(max_length=10)
    cholesterol = models.CharField(max_length=4)
    glucose = models.CharField(max_length=10)
    physical_activity = models.CharField(max_length=10)
    smoking = models.CharField(max_length=10)
    alcohol= models.CharField(max_length=10)