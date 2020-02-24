from django.contrib import admin
from django.urls import path, include
from inmueble import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='inicio'),
    path('paginas/ventas/', views.ventas, name='ventas'),
    path('paginas/arrendamientos/', views.arrendamientos, name='arrendamientos'),

    path('listar/', views.InmuebleView.as_view(), name='listar'),
    path('crear/', views.InmuebleCreate.as_view(), name='crear'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('usuario/', include(('usuario.urls', 'usuario'), namespace='usuario')),
]
