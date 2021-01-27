from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from django.template.loader import render_to_string
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView

from sicabio.form import PacienteForm, ImpressaoForm
from sicabio.models import Paciente, Impressao


def home(request):

    return render(request,'listagem_pacientes.html')


def list_all_pacientes(request):
    paciente = Paciente.objects.filter()

    busca = request.GET.get('buscar')

    if busca:
        paciente = Paciente.objects.filter(nome_paciente__icontains=busca)
    else:
        paciente_list = Paciente.objects.filter()
        paginator = Paginator(paciente_list, 10)
        page = request.GET.get('page', )
        paciente = paginator.get_page(page)

    return render(request, 'listagem_pacientes.html', {'paciente': paciente})

def delete_paciente(request, id):
    paciente = Paciente.objects.get(id=id)
    paciente.delete()
    messages.success(request, "Paciente excluído com sucesso.")
    return redirect('../../../pacientes/')

def form(request,id):
    paciente = Paciente.objects.get(id=id)
    return render(request,'add_digital.html',{'paciente':paciente})




# class ViewMedicamento(TemplateView):
#     template_name = 'base_consulta.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['medicamento'] = Medicamento.objects.all()
#         return context

class BasicUploadView(View):
    data = dict()
    def get(self, request,id):
        impressao = Impressao.objects.filter(paciente=id)
        paciente = Paciente.objects.get(pk=id)
        return render(self.request, 'add_digital.html', {'impressao': impressao,'paciente':paciente})

    def post(self, request,id):
        data = dict()
        paciente_id = request.POST.get('paciente-id')
        paciente = Paciente.objects.get(id=paciente_id)
        form = ImpressaoForm(self.request.POST, self.request.FILES)


        if form.is_valid():
            impressao = form.save(commit=False)
            impressao.paciente = paciente
            impressao.save()

            data['form_is_valid'] = True
            arquivo = Impressao.objects.filter(paciente=paciente)
            data['html_file_list'] = render_to_string('includes/partial_impressao_list.html', {'arquivo': arquivo})
        else:
            data = {'is_valid': False}
            print(form.errors)

        print(form.errors)
        return JsonResponse(data)


@csrf_protect
def save_paciente_form(request, form, template_name):


    data = dict()
    if request.method == 'POST':


        if form.is_valid():

            form.save()
            data['form_is_valid'] = True
            print(form.errors)


            paciente = Paciente.objects.filter()
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


def paciente_create(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
    else:
        form = PacienteForm()
    return save_paciente_form(request, form, 'includes/partial_paciente_create.html')


def paciente_update(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
    else:
        form = PacienteForm(instance=paciente)

    return save_paciente_form(request, form, 'includes/partial_paciente_update.html')

def listarImpressoes(request,id):
    paciente = Paciente.objects.get(id=id)
    impressao = Impressao.objects.filter(paciente=paciente)

    return render(request,'listar_impressoes.html',{'paciente':paciente,'impressao':impressao})
