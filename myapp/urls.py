from django.urls import path
from .views import home
from . import views

urlpatterns = [
    path('' , home, name = 'home') ,
    path("register/" , views.register , name = "register") ,
    path("account/" , views.account_view , name = "account") ,
    path("cards/" , views.card_list , name = "card_list") ,
    path("cards/create/" , views.card_create , name = "card_create") ,
    path("cards/<int:pk>/" , views.card_detail, name = "card_detail") ,
    path("cards/<int:pk>/update/" , views.card_update, name = "card_update") ,
    path("cards/<int:pk>/delete/" , views.card_delete, name = "card_delete") ,
    path( "login/", views.UserLoginView.as_view(), name="login" ),
    path( "logout/", views.UserLogoutView.as_view(), name="logout" ), 
]
