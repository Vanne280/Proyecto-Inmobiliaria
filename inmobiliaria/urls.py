from django.contrib import admin
from django.urls import path, include
from inmueble import views

# Modulo para buscar archivos en el proyecto
from django.conf.urls.static import static

# Importa el contenido del archivo settings.py
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # Ruta de la página de Inicio
    path('', views.home, name='inicio'),

    path('buscar/', views.Busqueda, name='buscar'),

    # path('buscar/', views.Buscarinmueble, name='buscar'),

    # Ruta de la página Nosotros
    path('paginas/nosotros/', views.nosotros, name='nosotros'),

    # Ruta de la página Contacto
    path('paginas/contacto/', views.ContactoView.as_view(), name='contacto'),

    # Ruta de la página de ventas
    path('paginas/ventas/', views.VentaList.as_view(), name='ventas'),

    # Ruta de la página de arrendamientos
    path('paginas/arrendamientos/', views.AlquilerList.as_view(), name='arrendamientos'),

    # Ruta de la página para crear inmuebles
    path('crear/', views.Guardar_inmueble, name='crear'),

    # Ruta de la página para listar los inmuebles
    path('listar/', views.InmuebleView.as_view(), name='listar'),

    # Ruta de la función de guardar inmuebles
    # path('guardar_inmueble/', views.Guardar_inmueble, name='guardar_inmueble'),

    # Ruta de la página para editar los inmuebles
    path('<int:pk>/', views.Editar_inmueble, name='editar'),    

    # Ruta de la página que muestra información de cada inmueble (Detail)
    path('detalle/<int:pk>/', views.InmuebleDetail.as_view(), name='detalle'),

    # Ruta de la página para gestionar los proietarios y sus inmuebles
    path('asesor/gestion_inmueble/', views.GestionCreate.as_view(), name='gestion'),

    # Ruta de la página que muestra los propietarios y sus inmuebles
    path('asesor/inmuebles/', views.GestionList.as_view(), name='listar_gestion'),

    # Ruta de la página que edita los propietarios y sus inmuebles
    path('<int:pk>/', views.GestionUpdate.as_view(), name='editar_gestion'),

    # Ruta de la página que elimina los propietarios y sus inmuebles
    path('eliminar/<int:pk>/', views.GestionDelete.as_view(), name='eliminar_gestion'),

    # Ruta de la página mis inmuebles
    path('cliente/mis_inmuebles/', views.MisinmueblesList.as_view(), name='mis_inmuebles'),

    path('cita/', views.Citas_inmuebles.as_view(), name='cita'),

    path('asesor/mis_citas/', views.CitaList.as_view(), name='mis_citas'),

    # Ruta del inicio de sesión
    path('accounts/', include('django.contrib.auth.urls')),

    # Ruta de las urls de la aplicación usuario
    path('usuario/', include(('usuario.urls', 'usuario'), namespace='usuario')),
]

# Concatenación para buscar archivos
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
