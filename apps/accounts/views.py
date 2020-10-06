from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
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
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required(login_url='login')
def account_page(request, user_id):
    try:
        account = User.objects.get(id=user_id)
    except:
        account = None
        messages.warning(request, 'No account found')
    return render(request, 'accounts/account.html', {'account': account})


@login_required(login_url='login')
def update_account(request):
    if request.method == 'POST':
        print(request.FILES)
        form = UserUpdateForm(data=request.POST, instance=request.user)
        profile_form = ProfileForm(
            data=request.POST, files=request.FILES, instance=request.user.profile)
        if form.is_valid() and profile_form.is_valid():
            user_form = form.save()
            custom_form = profile_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            return redirect('account')

    else:
        form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    context = {'profile_form': profile_form, 'form': form}
    return render(request, 'accounts/update_account.html', context)


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


def password_reset_confirm(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        messages.success(
            request, 'Tu contraseña ha sido cambiada exitosamente!')
        return redirect('login')
