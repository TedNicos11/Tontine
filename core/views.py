from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.views.generic import TemplateView, View
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.html import format_html
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.contrib import messages
from .models import *
from .forms import *

# Create your views here

class WelcomeView(TemplateView):
    template_name = 'welcome.html'

class HomeView(LoginRequiredMixin, View):
    template_name = 'index.html'
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        pk = get_object_or_404(User, id=self.kwargs["pk"])
        user = get_object_or_404(User, username=self.kwargs["user"])

        context = {
            'nbar': 'home',
            'pk': pk,
            'user': user,
        }
        return render(request, self.template_name, context)
    

class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'register.html'
    success_url = reverse_lazy('core:login')
    form_class = UserRegisterForm
    success_message = "Your account was created successfully"

class LoginView(View):
    template_name = 'login.html'
    initial = {'key': 'value'}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('core:home', kwargs={'pk': request.user.id, 'user': request.user.username}))
        else:
            if request.method == 'POST':
                username = request.POST.get('username')
                password = request.POST.get('password')

                auth_user = authenticate(
                    request, username=username, password=password)

                if auth_user is not None and auth_user.is_active:
                    login(request, auth_user)
                    message_out_success = format_html(
                        f'You are successfully logged in as <strong>{username}</strong>!'
                    )
                    messages.success(
                        request,
                        message_out_success
                    )
                    try:
                        if request.GET['next']:
                            return redirect(request.GET['next'])
                    except Exception as e:
                        return redirect(reverse('core:home', kwargs={'pk': request.user.id, 'user': request.user.username}))
                else:
                    messages.error(
                        request,
                        f'Login failed! Incorrect username or password.'
                    )
                    return redirect('core:login')

            return render(request, self.template_name)


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(
            request,
            f'You are now logged out.'
        )
        return redirect('core:login')

# App Views
class AppView(LoginRequiredMixin, TemplateView):
    template_name = 'app.html'
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        pk = get_object_or_404(User, id=self.kwargs["pk"])
        user = get_object_or_404(User, username=self.kwargs["user"])

        context = {
            'nbar': 'home',
            'pk': pk,
            'user': user,
        }
        return render(request, self.template_name, context)

# Custom 404 page
class page_not_found_view(TemplateView):
    template_name = '404.html'