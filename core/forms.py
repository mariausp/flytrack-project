# core/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re

class ContactForm(forms.Form):
    nome = forms.CharField(label="Nome", max_length=80)
    email = forms.EmailField(label="Seu e-mail")
    assunto = forms.CharField(label="Assunto", max_length=120)
    mensagem = forms.CharField(label="Mensagem", widget=forms.Textarea, max_length=4000)
    concordo = forms.BooleanField(label="Autorizo o contato por e-mail", required=True)


def validar_cpf(cpf: str) -> bool:
    cpf = re.sub(r'\D', '', cpf or '')
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    def dv(cpf_parcial):
        soma = sum(int(d) * w for d, w in zip(cpf_parcial, range(len(cpf_parcial)+1, 1, -1)))
        resto = (soma * 10) % 11
        return 0 if resto == 10 else resto
    return dv(cpf[:9]) == int(cpf[9]) and dv(cpf[:10]) == int(cpf[10])

class SignupForm(UserCreationForm):
    email = forms.EmailField(label='E-mail', required=True,
                             widget=forms.EmailInput(attrs={'placeholder': 'voce@email.com'}))
    birth_date = forms.DateField(label='Data de nascimento',
                                 widget=forms.DateInput(attrs={'type': 'date'}))
    cpf = forms.CharField(label='CPF', max_length=14,
                          widget=forms.TextInput(attrs={'inputmode': 'numeric', 'placeholder': 'Somente números'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'birth_date', 'cpf', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Seu usuário'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Crie uma senha'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirme a senha'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Zera help_texts verbosos do Django
        for f in ['username', 'password1', 'password2']:
            if f in self.fields:
                self.fields[f].help_text = ''

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Já existe um usuário com este e-mail.')
        return email

    def clean_cpf(self):
        raw = self.cleaned_data['cpf']
        digits = re.sub(r'\D', '', raw or '')
        if not validar_cpf(digits):
            raise forms.ValidationError('CPF inválido.')
        return digits

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email'].strip().lower()
        if commit:
            user.save()
            from .models import Profile
            Profile.objects.update_or_create(
                user=user,
                defaults={
                    'birth_date': self.cleaned_data['birth_date'],
                    'cpf': self.cleaned_data['cpf'],
                }
            )
        return user
class SignupForm(UserCreationForm):
    email = forms.EmailField(label='E-mail', required=True)
    birth_date = forms.DateField(label='Data de nascimento', widget=forms.DateInput(attrs={'type': 'date'}))
    cpf = forms.CharField(label='CPF', max_length=14, help_text='Apenas números', widget=forms.TextInput(attrs={'inputmode': 'numeric'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'birth_date', 'cpf', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Já existe um usuário com este e-mail.')
        return email

    def clean_cpf(self):
        raw = self.cleaned_data['cpf']
        digits = re.sub(r'\D', '', raw or '')
        if not validar_cpf(digits):
            raise forms.ValidationError('CPF inválido.')
        return digits  # guarda só dígitos

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email'].strip().lower()
        if commit:
            user.save()
            # cria/atualiza o Profile
            from .models import Profile
            Profile.objects.update_or_create(
                user=user,
                defaults={
                    'birth_date': self.cleaned_data['birth_date'],
                    'cpf': self.cleaned_data['cpf'],
                }
            )
        return user
