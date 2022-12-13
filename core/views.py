from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, HttpResponsePermanentRedirect
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
from django.contrib import messages
from .models import *
from .forms import *

# Create your views here


class HomeView(View):
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
    success_url = reverse_lazy('login')
    form_class = UserRegisterForm
    success_message = "Your account was created successfully"


class LoginView(View):

    template_name = 'login.html'
    initial = {'key': 'value'}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
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
                        return redirect(reverse('home', kwargs={'pk': request.user.id, 'user': request.user.username}))
                else:
                    messages.error(
                        request,
                        f'Login failed! Incorrect username or password.'
                    )
                    return redirect('login')

            return render(request, self.template_name)


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(
            request,
            f'You are now logged out.'
        )
        return redirect('login')
    
class ContactView(View):
    form_class = ContactForm
    initial = {'key': 'value'}
    template_name = 'contact.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            message = form.cleaned_data['message']

            emailSubject = f'{name} <{email}>'

            # Uncomment this later to send email to required address
            # try:
            #     send_mail(
            #         emailSubject, #subject
            #         message, #message
            #         email, #from email
            #         ['joelfah2003@gmail.com'], #to email
            #         fail_silently=False
            #         )
            # except BadHeaderError:
            #     return HttpResponse('Invalid header found')

            # Test if form data was saved and output corresponding flash message to confirm message placement or not.
            try:
                form.save()
                message_out_success = format_html(
                    f'Thanks for contacting us, <strong> {name} </strong> ! Your message has been sent successfully. We will get to you at <strong> {email} </strong> in the meantime.'
                )
                messages.success(
                    request,
                    message_out_success
                )
            except:
                message_out_error = format_html(
                   f'Sorry, <strong> {name} </strong> ! There was a problem sending your message. Please try again to fill the form!'
                )
                messages.error(
                    request,
                    message_out_error
                )
            
            # Redidrect to the same page with message output.
            return redirect('contact')
        else:
            form = ContactForm()

        context = {
            'nbar' : 'contact',
            'form': form
        }
        return render(request, self.template_name, context)

# Custom 404 page


# class page_not_found_view(TemplateView):
#     template_name = '404.html'

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)