from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, User


class PostURLTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Любители музыки',
            slug='test_slug',
            description='Описание тестовой группы')
        cls.user = User.objects.create_user(
            username='test_user')
        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.user,
            group=cls.group)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PostURLTests.user)

    def test_urls_all(self):
        """
        Тест проверки доступных url для авт/неавториз юзеров.
        """
        username = PostURLTests.user.username
        slug = PostURLTests.group.slug
        post_id = PostURLTests.post.id
        authorized_user = self.authorized_client
        url_user_status = (
            ('/', self.client),
            (f'/{username}/', self.client),
            (f'/group/{slug}/', self.client),
            (f'/{username}/{post_id}/', self.client),
            ('/new/', authorized_user),
            (f'/{username}/{post_id}/edit/', authorized_user)
        )
        for url_address, client in url_user_status:
            with self.subTest(adress=url_address):
                response = client.get(url_address)
                self.assertEqual(response.status_code,
                                 HTTPStatus.OK)

    def test_redirect_new_and_post_edit(self):
        """
        Приложение posts test_urls редирект с /new/ и /edit/.
        """
        user_not_author = User.objects.create_user(
            username='test_user_not_author')
        authorized_not_author = Client()
        authorized_not_author.force_login(user_not_author)
        username = PostURLTests.user.username
        post_id = PostURLTests.post.id
        edit_args = reverse("post_edit", args=(username, post_id))
        url_client_redirect = (
            ('/new/', self.client,
             reverse('login') + '?next=' + reverse("new_post")),
            (f'/{username}/{post_id}/edit/', self.client,
             reverse('login') + '?next=' + edit_args),
            (f'/{username}/{post_id}/edit/',
             authorized_not_author,
             reverse('post', args=(username, post_id)))
        )
        for url_address, client, url_redirect in url_client_redirect:
            with self.subTest(adress=url_address):
                response_client = client.get(url_address)
                self.assertRedirects(response_client, url_redirect)

    def test_correct_reverse_names(self):
        """
        Приложение posts test_urls проверка соответствия прямых ссылок
        и полученных через reverse(name).
        """
        username = PostURLTests.user.username
        slug = PostURLTests.group.slug
        post_id = PostURLTests.post.id
        url_name = (
            ('/', 'index', None),
            ('/new/', 'new_post', None),
            (f'/group/{slug}/', 'group', ('test_slug',)),
            (f'/{username}/',
             'profile', (username,)),
            (f'/{username}/{PostURLTests.post.id}/',
             'post', (username, post_id)),
            (f'/{username}/{post_id}/edit/',
             'post_edit', (username, post_id))
        )
        for url_address, name, args_value in url_name:
            with self.subTest(address=url_address):
                self.assertEqual(url_address, reverse(name, args=args_value))

    def test_urls_404(self):
        """
        Тест проверки работы страницы 404.
        """
        response_guest_user = self.client.get('/test/')
        self.assertEqual(response_guest_user.status_code, HTTPStatus.NOT_FOUND)
