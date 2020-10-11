from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .decorators import login_required_message
from .models import Prayer
from django.contrib import messages
from .forms import PrayerForm
# Create your views here.


@login_required(login_url='login')
def home(request):
    if request.user.is_superuser or request.user.is_staff:
        prayers = Prayer.objects.all().order_by('-created')
    else:
        prayers = Prayer.objects.filter(
            author=request.user).order_by('-created')
    context = {'prayers': prayers}
    return render(request, 'main/home.html', context)


@login_required_message(message="Inicio de sesión requerido!")
@login_required(login_url='login')
def new_prayer(request):
    if request.method == 'POST':
        form = PrayerForm(request.POST)
        if form.is_valid():
            prayer = form.save(False)
            prayer.author = request.user
            prayer.save()
            messages.success(request, 'Motivo añadido exitosamente!')
            return redirect('home')
    form = PrayerForm()
    return render(request, 'main/new_prayer.html', {'form': form})


@login_required_message(message="Inicio de sesión requerido!")
@login_required(login_url='login')
def edit_prayer(request, prayer_id):
    try:
        prayer = Prayer.objects.get(id=prayer_id)
    except:
        messages.warning(request, 'Algo ocurrio mal!')
        return redirect('home')
    if request.method == 'POST':
        form = PrayerForm(request.POST, instance=prayer)
        if form.is_valid():
            prayer = form.save()
            messages.success(request, 'Has editado tu motivo')
            return redirect('home')
    form = PrayerForm(instance=prayer)

    context = {'form': form, 'prayer': prayer}
    return render(request, 'main/edit_prayer.html', context)


@login_required_message(message="Inicio de sesión requerido!")
@login_required(login_url='login')
def delete_prayer(request, prayer_id):
    try:
        prayer = Prayer.objects.get(id=prayer_id)
        prayer.delete()
        messages.success(request, 'Has eliminado un motivo')
    except Prayer.DoesNotExist:
        messages.warning(request, "Algo anda mal!")
    return redirect('home')


@login_required_message(message="Inicio de sesión requerido!")
@login_required(login_url='login')
def add_prayer(request, prayer_id):
    try:
        if request.user.profile.praying.count() <= 10:
            p = Prayer.objects.get(id=prayer_id)
            request.user.profile.praying.add(p)
            messages.success(request, 'Oracion añanadida!')
        else:
            messages.warning('Limite de oraciones exedido.')
    except:
        messages.warning(request, 'Algo ocurrio mal!')
    return redirect('account_praying', user_id=request.user.id)


@login_required_message(message="Inicio de sesión requerido!")
@login_required(login_url='login')
def remove_prayer(request, prayer_id):
    try:
        p = Prayer.objects.get(id=prayer_id)
        request.user.profile.praying.remove(p)
    except:
        messages.warning(request, 'Algo ocurrio mal!')

    return redirect('account_praying', user_id=request.user.id)
