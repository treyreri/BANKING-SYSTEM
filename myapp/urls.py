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
    path("account/create/" , views.account_create, name = "account_create") ,
    path("account/update/" , views.account_update, name = "account_update") ,
    path("cards/<int:pk>/history/" , views.card_history, name = "card_history" ) ,
    path ("check-phone/" , views.check_phone, name = "check_phone") ,
    path("check-card/" , views.check_card, name = "check_card") ,
    path("transfer" , views.transfer, name = "transfer") ,
    path("history/" , views.history, name = "history") ,
]
