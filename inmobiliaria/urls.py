from django.contrib import admin
from django.urls import path, include
from inmueble import views

# Modulo para buscar archivos en el proyecto
from django.conf.urls.static import static

# Importa el contenido de settings.py
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='inicio'),
    path('paginas/ventas/', views.ventas, name='ventas'),
    path('paginas/arrendamientos/', views.arrendamientos, name='arrendamientos'),

    path('crear/', views.InmuebleCreate.as_view(), name='crear'),

    path('listar/', views.InmuebleView.as_view(), name='listar'),
    path('listar/', views.ImageList.as_view(), name='listar'),

    # Guardar inmuebles
    path('guardar_inmueble/', views.Guardar_inmueble, name='guardar_inmueble'),

    path('<int:pk>/', views.InmuebleUpdate.as_view(), name='editar'),
    path('eliminar/<int:pk>/', views.InmuebleDelete.as_view(), name='eliminar'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('usuario/', include(('usuario.urls', 'usuario'), namespace='usuario')),
]

# Concatenación para buscar archivos
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
