from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Номер телефона обязателен")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(phone_number, password, **extra_fields)

class User(AbstractUser):
        username = None
        phone_number = models.CharField(max_length=20, unique=True)
        USERNAME_FIELD = "phone_number" #Указывает Django, какое именно поле модели будет использоваться в качестве уникального идентификатора (логина) при входе в систему
        REQUIRED_FIELDS = [] #Оставив REQUIRED_FIELDS = [] пустым, вы говорите Django: «При выполнении команды createsuperuser запрашивай только номер телефона и пароль
        objects = UserManager()  # Подключаем кастомный менеджер

class Account(models.Model):
        user = models.OneToOneField(User, on_delete = models.CASCADE, related_name="account") #Благодарю related_name="account", вы теперь можете от объекта пользователя (user) сразу обратиться к его счету через user.account
        first_name = models.CharField(max_length=100)
        last_name = models.CharField(max_length=100)
        address = models.CharField(max_length=230)
        passport_id = models.CharField(max_length=50, unique=True)
        balance = models.DecimalField(max_digits=12, decimal_places=2, default=1000) #Всего цифр в числе , Из них цифр после запятой, и по умолчанию

        def __str__(self):
                return f"{self.first_name} {self.last_name}"


class Card(models.Model):
        CARD_TYPES = [ ("VISA" , "Visa") , ("MASTERCARD" , "Mastercard") ]
        user = models.ForeignKey( User, on_delete=models.CASCADE, related_name = "cards" )
        card_number = models.CharField(max_length=16, unique=True)
        cvv = models.CharField(max_length=5)
        date = models.DateField()
        type = models.CharField(max_length=20, choices=CARD_TYPES)
        pin = models.DecimalField(max_digits=12, decimal_places=2, default=500)

        def __str__(self):
                return self.card_number

class Transaction(models.Model):
        sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "send_transactions")
        receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "received_transactions")
        source_type = models.CharField(max_length=20)
        destination_type = models.CharField(max_length=20)
        source_card = models.ForeignKey(Card, on_delete=models.SET_NULL, null = True, blank = True, related_name = "send_transactions")
        destination_card = models.ForeignKey(Card, on_delete = models.SET_NULL, null = True, blank = True, related_name = "received_transactions")
        amoint = models.DecimalField(max_digits=12, decimal_places=2)
        created_at = models.DateTimeField(auto_now_add=True)