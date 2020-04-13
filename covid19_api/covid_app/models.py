from django.db import models

class Data(models.Model):
    region_name = models.CharField(max_length=100)
    average_age = models.CharField(max_length=100)
    average_daily_income = models.CharField(max_length=100)
    average_daily_income_population = models.CharField(max_length=100) 
    period_type = models.CharField(max_length=10)
    time_to_elapse = models.IntegerField()
    reported_cases = models.IntegerField()
    population = models.IntegerField()
    total_hospital_beds = models.IntegerField()



    def __str__(self):
        return str(self.region_name)


