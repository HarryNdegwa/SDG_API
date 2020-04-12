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


class Main(models.Model):
    data = models.OneToOneField(Data,on_delete = models.CASCADE,null=True)
    currently_infected = models.IntegerField(default=0)
    infections_by_requested_time = models.IntegerField(default=0)
    severe_cases_by_requested_time = models.IntegerField(default=0)
    hospital_beds_by_requested_time = models.IntegerField(default=0)
    cases_for_icu_by_requested_time = models.IntegerField(default=0)
    cases_for_ventilators_by_requested_time = models.IntegerField(default=0)
    dollars_in_flight = models.DecimalField(max_digits=100,decimal_places=2,null=True)


    class Meta:
        abstract = True


class Impact(Main):
    def __str__(self):
        return f"{self.data} impact"


class SevereImpact(Main):
    def __str__(self):
        return f"{self.data} severe impact"
