from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import *
from .models import User, Mobile, PhoneLoginUser
from django.contrib.auth import login
from datetime import datetime
from django.views import View
from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordChangeForm
from random import randint
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from order.models import Order
from home.models import UserWishlist
from django.contrib.messages.views import SuccessMessageMixin


# user register
class RegisterUser(View):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(email=data['email'], phone=data['phone'],
                                            f_name=data['f_name'], l_name=data['l_name'],
                                            create=datetime.now(),
                                            password=data['password_1'])

            login(request, user)
            return redirect('home:home')
        return render(request, self.template_name, {'form': form})


# user login
class LoginUser(auth_views.LoginView):
    template_name = 'accounts/login.html'
    form_class = UserLoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        remember = form.cleaned_data['remember']

        if remember:
            self.request.session.set_expiry(10)
        else:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super(LoginUser, self).form_valid(form)


# user profile
class ProfileUser(LoginRequiredMixin, DetailView):
    template_name = 'accounts/profile.html'
    context_object_name = 'users'

    def get_queryset(self, *args, **kwargs):
        queryset = User.objects.filter(id=self.request.user.id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProfileUser, self).get_context_data(**kwargs)
        context.update({
            'orders': Order.objects.filter(user_id=self.request.user.id),
            'data': get_object_or_404(UserWishlist, user_id=self.request.user.id)
        })
        return context


# user update profile
class UpdateUser(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'accounts/update.html'
    fields = ['f_name', 'l_name', 'phone']
    success_message = 'done!'


    def get_queryset(self):
        queryset = User.objects.filter(id=self.request.user.id)
        return queryset

    def get_success_url(self):
        return reverse('accounts:profile', kwargs={'pk': self.request.user.id})


# user update password profile
class ChangeUser(LoginRequiredMixin, auth_views.PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'accounts/change.html'
    success_url = reverse_lazy('accounts:login')
    context_object_name = 'users'


# user update password profile
class PhoneForgot(View):
    form_class = PhoneForgotForm

    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/phone.html', {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            rand_num = randint(1, 999)
            # code = ???
            Mobile.objects.create(phone_number=phone, code=rand_num)
            return redirect('accounts:verify')
        else:
            return redirect('home:home')


# user update password profile
class VerifyForgot(View):
    form_class = VerifyForgotForm
    template_name = 'accounts/verify.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                phone = Mobile.objects.get(code=data['code']).phone_number
                user = User.objects.get(phone=phone)
                Mobile.objects.get(code=data['code']).delete()
                return redirect('accounts:confirm', user.id)
            except:
                return redirect('home:home')


# user update password profile
class ConfirmForgot(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/confirm.html', )

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=kwargs['pk'])
            pass1 = request.POST['password1']
            pass2 = request.POST['password2']
            if pass1 == pass2:
                user.password = make_password(pass1)
                user.save()
                return redirect('accounts:login')
            else:
                return redirect('home:home')
        except:
            return redirect('accounts:register')


# user login phone
class LoginPhone(View):
    form_class = PhoneLoginForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/phone_login.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            rand_num = randint(1, 9999)
            # code = ???
            PhoneLoginUser.objects.create(phone_number=phone, code=rand_num)
            return redirect('accounts:phone_verify')
        else:
            return redirect('accounts:phone_verify')


# user login phone
class VerifyPhone(View):
    form_class = VerifyForm
    template_name = 'accounts/verify_phone.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                phone = PhoneLoginUser.objects.get(code=data['code']).phone_number
                user = User.objects.get(phone=phone)
                login(request, user)
                messages.success(request, 'hi user')
                PhoneLoginUser.objects.get(code=data['code']).delete()
                return redirect('home:home')
            except:
                messages.error(request, 'کد شما اشتباه است')
                return redirect('accounts:register')
