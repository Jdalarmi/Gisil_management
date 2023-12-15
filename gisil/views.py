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

            valor_lucro_total = liquid_value_total

            request.session['valor_reserva'] += nf_exist
            request.session['valor_imposto'] += value_nf
            request.session['valor_boleto'] += kilate_value + outher_cust
            request.session['valor_investimento'] += nf_not_exist
            request.session['valor_investimento'] += nf_not_exist
            if 'valor_lucro_liquido' in request.session:
                request.session['valor_lucro_liquido'] += valor_lucro_total
            else:
                request.session['valor_lucro_liquido'] = valor_lucro_total


            print(request.session['valor_reserva'])
            print(request.session['valor_imposto'])
            print(request.session['valor_boleto'])
            print(request.session['valor_investimento'])
            print(request.session['valor_lucro_liquido'])

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

            valor_lucro_total = liquid_value_total

            request.session['valor_reserva'] += nf_exist
            request.session['valor_imposto'] = 0
            request.session['valor_boleto'] += kilate_value + outher_cust
            request.session['valor_investimento'] += nf_not_exist
            if 'valor_lucro_liquido' in request.session:
                request.session['valor_lucro_liquido'] += valor_lucro_total
            else:
                request.session['valor_lucro_liquido'] = valor_lucro_total


            gisil_values_instance.emergency += nf_exist
            gisil_values_instance.imposto += 0
            gisil_values_instance.boleto += kilate_value + outher_cust  
            gisil_values_instance.invest += nf_not_exist
            gisil_values_instance.lucro += liquid_value_total

            gisil_values_instance.save()


            messages.success(request, 'Pedido Recebido com SUCESSO!!')
            return redirect('gisil-values')
    totals = {
        'valor_reserva':request.session['valor_reserva'],
        'valor_imposto':request.session['valor_imposto'],
        'valor_boleto':request.session['valor_boleto'],
        'valor_investimento':request.session['valor_investimento'],
        'valor_lucro_liquido':request.session['valor_lucro_liquido']
    }  

    values_gisil = GisilValues.objects.all
    context = {
        "values_gisil":values_gisil,
        "totals":totals
    }

    
    return render(request, 'gisil/gisil_values.html', context)

def customer(request):
    return render(request, 'gisil/customer.html')

#função tempoaria
def reset_all_zero(request):
    request.session['valor_reserva'] = 0
    request.session['valor_reserva'] = 0
    request.session['valor_imposto'] = 0 
    request.session['valor_boleto'] = 0
    request.session['valor_investimento'] = 0
    request.session['valor_lucro_liquido'] = 0
    return redirect('gisil-values')