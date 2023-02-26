from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")
        help_texts = {
            "first_name": "Имя",
            "last_name": "Фамилия",
            "email": "e-mail",
            "username": "короткий NICK-NAME латинскими буквами",
        }
