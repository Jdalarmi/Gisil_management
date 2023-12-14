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

class GisilValues(models.Model):
    emergency = models.FloatField()
    imposto = models.FloatField(null=True, blank=True)
    boleto = models.FloatField()
    invest = models.FloatField()
    lucro = models.FloatField()