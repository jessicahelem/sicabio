from django import forms

from sicabio.models import Paciente, Impressao
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.forms import ModelForm


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'
        labels = {'dt_nascimento':'Data de Nascimento','cpf_paciente':'CPF','nome_paciente':'Nome Completo'}


        widgets = {

            'cpf_paciente': forms.TextInput(attrs={'data-mask': "000.000.000-00"}),
            'dt_nascimento':forms.DateInput(attrs={'data-mask':'00/00/0000'})

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nome_paciente', css_class='form-group col-md mb-0'),


            ),

            Row(
                Column('cpf_paciente', css_class='form-group col-md-6 mb-0'),
                Column('dt_nascimento', css_class='form-group col-md-6 mb-0'),

            ),


            #  'check_me_out',
            # Submit('submit', 'Sign in')
        )

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf_paciente']
        if Paciente.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError('CPF JÁ EXISTE!')
        return cpf


class ImpressaoForm(forms.ModelForm):
    class Meta:
        model = Impressao
        fields = ('img',)

