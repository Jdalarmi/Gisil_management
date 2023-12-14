from django.shortcuts import render, redirect
from .models import GroosValue, LiquidValue, GisilValues
from datetime import datetime
from django.contrib import messages
def index(request):
    values = LiquidValue.objects.all()
    context = {
        "values":values,
    }
    return render(request, 'gisil/index.html', context)

def entry_value(request):

    if request.method == 'POST':
        value = float(request.POST.get('value').replace(",", "."))
        date = request.POST.get('date').replace(",", ".")
        quantity = float(request.POST.get('quantity'))
        kilate = float(request.POST.get('kilate').replace(",", "."))
        frete = float(request.POST.get('frete').replace(",", "."))
        box = float(request.POST.get('box').replace(",", "."))
        nf = request.POST.get('nf')

        nf_exist = value * (5 / 100)

        nf_not_exist = value * (2 / 100)

        data_obj = datetime.strptime(date, '%Y-%m-%d')
        month_name = data_obj.strftime('%B')

        kilate_value = quantity * kilate * 0.2 * 5
        outher_cust = box + frete + (quantity * 1.90)
        
        if nf == '1':
            value_nf = value * (4.5 / 100)
            liquid_value_total = value - kilate_value - outher_cust - value_nf - nf_exist - nf_exist
            dados_mensais, created = LiquidValue.objects.get_or_create(
                month = month_name,
                defaults={'liquid_value':liquid_value_total}
            )
            if not created:
                dados_mensais.liquid_value += liquid_value_total
                dados_mensais.save()
            
            gisil_values_instance, created = GisilValues.objects.get_or_create(
            id=1,
            defaults={'emergency': 0, 'imposto': 0, 'boleto': 0, 'invest': 0, 'lucro': 0}
            )

            gisil_values_instance.emergency += nf_exist
            gisil_values_instance.imposto += value_nf
            gisil_values_instance.boleto += kilate_value + outher_cust  
            gisil_values_instance.invest += nf_not_exist
            gisil_values_instance.lucro += liquid_value_total

            gisil_values_instance.save()

            dados_mensais.save()
            messages.success(request, 'Pedido Recebido com SUCESSO!!')
            return redirect('gisil-values')
        
        if nf == '2':
            liquid_value_total = value - kilate_value - outher_cust -nf_exist - nf_exist
            dados_mensais, created = LiquidValue.objects.get_or_create(
                month = month_name,
                defaults={'liquid_value':liquid_value_total}
            )
            if not created:
                dados_mensais.liquid_value += liquid_value_total
                dados_mensais.save()

            gisil_values_instance, created = GisilValues.objects.get_or_create(
                id=1,
                defaults={'emergency': 0, 'imposto': 0, 'boleto': 0, 'invest': 0, 'lucro': 0}
            )

            gisil_values_instance.emergency += nf_exist
            gisil_values_instance.imposto += 0
            gisil_values_instance.boleto += kilate_value + outher_cust  
            gisil_values_instance.invest += nf_not_exist
            gisil_values_instance.lucro += liquid_value_total

            gisil_values_instance.save()


            messages.success(request, 'Pedido Recebido com SUCESSO!!')
            return redirect('gisil-values')
        
    values_gisil = GisilValues.objects.all
    context = {
        "values_gisil":values_gisil
    }

    
    return render(request, 'gisil/gisil_values.html', context)

def customer(request):
    return render(request, 'gisil/customer.html')