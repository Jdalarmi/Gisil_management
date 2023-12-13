from django.shortcuts import render, redirect
from .models import GroosValue, LiquidValue
from datetime import datetime
from django.contrib import messages
def index(request):
    values = LiquidValue.objects.all()
    context = {
        "values":values
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

        data, created = GroosValue.objects.get_or_create(
            value_groos = value,
            date = date,
            quantity = quantity,
            frete = frete,
            box_value = box,
        )
        if not created:
            data.value_groos += value
            data.quantity += quantity
            data.frete += frete
            data.box_value += box

        data_obj = datetime.strptime(date, '%Y-%m-%d')
        month_name = data_obj.strftime('%B')

        kilate_value = quantity * kilate * 0.2 * 5
        outher_cust = box + frete
        if nf == '1':
            value_nf = value * (4.5 / 100)
            liquid_value_total = value - (kilate_value - outher_cust - value_nf)
            dados_mensais, created = LiquidValue.objects.get_or_create(
                month = month_name,
                defaults={'liquid_value':liquid_value_total}
            )
            if not created:
                dados_mensais.liquid_value += liquid_value_total

            dados_mensais.save()
            messages.success(request, 'Pedido cadastrado com SUCESSO!!')
            return redirect('gisil-values')
        elif nf == '2':
            liquid_value_total = value - (kilate_value - outher_cust)
            dados_mensais, created = LiquidValue.objects.get_or_create(
                month = month_name,
                defaults={'liquid_value':liquid_value_total}
            )
            if not created:
                dados_mensais.liquid_value += liquid_value_total
            dados_mensais.save()
            messages.success(request, 'Pedido cadastrado com SUCESSO!!')
            return redirect('gisil-values')
    
    return render(request, 'gisil/gisil_values.html')

def customer(request):
    return render(request, 'gisil/customer.html')