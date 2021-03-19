from django import forms

from sicabio.models import Paciente, Impressao, User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column


class PacienteForm(forms.ModelForm):

    Paciente._meta.get_field('cpf_paciente').blank = True
    Paciente._meta.get_field('dt_nascimento').blank = False
    Paciente._meta.get_field('nome_paciente').blank = False


    class Meta:
        model = Paciente
        fields = '__all__'
        labels = {'dt_nascimento': 'Data de Nascimento', 'cpf_paciente': 'CPF', 'nome_paciente': 'Nome Completo'}
        exclude = ('user',)

        widgets = {

            'cpf_paciente': forms.TextInput(attrs={'data-mask': "000.000.000-00"}),
            'dt_nascimento': forms.DateInput(attrs={'data-mask': '00/00/0000'})

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
        fields = ('img', 'dedos', 'mao', 'paciente',)


class UsuarioForm(forms.ModelForm):
    User._meta.get_field('password').blank = False
    User._meta.get_field('CPF').blank = False
    User._meta.get_field('email').blank = False
    User._meta.get_field('username').blank = False

    class Meta:
        model = User
        fields = ("username", "first_name", "CPF", "email", "password")
        labels = {'first_name': 'Nome Completo', 'CPF': 'CPF', 'email': 'Email', 'username': 'Usuário',
                  'password': 'Senha'}
        exclude = ('date_joined',)
        nome = forms.CharField()

        widgets = {
            "username": forms.TextInput(attrs={'class': 'form-control', 'maxlength': 255, }),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 255, }),
            'CPF': forms.TextInput(
                attrs={'class': 'form-control', 'maxlength': 14, }),

            'email': forms.EmailInput(attrs={'class': 'form-control', 'maxlength': 255, }),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'maxlength': 8, }),

        }

    def save(self, commit=True):
        user = super(UsuarioForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email JÁ EXISTE!')

        return email

    def clean_cpf(self):
        cpf = self.cleaned_data['CPF']
        if User.objects.filter(CPF=cpf).exists():
            raise forms.ValidationError('CPF JÁ EXISTE!')
        return cpf

    def clean_user(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('USUÁRIO JÁ EXISTE!')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise forms.ValidationError('A SENHA DEVE TER 8 OU MAIS CARACTERES!')
        return password
