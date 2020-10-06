from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django import forms
from django.core.exceptions import ValidationError


class CustomUserCreationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'usuario', 'class': 'form-control'}),
        min_length=4, max_length=150)
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'correo electronico', 'class': 'form-control'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'contraseña', 'class': 'form-control'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'confirmar contraseña', 'class': 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Usuario existente")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Correo electronico asociado a una cuenta")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden!")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user


class ProfileForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Cuentanos sobre ti.'}))
    role = forms.CharField(
        widget=forms.Select(choices=Profile.ROLE_CHOICES, attrs={'class': 'form-control'}))
    image = forms.ImageField(widget=forms.ClearableFileInput(
        attrs={'name': 'profile_image'}), label='Imagen')

    class Meta:
        model = Profile
        fields = ['image', 'bio', 'role']


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'usuario'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'correo electronico'}))

    class Meta:
        model = User
        fields = ['username', 'email']
