from django.urls import path
from usuario import views
#UserUpdate

urlpatterns = [

    # Ruta de la página de registro de usuario
    path('signup/', views.signup, name='signup'),

    # Ruta de la página de para realizar la activación de la cuenta
    path('emailsent/<str:username>/', views.templateEmailSent, name='emailsent'),

    # Ruta de la página que muestra la cuenta activada
    path('activate/<str:uidb64>/<str:token>/', views.ActivateUser, name='activate'),

    # Ruta de la página que lista los usuarios
    path('listar/', views.UserList.as_view(), name="listar"),

]
