from django.contrib import admin
from django.urls import path
from inmueble import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('paginas/ventas/', views.ventas, name='ventas'),
    path('paginas/arrendamientos/', views.arrendamientos, name='arrendamientos'),
]
