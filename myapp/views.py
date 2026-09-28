from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView

from django.db import transaction
from django.db.models import Q

from .models import User, Account, Card, Transaction
from .forms import ( RegistrationForm, AccountForm, CardForm, TransferForm, CheckPhoneForm, CheckCardForm, )


#home
def home(request):
    return render(request, "home.html")


#authentication
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("account_create")

    else:
        form = RegistrationForm()

    return render(
        request, "register.html", {"form": form} )


class UserLoginView(LoginView):
    template_name = "login.html"


class UserLogoutView(LogoutView):
    next_page = "home"



#account
@login_required
def account_create(request):

    if hasattr(request.user, "account"):
        return redirect("account")

    if request.method == "POST":

        form = AccountForm(request.POST)

        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect("account")

    else:
        form = AccountForm()

    return render( request, "account_create.html", {"form": form} )


@login_required
def account_view(request):
    account = get_object_or_404( Account, user=request.user)
    return render( request, "account.html", {"account": account})


@login_required
def account_update(request):
    account = get_object_or_404( Account, user=request.user )

    if request.method == "POST":
        form = AccountForm(request.POST, instance=account )

        if form.is_valid():
            form.save()
            return redirect("account")
    else:
        form = AccountForm( instance=account )

    return render( request, "account_update.html", {"form": form})



#cards
@login_required
def card_list(request):
    cards = Card.objects.filter( user=request.user)

    return render( request,  "cards/list.html", {"cards": cards} )


@login_required
def card_create(request):
    if request.method == "POST":
        form = CardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            card.save()
            return redirect("card_list")
    else:
        form = CardForm()

    return render( request, "cards/create.html", {"form": form} )



@login_required
def card_detail(request, pk):
    card = get_object_or_404( Card, pk=pk, user=request.user )
    return render( request, "cards/detail.html", {"card": card} )


@login_required
def card_update(request, pk):
    card = get_object_or_404( Card, pk=pk, user=request.user )

    if request.method == "POST":
        form = CardForm( request.POST, instance=card )

        if form.is_valid():
            form.save()

            return redirect( "card_detail", pk=card.pk)
    else:
        form = CardForm( instance=card )

    return render( request, "cards/update.html", {"form": form})

@login_required
def card_delete(request, pk):
    card = get_object_or_404( Card, pk=pk, user=request.user)

    if request.method == "POST":
        card.delete()
        return redirect("card_list")

    return render(request, "cards/delete.html", {"card": card})



#check phone
@login_required
def check_phone(request):
    user = None

    if request.method == "POST":
        form = CheckPhoneForm(request.POST)

        if form.is_valid():
            phone_number = form.cleaned_data[ "phone_number" ]

            user = User.objects.filter( phone_number=phone_number).first()

    else:
        form = CheckPhoneForm()

    return render( request, "check_phone.html",
        {
            "form": form,
            "user": user })


#check card
@login_required
def check_card(request):
    card = None
    if request.method == "POST":
        form = CheckCardForm(request.POST)
        if form.is_valid():
            card_number = form.cleaned_data[  "card_number" ]

            card = Card.objects.filter( card_number=card_number ).select_related( "user" ).first()
    else:
        form = CheckCardForm()

    return render( request, "check_card.html",
        {
            "form": form,
            "card": card })


#transfer
@login_required
def transfer(request):
    if request.method == "POST":
        form = TransferForm(request.POST)

        if form.is_valid():
            source_type = form.cleaned_data[ "source_type" ]
            destination_type = form.cleaned_data[ "destination_type"]
            receiver_phone = form.cleaned_data[ "receiver_phone" ]
            card_number = form.cleaned_data[ "card_number" ]
            amount = form.cleaned_data[ "amount" ]

            #source

            source_account = None
            source_card = None

            if source_type == "account":

                source_account = get_object_or_404( Account, user=request.user)
                if source_account.balance < amount:
                    form.add_error( "amount", "Insufficient account balance." )
                    return render( request, "transfer.html", {"form": form})

            elif source_type == "card":
                source_card = get_object_or_404( Card, user=request.user, card_number=card_number )

                if source_card.balance < amount:
                    form.add_error( "amount", "Insufficient card balance." )
                    return render( request, "transfer.html", {"form": form} )

            #destination
            destination_account = None
            destination_card = None

            if destination_type == "phone":
                receiver = User.objects.filter( phone_number=receiver_phone ).first()

                if receiver is None:
                    form.add_error( "receiver_phone", "User not found." )
                    return render( request, "transfer.html", {"form": form} )
                destination_account = get_object_or_404( Account, user=receiver )


            elif destination_type == "card":
                destination_card = Card.objects.filter( card_number=card_number).select_related("user").first()
                if destination_card is None:
                    form.add_error("card_number",  "Card not found." )
                    return render( request, "transfer.html", {"form": form})
                destination_account = None

            #transaction
            with transaction.atomic():

                if source_account:
                    source_account.balance -= amount
                    source_account.save()

                if source_card:
                    source_card.balance -= amount
                    source_card.save()

                if destination_account:
                    destination_account.balance += amount
                    destination_account.save()

                if destination_card:
                    destination_card.balance += amount
                    destination_card.save()

                receiver = ( destination_card.user
                    if destination_card
                    else destination_account.user )

                Transaction.objects.create(
                    sender =request.user,
                    receiver =receiver,
                    source_type =source_type,
                    destination_type =destination_type,
                    source_card =source_card,
                    destination_card =destination_card,
                    amount =amount )
            return redirect("history")


    else:
        form = TransferForm()
    return render( request, "transfer.html", {"form": form} )


#history
@login_required
def history(request):
    sent = Transaction.objects.filter( sender=request.user)
    received = Transaction.objects.filter( receiver=request.user)
    transactions = ( sent | received ).distinct().order_by( "-created_at" )
    filter_type = request.GET.get( "type", "all" )

    if filter_type == "sent":
        transactions = sent.order_by( "-created_at")

    elif filter_type == "received":
        transactions = received.order_by( "-created_at")

    return render(request, "history.html",
        {
            "transactions": transactions,
            "filter_type": filter_type })



#card history
@login_required
def card_history(request, pk):

    card = get_object_or_404( Card, pk=pk, user=request.user )
    sent = Transaction.objects.filter( source_card=card)
    received = Transaction.objects.filter( destination_card=card )
    transactions = ( sent | received ).distinct().order_by( "-created_at")
    filter_type = request.GET.get( "type", "all" )

    if filter_type == "sent":
        transactions = sent.order_by( "-created_at")

    elif filter_type == "received":
        transactions = received.order_by( "-created_at" )

    return render( request, "card_history.html",
        {
            "card": card,
            "transactions": transactions,
            "filter_type": filter_type  } )