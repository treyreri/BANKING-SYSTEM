from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm

# Create your views here.
#В Django представление (view) может быть написано двумя способами: 
# через функции (Function-Based Views, FBV) и через классы (Class-Based Views, CBV)

def home(request):
    return render(request, "home.html")

from django.contrib.auth import login

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("account")
    else:
        form = RegistrationForm()
    return render(request, "register.html" , {"form" : form})


from django.contrib.auth.views import LoginView, LogoutView

class UserLoginView(LoginView): #Этот встроенный класс уже умеет принимать логин и пароль, проверять их через форму AuthenticationForm и аутентифицировать пользователя
    template_name = "login.html"

class UserLogoutview(LogoutView):
    next_page = "home"

from django.contrib.auth.decorators import login_required #Импортируется декоратор для проверки авторизации

@login_required
def account_view(request):
    account = request.user.account
    return render(request, "account.html", {"account" : account})



#CRUD для карт
from .models import Card
from .forms import CardForm
@login_required
def card_list(request):
    cards = Card.objects.filter(user = request.user)
    return render(request, "cards/list.html" , {"cards" : cards})

@login_required
def card_create(request):
    if request.method == "POST":
        form = CardForm(request.POST)

        if form.is_valid():
            card = form.save(commit = False)
            card.user = request.user
            card.save()
            return redirect("card_list")
    else:
        form = CardForm()
    return render(request, "cards/create.html" , {"form" : form})


@login_required
def card_detail(request, pk):
    card = Card.objects.get(pk = pk, user = request.user) #эта часть не даёт человеку открыть чужую карту
    return render(request, "cards/detail.html" , {"card" : card})

from django.shortcuts import get_object_or_404
@login_required
def card_update(request, pk):
    card = get_object_or_404(Card, pk=pk, user=request.user) # ищем карточку по первичному ключу (pk), проверяя, 
                                                        #что она принадлежит текущему вошедшему пользователю (user = request.user)

    if request.method == "POST":
        form = CardForm(request.POST, instance = card)
        if form.is_valid():
            form.save()
            return redirect("card_detail" , pk = card.pk)
    else: 
        form = CardForm(instance = card)
    return render(request, "cards/update.html" , {"form" : form})

@login_required
def card_delete(request, pk):
    card = get_object_or_404(Card, pk=pk, user=request.user)
    if request.method == "POST":
        card.delete()
        return redirect("card_list")
    return render(request, "cards/delete.html", {"card" : card})