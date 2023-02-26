from django.test import Client, TestCase
from django.urls import reverse

from ..models import Follow, Post, User


class PostsFollowTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='test_user')
        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.user)
        cls.user_subscriber = User.objects.create_user(
            username='test_user_subscriber')
        cls.user_post = User.objects.create_user(
            username='test_user_post')

    def setUp(self):
        self.authorized_client_subscriber = Client()
        self.authorized_client_subscriber.force_login(
            PostsFollowTests.user_subscriber)

    def test_authorized_user_subscribe(self):
        """
        Приложение posts test_follow проверка подписки
        авторизованным пользователем.
        """
        # Считаем подписчиков до подписки
        follower_before = Follow.objects.count()
        self.authorized_client_subscriber.get(reverse(
            'profile_follow', args=(self.user.username,)))
        response = self.authorized_client_subscriber.get(reverse(
            'profile', args=(self.user.username,)))
        self.assertIn('following', response.context)
        self.assertTrue(response.context['following'])
        self.assertEqual(Follow.objects.count(), follower_before + 1)
        subscriber = Follow.objects.last()
        compare_date = (
            (subscriber.user, PostsFollowTests.user_subscriber),
            (subscriber.author, PostsFollowTests.user))
        for attr, expected in compare_date:
            with self.subTest(attr=attr):
                self.assertEqual(attr, expected)

    def test_subscriber_follow_index(self):
        """
        Приложение posts test_follow проверка появления поста
        подписанного автора в ленте.
        """
        self.authorized_client_subscriber.get(reverse(
            'profile_follow', args=(self.user.username,)))
        response_subscriber = self.authorized_client_subscriber.get(reverse(
            'follow_index'))
        # Запись поста появилась в ленте подписчика
        self.assertEqual(response_subscriber.context['page'][0],
                         PostsFollowTests.post)

    def test_authorized_user_unsubscribe(self):
        """
        Приложение posts test_follow проверка отпписки
        авторизованным пользователем от автора постов.
        """
        # Считаем подписчиков до подписки
        follower_before = Follow.objects.count()
        self.authorized_client_subscriber.get(reverse(
            'profile_follow', args=(self.user.username,)))
        # Подписчиков на одного больше
        self.assertEqual(Follow.objects.count(), follower_before + 1)
        self.authorized_client_subscriber.get(reverse(
            'profile_unfollow', args=(self.user.username,)))
        # Подписчиков столькоже сколько было по подписки
        self.assertEqual(Follow.objects.count(), follower_before)

    def test_non_subscriber_follow_index(self):
        """
        Приложение posts test_follow тест, что пользователь не видит посты
        авторов на которых не подписан.
        """
        Post.objects.create(author=PostsFollowTests.user_post,
                            text='test follow text')
        # Количество постов до подписки
        follower_before = Follow.objects.count()
        self.authorized_client_subscriber.get(reverse(
            'profile_follow', args=(PostsFollowTests.user.username,)))
        # Подписчиков на одного больше
        self.assertEqual(Follow.objects.count(), follower_before + 1)
        response_user = self.authorized_client_subscriber.get(reverse(
            'follow_index'))
        # Всего постов два
        self.assertEqual(Post.objects.count(), 2)
        # Два поста - на странице один- с контекстом подписанного автора
        self.assertEqual(len(response_user.context['page']), 1)
        self.assertEqual(response_user.context['page'][0],
                         PostsFollowTests.post)
