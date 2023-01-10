import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.html import format_html
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.text import slugify
from .models import Tontine
from .forms import UserRegisterForm, CreateTontineForm

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
        query_all = Tontine.objects.all()

        # Determine whether it is morning or evening
        if now.hour < 12:
            greeting = "Bonjour"
        else:
            greeting = "Bonsoir"

        # Paginator
        items_per_page = 6
        paginator = Paginator(query, items_per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'pk': pk,
            'user': user,
            'query': query,
            'greeting': greeting,
            'page_obj': page_obj,
            'items_per_page': items_per_page,
            'query_all': query_all,
        }
        return render(request, self.template_name, context)


class CreateTontine(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Tontine
    template_name = 'tontine/tontine_create_form.html'
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
    
class DetailTontine(LoginRequiredMixin, View):
    template_name = 'tontine/tontine_details.html'
    
    def get(self, request, *args, **kwargs):
        # pk = get_object_or_404(User, id=self.kwargs["pk"])
        # user = get_object_or_404(User, username=self.kwargs["user"])
        tont_id = get_object_or_404(Tontine, id=self.kwargs["tont_id"])
        tontine = get_object_or_404(Tontine, slug=self.kwargs["tontine"])
       
        # Query user's tontines
        owner = self.request.user
        query = Tontine.objects.get(id=tont_id.id)
        
        # Manage joined members by getting current tontine and user

        context = {
            'pk': owner,
            'user': owner,
            'tont_id': tont_id,
            'tontine': tontine,
            'query': query,
        }
        return render(request, self.template_name, context)
    
class UpdateTontine(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Tontine
    template_name = 'tontine/tontine_update_form.html'
    success_message = "Tontine mise à jour avec succes"
    form_class = CreateTontineForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = get_object_or_404(User, id=self.kwargs["pk"])
        context['user'] = get_object_or_404(User, username=self.kwargs["user"])
        context['tont_id'] = get_object_or_404(Tontine, id=self.kwargs["tont_id"])
        context['tontine'] = get_object_or_404(Tontine, slug=self.kwargs["tontine"])
        context['object'] = Tontine.objects.get(owner_id=self.request.user.id, id=context['tont_id'].id)

        return context
    
    def get_object(self, queryset=None):
        object = Tontine.objects.get(id=self.kwargs['tont_id'])
        return object
    
    def form_valid(self, form):
        # Save the form data
        form.save()
        
        # Get the object's id and name
        object_id = self.kwargs['tont_id']
        object_name = self.kwargs['tontine']
        
        # success message
        message_out_success = format_html(
            f'<strong>{object_name}</strong> mise à jour avec succès.'
        )
        messages.success(
            self.request,
            message_out_success
        )
        
        # Redirect to a different URL
        return redirect(reverse_lazy('core:detail_tontine', kwargs={'pk': self.request.user.id, 'user': self.request.user.username, 'tont_id': object_id, 'tontine': object_name}))
        
    
class DeleteTontine(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Tontine
    template_name = 'tontine/tontine_confirm_delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = get_object_or_404(User, id=self.kwargs["pk"])
        context['user'] = get_object_or_404(User, username=self.kwargs["user"])
        context['tont_id'] = get_object_or_404(Tontine, id=self.kwargs["tont_id"])
        context['tontine'] = get_object_or_404(Tontine, slug=self.kwargs["tontine"])
        context['query'] = Tontine.objects.get(owner_id=self.request.user.id, id=context['tont_id'].id)
        return context
    
    def get_object(self, queryset=None):
        object = Tontine.objects.get(id=self.kwargs['tont_id'])
        return object
    
    def get_success_url(self):
        # Get the object's user that was created
        user = self.request.user

        # Use the reverse_lazy() function to reverse a URL pattern and return the URL as a string
        success_url = reverse_lazy(
            'core:all_tontines', kwargs={'pk': user.id, 'user': user.username})

        return success_url
    
    def form_valid(self, form):
        # Get the object's id and name
        object_name = self.kwargs['tontine']
        
        # success message
        message_out_success = format_html(
            f'<strong>{object_name}</strong> a bien été supprimé de vos tontines.'
        )
        messages.success(
            self.request,
            message_out_success
        )
        return super().form_valid(form)
    
class JoinTontine(LoginRequiredMixin, SuccessMessageMixin, View):
    template_name = 'tontine/tontine_join.html'
    
    def get(self, request, *args, **kwargs):
        pk = get_object_or_404(User, id=self.kwargs["pk"])
        user = get_object_or_404(User, username=self.kwargs["user"])
        
        # Get all Tontines from the DB
        query = Tontine.objects.all()

        context = {
            'pk': pk,
            'user': user,
            'query': query,
        }
        return render(request, self.template_name, context)
    
    
# Custom 404 page


class page_not_found_view(TemplateView):
    template_name = '404.html'
