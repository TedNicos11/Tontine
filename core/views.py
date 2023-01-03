import datetime
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.views.generic import TemplateView, ListView, View
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.html import format_html
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.contrib import messages
from django.core.paginator import Paginator
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


class AppView(LoginRequiredMixin, View):
    template_name = 'app.html'
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        pk = get_object_or_404(User, id=self.kwargs["pk"])
        user = get_object_or_404(User, username=self.kwargs["user"])
        owner = self.request.user

        # Get the current time
        now = datetime.datetime.now()
        
         # Query user's tontines
        owner = self.request.user
        query = Tontine.objects.filter(owner_id=owner.id)

        # Determine whether it is morning or evening
        if now.hour < 12:
            greeting = "Bonjour"
        else:
            greeting = "Bonsoir"

        # Paginator
        paginator = Paginator(query, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'pk': pk,
            'user': user,
            'query': query,
            'greeting': greeting,
            'page_obj': page_obj
        }
        return render(request, self.template_name, context)


class CreateTontine(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Tontine
    # fields = ['name', 'number_of_members', 'slogan', 'rules']
    template_name = 'tontine/tontine_form.html'
    form_class = CreateTontineForm
    success_message = "Tontine crée avec succes"
    initial = {'key': 'value'}

    def get(self, request, *args, **kwargs):
        pk = get_object_or_404(User, id=self.kwargs["pk"])
        user = get_object_or_404(User, username=self.kwargs["user"])
        form = self.form_class(initial=self.initial)

        context = {
            'pk': pk,
            'user': user,
            'form': form
        }
        return render(request, self.template_name, context)
    
    def form_valid(self, form):
        # Get the current user
        owner = self.request.user

        # Set the default value of the user field to the current user
        form.instance.owner = owner

        return super().form_valid(form)

    def get_success_url(self):
        # Get the object that was created
        user = self.request.user

        # Use the reverse_lazy() function to reverse a URL pattern and return the URL as a string
        success_url = reverse_lazy(
            'core:app', kwargs={'pk': user.id, 'user': user.username})

        return success_url

class ListTontine(LoginRequiredMixin, View):
    template_name = 'tontine/tontine_all.html'
    context_object_name = 'tontines'
    
    def get(self, request, *args, **kwargs):
        pk = get_object_or_404(User, id=self.kwargs["pk"])
        user = get_object_or_404(User, username=self.kwargs["user"])
        
        # Query user's tontines
        owner = self.request.user
        query = Tontine.objects.filter(owner_id=owner.id)

        context = {
            'pk': pk,
            'user': user,
            'query': query,
        }
        return render(request, self.template_name, context)
    
    def get_queryset(self):
        return Tontine.objects.filter(owner_id=self.request.user.id)
    
class DetailTontine(LoginRequiredMixin, View):
    template_name = 'tontine/tontine_details.html'
    
    def get(self, request, *args, **kwargs):
        pk = get_object_or_404(User, id=self.kwargs["pk"])
        user = get_object_or_404(User, username=self.kwargs["user"])
        tont_id = get_object_or_404(Tontine, id=self.kwargs["tont_id"])
        tontine = get_object_or_404(Tontine, name=self.kwargs["tontine"])
        print(tontine)
        
        # Query user's tontines
        owner = self.request.user
        # query = Tontine.objects.filter(owner_id=owner.id, id=tont_id)
        query = Tontine.objects.get(owner_id=owner.id, id=tont_id.id)

        context = {
            'pk': pk,
            'user': user,
            'tont_id': tont_id,
            'tontine': tontine,
            'query': query,
        }
        return render(request, self.template_name, context)


class CreateTontine(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Tontine
    # fields = ['name', 'number_of_members', 'slogan', 'rules']
    template_name = 'tontine_form.html'
    form_class = CreateTontineForm
    success_message = "Tontine crée avec succes"
    initial = {'key': 'value'}

    def get(self, request, *args, **kwargs):
        pk = get_object_or_404(User, id=self.kwargs["pk"])
        user = get_object_or_404(User, username=self.kwargs["user"])
        form = self.form_class(initial=self.initial)

        context = {
            'pk': pk,
            'user': user,
            'form': form
        }
        return render(request, self.template_name, context)

    def get_success_url(self):
        # Get the object that was created
        user = self.request.user

        # Use the reverse_lazy() function to reverse a URL pattern and return the URL as a string
        success_url = reverse_lazy(
            'core:app', kwargs={'pk': user.id, 'user': user.username})

        return success_url


# Custom 404 page


class page_not_found_view(TemplateView):
    template_name = '404.html'
