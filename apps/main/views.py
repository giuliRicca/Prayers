from django.shortcuts import render
from .models import Prayer
# Create your views here.


def home(request):
	prayers = Prayer.objects.all()

	context = {'prayers':prayers}
	return render(request, 'main/home.html', context)
