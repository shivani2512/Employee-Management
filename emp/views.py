from django.shortcuts import render,redirect, get_object_or_404
from .forms import UserForm, ProfileForm
from .models import User, Profile
from django.views.generic import (TemplateView, ListView,
                                  DetailView, UpdateView)
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .backends import EmailBackend
from django.core.mail import send_mail
from django.conf import settings


def login_user(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    user = EmailBackend.authenticate(username=email, password=password)
    # print(user.username, user.password)
    if user:
        if user.is_active:
            login(request, user, backend='emp.backends.EmailBackend')
            return HttpResponseRedirect(reverse('index'))
        else:
            print("Not active")
    else:
        print("wrong person tried to access.")
    return render(request, 'login.html', {})


@login_required()
def logout_user(request):
    logout(request)
    return redirect('index')


def registration(request):
    register = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            register = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = ProfileForm()

    return render(request, 'register.html', {'user_form': user_form,
                                             'profile_form': profile_form,
                                             'register': register})


class Index(TemplateView):
    model = Profile
    template_name = 'index.html'


class UserList(ListView):
    context_object_name = 'user'
    # model = User
    model = Profile
    template_name = 'userlist.html'


class Emplist(ListView):
    context_object_name = 'user'
    # model = User
    model = Profile
    template_name = 'emplist.html'


class UserDetail(DetailView):
    context_object_name = 'user'
    model = Profile
    template_name = 'userdetail.html'


class UserUpdate(UpdateView):
    model = Profile
    fields = '__all__'
    template_name = 'userupdate.html'
    # success_url = reverse_lazy('list')
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('emp:detail', kwargs={'pk': pk})


def user_change_status(request, pk=None):
    if pk:
        user = Profile.objects.get(pk=pk)
        # print(user.pk)
        if user.user.is_employee == False:
            user.user.employee = True
            user.user.save()
            email = user.user.email
            # print(email)
            subject = 'Hello Employee'
            message = 'Congrats, Now you are now employee'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            mail = send_mail(subject, message, email_from, recipient_list, fail_silently=False)
            # if mail == True:
            #     print("sent it")
            # else:
            #     print("Error")
            return render(request, "empcreate.html", {"user": user})
        else:
            user.user.employee = False
            user.user.save()
            return render(request, "empdelete.html", {"user": user})
    return render(request, "index.html", {})


