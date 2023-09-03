from django import forms
from .models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import AuthenticationForm


class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'phone', 'f_name', 'l_name']

    def clean_password2(self):
        data = self.cleaned_data
        if data['password2'] and data['password1'] and data['password2'] != data['password1']:
            raise forms.ValidationError('plz check')
        return data['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField

    class Meta:
        model = User
        fields = ['email', 'phone', 'f_name', 'l_name']

    def clean_password(self):
        return self.initial['password']


class UserRegisterForm(forms.ModelForm):
    password_1 = forms.CharField(max_length=200, label='پسورد',
                                 widget=forms.PasswordInput(attrs={'placeholder': 'پسورد '}))

    class Meta:
        model = User
        fields = ['email', 'phone', 'f_name', 'l_name']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('این ایمیل از قبل وجود دارد')
        return email

    def clean_password_1(self):
        password1 = self.cleaned_data['password_1']
        if len(password1) < 8:
            raise forms.ValidationError('پسورد شما حداقل باید 8 حرف باشد!!!')
        return password1


class UserLoginForm(AuthenticationForm):
    password = forms.CharField(label='پسورد', widget=forms.PasswordInput)
    remember = forms.BooleanField(label='مرا به خاطر بسپار', required=False, widget=forms.CheckboxInput())

    def __init__(self, *args, **kwargs):
        self.error_messages['invalid_login'] = 'پسورد یا نام کاربری اشتباه است'
        super().__init__(*args, **kwargs)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'phone', 'f_name', 'l_name']
        widgets = {
            'f_name': forms.TextInput(attrs={'class': 'myclass'})
        }


class PhoneLoginForm(forms.Form):
    phone = forms.IntegerField()


class VerifyForm(forms.Form):
    code = forms.IntegerField()


class PhoneForgotForm(forms.Form):
    phone = forms.IntegerField()


class VerifyForgotForm(forms.Form):
    code = forms.IntegerField()
