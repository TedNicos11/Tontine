from django import forms
from django.forms.widgets import TextInput, NumberInput, EmailInput, Textarea, PasswordInput, FileInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Tontine

# Create your form here.


class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(max_length=50, label="Mot de passe", widget=PasswordInput(
        attrs={'placeholder': 'Mot de passe', }))
    password2 = forms.CharField(max_length=50, label="Confirmation de mot de passe", widget=PasswordInput(
        attrs={'placeholder': 'Confirmation', }))
    # Meta class

    class Meta:
        model = User

        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2'
        ]

        labels = {
            'first_name': 'Nom',
            'last_name': 'Prénom',
            'username': 'Nom d\'utilisateur',
            'email': 'Adresse email',
            'password1': 'Mot de passe',
            'password2': 'Confirmation de mot de passe',
        }

        widgets = {
            'first_name': TextInput(
                attrs={
                    'placeholder': 'First Name (optional)',
                }
            ),

            'last_name': TextInput(
                attrs={
                    'placeholder': 'Last Name (optional)',
                }
            ),

            'username': TextInput(
                attrs={
                    'placeholder': 'Username',
                }
            ),

            'email': EmailInput(
                attrs={
                    'placeholder': 'Email',
                }
            ),
            # 'password1': PasswordInput(
            #     attrs={
            #         'placeholder': 'Password',
            #     }
            # ),

            # 'password2': PasswordInput(
            #     attrs={
            #         'placeholder': 'Confirm Password',
            #     }
            # ),
        }

        # def __init__(self, *args, **kwargs):
        #     super(UserRegisterForm, self).__init__(*args, **kwargs)
        #     self.fields['password1'].widget = PasswordInput(attrs={'placeholder': 'Password'})
        #     self.fields['password2'].widget = PasswordInput(attrs={'placeholder': 'Confirm Password'})


class CreateTontineForm(forms.ModelForm):
    # Meta class
    class Meta:

        model = Tontine

        fields = ['name', 'number_of_members', 'slogan', 'rules']

        widgets = {
            'name': TextInput(
                attrs={
                    'name': 'name',
                    'class': 'form-control rounded',
                    'id': 'name',
                    'placeholder': 'Nom de la tontine',
                }
            ),

            'number_of_members': NumberInput(
                attrs={
                    'name': 'number_of_members',
                    'class': 'form-control rounded',
                    'id': 'numbers',
                    'placeholder': 'Nombre de membres',
                    'style': 'height: 47.5px'
                }
            ),

            'slogan': TextInput(
                attrs={
                    'name': 'slogan',
                    'class': 'form-control',
                    'id': 'slogan',
                    'placeholder': 'Slogan',
                }
            ),

            'rules': Textarea(
                attrs={
                    'name': 'rules',
                    'class': 'form-control',
                    'id': 'rules',
                    'placeholder': 'Reglement interieure',
                }
            ),
        }
