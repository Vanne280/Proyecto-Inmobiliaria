from django.contrib import admin
from django.urls import path, include
from inmueble import views

# Modulo para buscar archivos en el proyecto
from django.conf.urls.static import static

# Importa el contenido de settings.py
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # Ruta de la página de Inicio
    path('', views.home, name='inicio'),

    # Ruta de la página de ventas
    path('paginas/ventas/', views.ventas, name='ventas'),
    # path('paginas/arrendamientos/', views.arrendamientos, name='arrendamientos'),

    # Ruta de la página de arrendamientos
    path('paginas/arrendamientos/', views.ImageList.as_view(), name='listar_imagenes'),

    # Ruta de la página para crear inmuebles
    path('crear/', views.InmuebleCreate.as_view(), name='crear'),

    # Ruta de la página para listar los inmuebles
    path('listar/', views.InmuebleView.as_view(), name='listar'),

    # Ruta de la función de guardar inmuebles
    path('guardar_inmueble/', views.Guardar_inmueble, name='guardar_inmueble'),

    # Ruta de la página para editar los inmuebles
    path('<int:pk>/', views.InmuebleUpdate.as_view(), name='editar'),

    # Ruta de la página para eliminar los inmuebles
    path('eliminar/<int:pk>/', views.InmuebleDelete.as_view(), name='eliminar'),

    # Ruta de la página que muestra información de cada inmueble (Detail)
    path('detalle/<int:pk>/', views.InmuebleDetail.as_view(), name='detalle'),

    # Ruta del inicio de sesión
    path('accounts/', include('django.contrib.auth.urls')),

    # Ruta de las urls de la aplicación usuario
    path('usuario/', include(('usuario.urls', 'usuario'), namespace='usuario')),
]

# Concatenación para buscar archivos
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
