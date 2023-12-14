from django.contrib import admin
from .models import LiquidValue, GroosValue, GisilValues

admin.site.register(LiquidValue)
admin.site.register(GroosValue)
admin.site.register(GisilValues)