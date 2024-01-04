from django.shortcuts import get_object_or_404, render, redirect
from .models import LiquidValue, GisilValues, DefinitionsValues
from datetime import datetime
from django.contrib import messages
from .forms import GisilForm
from utils.grafic_bar import generate_bar
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required

@login_required(login_url='user-login')
def index(request):
    definition_values = DefinitionsValues.objects.all()
    categories = ['caixa', 'frete']
    for obj in definition_values:
        box_value = obj.box
        cust_value = obj.frete_cust

    values = [box_value, cust_value]
    chart_data = generate_bar(categories, values)
    values = LiquidValue.objects.all()
    context = {
        "values":values,
        "chart_data":chart_data,
    }
    return render(request, 'gisil/index.html', context)


@login_required(login_url='user-login')
def entry_value(request):
    if request.method == 'POST':
        value = float(request.POST.get('value').replace(",", "."))
        date = request.POST.get('date').replace(",", ".")
        quantity = float(request.POST.get('quantity'))
        kilate = float(request.POST.get('kilate').replace(",", "."))
        frete = float(request.POST.get('frete').replace(",", "."))
        box = float(request.POST.get('box').replace(",", "."))
        nf = request.POST.get('nf')

        data_definitions = DefinitionsValues.objects.filter(box=box, frete_cust=frete).first()
        if data_definitions is None:
            data_definitions = DefinitionsValues.objects.create(box=box, frete_cust=frete)
        else:
            data_definitions.box += box
            data_definitions.frete_cust += frete
            data_definitions.save()

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
            if 'valor_lucro_liquido' in request.session:
                request.session['valor_lucro_liquido'] += valor_lucro_total
            else:
                request.session['valor_lucro_liquido'] = valor_lucro_total

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
            request.session['valor_investimento'] += nf_exist
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
    # totals = {
    #     'valor_reserva':request.session['valor_reserva'],
    #     'valor_imposto':request.session['valor_imposto'],
    #     'valor_boleto':request.session['valor_boleto'],
    #     'valor_investimento':request.session['valor_investimento'],
    #     'valor_lucro_liquido':request.session['valor_lucro_liquido']
    # }  
    totals = {
        'valor_reserva': request.session.get('valor_reserva', 0),
        'valor_imposto': request.session.get('valor_imposto', 0),
        'valor_boleto': request.session.get('valor_boleto', 0),
        'valor_investimento': request.session.get('valor_investimento', 0),
        'valor_lucro_liquido': request.session.get('valor_lucro_liquido', 0),
    }

    values_gisil = GisilValues.objects.all
    context = {
        "values_gisil":values_gisil,
        "totals":totals
    }

    
    return render(request, 'gisil/gisil_values.html', context)


@login_required(login_url='user-login')
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

@login_required(login_url='user-login')
def edit_values(request):
    instancia  = get_object_or_404(GisilValues)

    if request.method == "POST":
        form = GisilForm(request.POST, instance = instancia)
        if form.is_valid():
            form.save()
            return redirect('gisil-values')
    else:
        form = GisilForm(instance=instancia)

    return render(request, 'gisil/edit_values.html', {"form":form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Usuario não existe! Favor registre seu usuario.')
            return redirect('user-login')
    return render(request, 'gisil/user_login.html')

def logout_user(request):
    auth.logout(request)

    return redirect('user-login')