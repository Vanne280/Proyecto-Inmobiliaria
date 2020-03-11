from django.urls import path

from .views import signup, ActivateUser, templateEmailSent, UserList
# UserApp

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('activate/<str:uidb64>/<str:token>/', ActivateUser, name='activate'),
    path('emailsent/<str:username>/', templateEmailSent, name='emailsent'),
    path('listar/', UserList.as_view(), name="listar"),
    # path('userapp/', UserApp, name="userapp"),
]
