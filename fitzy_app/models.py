from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age=models.PositiveIntegerField()
    gender=models.CharField(max_length=6)
    weight=models.FloatField(help_text="weight in kg")
    activity_level=models.CharField(max_length=50)
    goal=models.CharField(max_length=50,default="")
    h1=models.FloatField(help_text="height in meter for bmi")
    h2=models.FloatField(help_text="height in cm for calorie")
    protein_req=models.DecimalField(max_digits=5, decimal_places=1, default=0)
    protein_eaten= models.DecimalField(max_digits=5, decimal_places=1, default=0)
    calorie_req= models.DecimalField(max_digits=5, decimal_places=0, default=0)
    calorie_eaten= models.DecimalField(max_digits=5, decimal_places=1, default=0)
    bmi_req=models.DecimalField(max_digits=3,decimal_places=1,default=0)
    nutrition=models.JSONField(default=dict)
    date_update=models.DateField(default=timezone.now)

    def __str__(self):
        return self.user.first_name
    
class NutritionalData(models.Model):
    food_name=models.CharField(max_length=30,primary_key=True)
    calorie=models.FloatField()
    protein=models.FloatField()
    serving_size=models.CharField(max_length=50, default="1")
    

    def __str__(self):
        return self.food_name