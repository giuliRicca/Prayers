from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .decorators import login_required_message
from .models import Prayer
from django.contrib import messages
from .forms import PrayerForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


@login_required(login_url='login')
def home(request):
    if request.user.is_superuser or request.user.is_staff:
        prayers = Prayer.objects.all().order_by('-created')
    else:
        prayers = Prayer.objects.filter(
            author=request.user).order_by('-created')
    query = request.GET.get('q')
    if query:
        prayers = prayers.filter(
            Q(title__icontains=query) |
            Q(body__icontains=query) |
            Q(author__username__icontains=query))
    category = request.GET.get('category')
    if category:
        prayers = prayers.filter(category=category)
    paginator = Paginator(prayers, 6)
    page_number = request.GET.get('page')
    try:
        response = paginator.page(page_number)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)

    categories = Prayer.PRAYER_CATEGORIES

    context = {'response': response, 'categories': categories}
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
@login_required
@user_passes_test(lambda u: u.groups.filter(name='equipo').exists() or u.is_superuser,
                  login_url='login')
def add_prayer(request, prayer_id):
    try:
        user = User.objects.get(id=request.GET.get('user_id'))
    except:
        user = request.user
    try:
        if user.profile.praying.count() <= 10:
            p = Prayer.objects.get(id=prayer_id)
            user.profile.praying.add(p)
            if request.user == user:
                messages.success(request, 'Oración guardada!')
            else:
                messages.success(
                    request, 'Oracion asignada a ' + user.username)
                return redirect('home')
        else:
            messages.warning('Limite de oraciones exedido.')
    except:
        messages.warning(request, 'Algo ocurrio mal!')
    return redirect(request.META.get('HTTP_REFERER'))


@user_passes_test(lambda u: u.is_superuser)
def assign_prayer(request, prayer_id):
    try:
        prayer = Prayer.objects.get(id=prayer_id)
        users = User.objects.filter(groups__name='equipo')
        staff = []
        for user in users:
            if not user.profile.praying.filter(id=prayer.id).exists() and user != prayer.author:
                staff.append(user)

        print(staff)
    except:
        staff = None

    context = {'staff': staff, 'prayer': prayer}
    return render(request, 'main/assign_prayer.html', context)


@ login_required_message(message="Inicio de sesión requerido!")
@ login_required(login_url='login')
def remove_prayer(request, prayer_id):
    try:
        p = Prayer.objects.get(id=prayer_id)
        request.user.profile.praying.remove(p)
        messages.info(request, 'Oración removida de tus guardados')
    except:
        messages.warning(request, 'Algo ocurrio mal!')

    return redirect(request.META.get('HTTP_REFERER'))
