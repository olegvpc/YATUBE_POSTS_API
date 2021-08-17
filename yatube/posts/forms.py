from django.forms import ModelForm

from .models import Avatar, Comment, Post, User


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        help_texts = {
            'text': 'Использовать нормативную лексику',
            'group': 'Выбери что тебя интересует',
        }


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
        help_texts = {
            'text': 'Использовать нормативную лексику',
        }


class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')
        help_texts = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'e-mail',
            'username': 'NICK-name- латинскими буквами'
        }


class AvatarForm(ModelForm):

    class Meta:
        model = Avatar
        fields = ('city', 'date_of_birth', 'image')
        help_texts = {
            'city': 'город проживания',
            'date_of_birth': 'введите дату в формате: ДД.ММ.ГГГГ',
            'image': 'картинка себя любимого',
        }
