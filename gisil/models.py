from django.db import models

class GroosValue(models.Model):
    value_groos = models.FloatField()
    date = models.DateField()
    quantity = models.FloatField()
    frete = models.FloatField()
    box_value = models.FloatField()

class LiquidValue(models.Model):
    liquid_value = models.FloatField()
    month = models.CharField(max_length=20)