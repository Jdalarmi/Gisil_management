from django.contrib import admin
from .models import LiquidValue, GroosValue, GisilValues, DefinitionsValues

admin.site.register(LiquidValue)
admin.site.register(GroosValue)
admin.site.register(GisilValues)
admin.site.register(DefinitionsValues)