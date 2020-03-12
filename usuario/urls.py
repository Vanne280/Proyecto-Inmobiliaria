from django.urls import path

from .views import signup, ActivateUser, templateEmailSent, UserList, UserData
#UserUpdate

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('activate/<str:uidb64>/<str:token>/', ActivateUser, name='activate'),
    path('emailsent/<str:username>/', templateEmailSent, name='emailsent'),
    path('listar/', UserList.as_view(), name="listar"),
    path('userdata/', UserData, name="userdata"),

    #path('/<int:pk>/', UserUpdate.as_view(), name="editar"),
]
