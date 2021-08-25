from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Group(models.Model):
    title = models.CharField(verbose_name="Имя группы", max_length=200)
    slug = models.SlugField(verbose_name="slug-URL", unique=True)
    description = models.TextField(verbose_name="Увлечение", blank=True)

    class Meta:
        verbose_name = "Группа по интересам"
        verbose_name_plural = "Группы по интересам"

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(verbose_name="Текст поста")
    pub_date = models.DateTimeField(verbose_name="Дата публикации",
                                    auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="posts",
                               verbose_name="Автор поста")
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, blank=True,
                              null=True, verbose_name="Группа по увлечениям",
                              related_name="posts")
    image = models.ImageField(upload_to="posts/", blank=True, null=True,
                              verbose_name="Картинка к посту")

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Пост пользователя"
        verbose_name_plural = "Посты пользователей"

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True,
                             null=True, verbose_name="Комментарии к посту",
                             related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="comments",
                               verbose_name="Автор комментария")
    text = models.TextField(verbose_name="Текст комментария")
    created = models.DateTimeField(verbose_name="Дата публикации комментария",
                                   auto_now_add=True)

    class Meta:
        ordering = ("-created",)
        verbose_name = "Комментарий поста"
        verbose_name_plural = "Комментарии постов"

    def __str__(self):
        return self.text[:15]


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="follower",
                             verbose_name="Подписчик")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="following",
                               verbose_name="Автор поста Подписчика")

    class Meta:
        verbose_name_plural = "Подписки"
        verbose_name = "Подписка"
        constraints = (
            models.UniqueConstraint(fields=("user", "author"),
                                    name="unique_list"),
            models.CheckConstraint(check=~models.Q(user=models.F("author")),
                                   name="author")
        )

    def __str__(self):
        return f'Подписчик {self.user.username} автора- {self.author.username}'


class Avatar(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                verbose_name="Аватар Пользователя")
    image = models.ImageField(upload_to="about/", blank=True, null=True,
                              verbose_name="Картинка аватара")
    date_of_birth = models.DateField(verbose_name="Дата рождения",
                                     null=True)
    city = models.CharField(verbose_name="Город проживания", max_length=30,
                            blank=True, default='Москва')

    class Meta:
        verbose_name_plural = "Данные пользователя"
        verbose_name = "Данные пользователя"

    def __str__(self):
        return f"{self.user.username} родился {self.date_of_birth}"
