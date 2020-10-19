from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('new_prayer/', views.new_prayer, name='new_prayer'),
    path('edit_prayer/<str:prayer_id>/', views.edit_prayer, name='edit_prayer'),
    path('delete_prayer/<str:prayer_id>/',
         views.delete_prayer, name='delete_prayer'),
    path('add_prayer/<str:prayer_id>/',
         views.add_prayer, name='add_prayer'),
    path('remove_prayer/<str:prayer_id>/',
         views.remove_prayer, name='remove_prayer'),
]
