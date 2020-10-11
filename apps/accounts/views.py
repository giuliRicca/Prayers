from django.shortcuts import render, redirect
from django.contrib import auth, messages
from apps.main.models import Prayer
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from apps.main.decorators import login_required_message
from.forms import CustomUserCreationForm, ProfileForm, UserUpdateForm
# Create your views here.


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            # correct username and password login the user
            auth.login(request, user)
            return redirect('home')
        else:
            messages.warning(request, 'Usuario o contraseña invalido')

    return render(request, 'accounts/login.html')


@login_required_message(message="Inicio de sesión requerido!")
@login_required(login_url='login')
def logout_page(request):
    auth.logout(request)
    messages.success(request, 'Session cerrada con exito')
    return redirect('login')


def register_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada exitosamente!')
            return redirect('login')
    form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


@login_required_message(message="Inicio de sesión requerido!")
@login_required(login_url='login')
def account_page(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        prayers = Prayer.objects.filter(author=user)
    except:
        user = None
        prayers = None
        messages.warning(request, 'No account found')

    context = {'account': user, 'prayers': prayers}
    return render(request, 'accounts/account.html', context)


@login_required_message(message="Inicio de sesión requerido!")
@login_required(login_url='login')
def update_account(request):
    if request.method == 'POST':
        form = UserUpdateForm(data=request.POST, instance=request.user)
        profile_form = ProfileForm(
            data=request.POST, files=request.FILES, instance=request.user.profile)
        if form.is_valid() and profile_form.is_valid():
            user_form = form.save()
            custom_form = profile_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            return redirect('account', user_id=request.user.id)

    else:
        form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    context = {'profile_form': profile_form, 'form': form}
    return render(request, 'accounts/update_account.html', context)


@login_required_message(message="Inicio de sesión requerido!")
@login_required(login_url='login')
def delete_account(request):
    if request.method == 'POST':
        try:
            u = User.objects.get(username=request.user.username)
            u.delete()
            messages.success(request, "Usuario eliminado exitosamente")
            return redirect('login')
        except User.DoesNotExist:
            messages.warning(request, "Usuario no existe")
            return redirect('login')
        except Exception as e:
            messages.warning(request, e.message)
            return redirect('login')
    return render(request, 'accounts/delete_account.html')


@login_required_message(message="Inicio de sesión requerido!")
@login_required(login_url='login')
def account_praying(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        user = None
        messages.warning(request, 'El usuario no existe')
    context = {'account': user}
    return render(request, 'accounts/account_praying.html', context)


def password_reset_confirm(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        messages.success(
            request, 'Tu contraseña ha sido cambiada exitosamente!')
        return redirect('login')
