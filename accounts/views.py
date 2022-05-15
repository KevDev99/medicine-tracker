from tkinter.tix import Form
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from medication.models import Medication
from django.http import HttpResponse


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, label='Firstname',
                                 help_text='', widget=forms.TextInput(attrs={'class': "form-control"}))
    last_name = forms.CharField(max_length=30, required=False, label='Lastname',
                                help_text='', widget=forms.TextInput(attrs={'class': "form-control"}))
    email = forms.EmailField(max_length=50, required=True, label='Email',
                             help_text='Required.', widget=forms.TextInput(attrs={'class': "form-control"}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2', )


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'username or email',
                'class': 'form-control'
            }
        )
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'password',
                'class': 'form-control'
            }
        )
    )


class AddMedicineForm(ModelForm):
    class Meta:
        model = Medication
        fields = ['name', 'dosage', 'dosage_unit', 'day', 'time']


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class LoginView(LoginView):
    form_class = LoginForm
    success_url = reverse_lazy("/")
    template_name = "registration/login.html"


# Create your views here.

def register(request):
    if(request.method == 'GET'):
        return render(request, 'registration/signup.html', context={"register_form": SignUpForm})
    elif request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("account")
        else:
            messages.error(
                request, "Unsuccessful registration. Invalid information.")
    else:
        return render(request, 'registration/signup.html', context={"register_form": SignUpForm})


def index(request):

    if(request.method == 'POST'):
        form = AddMedicineForm(request.POST)
        if form.is_valid():
            medicine = form.save(commit=False)
            medicine.user = request.user
            medicine.save()
            return redirect("account")
        else:
            messages.error(
                request, "Wrong form input")
    else:
        user_medicine = Medication.objects.filter(user=request.user)

        return render(request, 'account/index.html', {
            'add_medicine_form': AddMedicineForm,
            'medications': user_medicine
        })
