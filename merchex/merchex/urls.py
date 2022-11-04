# ~/projects/django-web-app/merchex/merchex/urls.py

from django.contrib import admin
from django.urls import path
from listings import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bands/', views.band_list, name='band-list'),
    path('bands/<int:id>/', views.band_detail, name='band-detail'),
    path('bands/add/', views.band_create, name='band-create'),
    path('bands/<int:id>/change/', views.band_update, name='band-update'),
    path('bands/<int:id>/delete/', views.band_delete, name='band-delete'),
    
    path('about-us/', views.about),  # ajoutez cette ligne
    path('contact-us/', views.contact, name='contact'),
    path('email-sent/', views.email_sent, name='email-sent'),  # ajoutez cette ligne
]
