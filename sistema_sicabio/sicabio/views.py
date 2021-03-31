import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from django.template.loader import render_to_string
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView

from sicabio.form import PacienteForm, ImpressaoForm, UsuarioForm
from sicabio.models import Paciente, Impressao



@login_required(login_url='/login/')
def list_all_pacientes(request):
    paciente = Paciente.objects.filter(user=request.user)

    busca = request.GET.get('buscar')

    if busca:
        paciente = Paciente.objects.filter(nome_paciente__icontains=busca)
    else:
        paciente_list = Paciente.objects.filter(user=request.user)
        paginator = Paginator(paciente_list, 10)
        page = request.GET.get('page', )
        paciente = paginator.get_page(page)

    return render(request, 'listagem_pacientes.html', {'paciente': paciente})

@login_required(login_url='/login/')
def delete_paciente(request, id):
    paciente = Paciente.objects.get(id=id)
    paciente.delete()
    messages.success(request, "Paciente excluído com sucesso.")
    return redirect('../../../pacientes/')



def do_login(request):
    return render(request, 'login.html')


@csrf_protect
def submit_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Usuário e senha inválidos. Por favor, tente novamente.')
    return redirect('/login/')


@login_required(login_url='/login/')
def logout_user(request):
    logout(request)
    return redirect('/login')

#
# class ViewImpressao(TemplateView):
#     template_name = 'add_digital.html'
#
#     def get_context_data(self, **kwargs):
#         paciente = Paciente.objects.all()
#         context = super().get_context_data(**kwargs)
#         context= {'form':ImpressaoForm(self.request.POST),'paciente':paciente}
#         print('Testando',context)
#
#         return context
#
#
#
#
# @csrf_protect
# def save_impressao_form(request, form, template_name):
#
#     data = dict()
#     if request.method == 'POST':
#
#         if form.is_valid():
#
#             pacient = form.cleaned_data.get('paciente')
#             print('FORMPACIENTE',pacient)
#             form_im = ImpressaoForm( data=request.POST, files=request.FILES,instance=pacient)
#
#
#             data['form_is_valid'] = True
#
#
#         else:
#             data['form_is_valid'] = False
#             form = ImpressaoForm(request.POST)
#             print('invalid form')
#
#             print('Erro:', form.errors)
#
#
#
#
#     context = {'form': form}
#     data['html_form'] = render_to_string(template_name, context, request=request)
#     return JsonResponse(data)
#
# def impressao_create(request):
#     if request.method == 'POST':
#         form = ImpressaoForm(request.POST)
#     else:
#         form = ImpressaoForm(request.POST)
#         print(form.errors)
#
#     return save_impressao_form(request, form, 'add_digital.html')
@login_required(login_url='/login/')
@csrf_protect
def post(request,id):
    paciente_id = request.POST.get('id_paciente')
    paciente = Paciente.objects.get(pk=id)
    data = dict()

    if request.method == "POST":

        form = ImpressaoForm(data=request.POST, files=request.FILES)
        if form.is_valid():

            file = form.save(commit=False)
            file.paciente = paciente

            file.save()
            data['form_is_valid'] = True
            data['html_file_list'] = render_to_string('includes/partial_impressao_list.html')
            return JsonResponse(data)

        else:
            data['form_is_valid'] = False
            form = ImpressaoForm(request.POST)

            print('invalid form')
            print(form.errors)
            return JsonResponse(data)

    form = ImpressaoForm(request.POST)
    return render(request,'listar_impressoes.html',{'form':form})


@login_required(login_url='/login/')
@csrf_protect
def save_paciente_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if request.user.is_authenticated:

            if form.is_valid():
                form_m = PacienteForm(request.POST, request.user)

                u = form_m.save(commit=False)
                u.user = request.user

                u.save()
                data['form_is_valid'] = True
                print(form.errors)

                paciente = Paciente.objects.filter(user=request.user)
                data['html_paciente_list'] = render_to_string('includes/partial_paciente_list.html', {
                    'paciente': paciente
                })




            else:
                data['form_is_valid'] = False
                print('invalid form')

                print(form.errors)
    print(form.errors)

    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required(login_url='/login/')
def paciente_create(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
    else:
        form = PacienteForm()
    return save_paciente_form(request, form, 'includes/partial_paciente_create.html')

@login_required(login_url='/login/')
def paciente_update(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
    else:
        form = PacienteForm(instance=paciente)

    return save_paciente_form(request, form, 'includes/partial_paciente_update.html')

@login_required(login_url='/login/')
def listarImpressoes(request, id):
    paciente = Paciente.objects.get(id=id)
    impressao = Impressao.objects.filter(paciente=paciente)

    return render(request, 'listar_impressoes.html', {'paciente': paciente, 'impressao': impressao})


@login_required(login_url='/login/')
def delete_impressao(request,id,id_impressao):
    impressao = Impressao.objects.get(id=id_impressao)
    impressao.delete()
    return redirect('../../../digitais/',{'impressao':impressao})


@login_required(login_url='/login/')
def logout_user(request):
    logout(request)
    return redirect('/login')

@csrf_protect
def cadastro(request):
    form = UsuarioForm(request.POST or None)
    context = {'form': form}
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Cadastro realizado com sucesso!")
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
            print(form.errors)

            return redirect('/cadastro/')
    return render(request, "base_cadastro.html", context)


def do_login(request):
    return render(request, "login.html")


@csrf_protect
def submit_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)

        if usuario is not None:
            login(request, usuario)

            return redirect('../pacientes/')
        else:
            messages.error(request, 'Usuário e senha inválidos. Por favor, tente novamente.')
    return redirect('/login/')


def home(request):
    return redirect('/login/')
