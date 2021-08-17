import shutil
import tempfile

from django.conf import settings
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..forms import PostForm
from ..models import Group, Post, User

TEMP_MEDIA = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class TestPostImages(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Любители музыки',
            slug='test_slug',
            description='Описание тестовой группы')
        cls.user = User.objects.create_user(username='test_user')
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif')

        cls.post = Post.objects.create(
            author=TestPostImages.user,
            text='Тестовый пост с картинкой',
            group=cls.group,
            image=cls.uploaded)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        cache.clear()
        self.authorized_user = Client()
        self.authorized_user.force_login(TestPostImages.user)

    def test_image_contains_in_pages(self):
        url_name_arg = (
            ('index', None),
            ('group', (TestPostImages.group.slug,)),
            ('profile', (TestPostImages.user.username,)))
        for reverse_name, args_value in url_name_arg:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_user.get(reverse(
                    reverse_name, args=args_value))
                image_check = response.context['page'][0].image
                self.assertEqual(
                    image_check, TestPostImages.post.image.name)
        response_post = self.authorized_user.get(
            reverse('post', args=(TestPostImages.user.username,
                                  TestPostImages.post.id)))
        self.assertEqual(response_post.context['post'].image,
                         TestPostImages.post.image.name)


class PostsViewsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Любители музыки',
            slug='test_slug',
            description='Описание тестовой группы')
        cls.user_author = User.objects.create_user(
            username='test_user_author')
        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.user_author,
            group=cls.group)

    def setUp(self):
        cache.clear()
        self.authorized_client_author = Client()
        self.authorized_client_author.force_login(self.post.author)

    def test_pages_use_correct_templates(self):
        """
        Приложение posts test_views шаблонов URL-адресов.
        """
        username = PostsViewsTests.post.author.username
        post_id = PostsViewsTests.post.id
        templates_pages_names = (
            ('index.html', 'index', None),
            ('new_edit_post.html', 'new_post', None),
            ('new_edit_post.html', 'post_edit', (username, post_id)),
            ('group.html', 'group', ('test_slug',)),
            ('post.html', 'post', (username, post_id)),
            ('profile.html', 'profile', (username,))
        )
        for template, name, args_value in templates_pages_names:
            with self.subTest(name=name):
                response = self.authorized_client_author.get(reverse(
                    name, args=args_value))
                self.assertTemplateUsed(response, f'posts/{template}')
                self.assertIn('utf-8', response.charset)

    def context_post_check(self, context, one_post=False):
        if one_post:
            self.assertIn('post', context)
            post = context['post']
        else:
            self.assertIn('page', context)
            self.assertNotEqual(len(context.get('page')), 0)
            post = context['page'][0]
        self.assertEqual(post.text, PostsViewsTests.post.text)
        self.assertEqual(post.author, PostsViewsTests.post.author)
        self.assertEqual(post.group, PostsViewsTests.post.group)
        self.assertEqual(post.pub_date, PostsViewsTests.post.pub_date)

    def test_index_page_shows_correct_context(self):
        """
        Приложение post test_views -index контекст.
        """
        # cache.clear()
        response = self.client.get(reverse('index'))
        self.context_post_check(response.context, one_post=False)

    def test_group_page_shows_correct_context(self):
        """
        Шаблон group сформирован с правильным контекстом.
        """
        response = self.client.get(reverse(
            'group', kwargs={'slug': PostsViewsTests.group.slug}))
        self.assertIn('group', response.context)
        group = response.context['group']
        self.assertEqual(group.title, PostsViewsTests.group.title)
        self.assertEqual(group.slug, PostsViewsTests.group.slug)
        self.assertEqual(group.description, PostsViewsTests.group.description)
        self.context_post_check(response.context, one_post=False)

    def test_profile_page_shows_correct_context(self):
        """
        Приложение post test_views profile контекст.
        """
        response = self.client.get(reverse(
            'profile', kwargs={'username': PostsViewsTests.user_author}))
        self.assertIn('author', response.context)
        self.assertEqual(response.context['author'],
                         PostsViewsTests.post.author)
        self.context_post_check(response.context, one_post=False)

    def test_post_page_shows_correct_context(self):
        """
        Приложение post test_views отдельный пост контекст.
        """
        response = self.client.get(reverse(
            'post', kwargs={'username': PostsViewsTests.post.author.username,
                            'post_id': PostsViewsTests.post.id}))
        self.context_post_check(response.context, one_post=True)

    def test_new_post_and_post_edit_shows_correct_context(self):
        """
        Приложение posts test_views проверяем context new_post и edit.
        """
        name_patterns = (
            ('new_post', None, True),
            ('post_edit', (PostsViewsTests.user_author.username,
                           PostsViewsTests.post.id), False))

        for name, args_value, value_new in name_patterns:
            with self.subTest(name=name):
                response = self.authorized_client_author.get(
                    reverse(name, args=args_value))
                self.assertIn('new_post', response.context)
                self.assertIs(response.context['new_post'], value_new)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], PostForm)

    def test_cache_index(self):
        response = self.client.get(reverse('index'))
        Post.objects.create(
            text='Второй пост- запись- cache',
            author=PostsViewsTests.user_author)
        response_2 = self.client.get(reverse('index'))
        self.assertEqual(response.content, response_2.content)
        cache.clear()
        response_3 = self.client.get(reverse('index'))
        self.assertNotEqual(response_3.content, response_2.content)
        self.assertEqual(len(response_3.context['page'].object_list), 2)


class PostsViewsEditTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Любители музыки',
            slug='test_slug',
            description='Описание тестовой группы')
        cls.group_2 = Group.objects.create(
            title='Любители тестов',
            slug='tests_are_life',
            description='Пол царства за тесты')
        cls.user = User.objects.create_user(
            username='test_user')
        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.user,
            group=cls.group)

    def test_post_gets_right_group(self):
        """
        Приложение posts test_views наличие группы и поста в ней.
        """
        # Пост с группой есть в группе tests_slug
        cache.clear()
        response_group = self.client.get(
            reverse('group', kwargs={'slug': PostsViewsEditTests.group.slug}))
        self.assertIn('group', response_group.context)
        self.assertIn('page', response_group.context)
        self.assertEqual(response_group.context['group'],
                         PostsViewsEditTests.group)
        self.assertEqual(response_group.context['page'][0].id,
                         PostsViewsEditTests.post.id)
        # Пост с новой группой попал на главную страницу
        response_post = self.client.get(reverse('index'))
        self.assertIn('page', response_post.context)
        self.assertEqual(response_post.context['page'][0].id,
                         PostsViewsEditTests.post.id)

    def test_post_doesnt_get_wrong_group(self):
        """
        Приложение posts test_views пост не попал во вторую группу.
        """
        #  Вторая группа tests_are_life создана а поста нет во второй группе
        response_group = self.client.get(
            reverse('group', args=(PostsViewsEditTests.group_2.slug,)))
        self.assertIn('group', response_group.context)
        self.assertIn('page', response_group.context)
        self.assertEqual(response_group.context['group'],
                         PostsViewsEditTests.group_2)
        self.assertEqual(len(response_group.context['page'].object_list), 0)


class PaginatorViewsTest(TestCase):
    """
    Приложение posts test_views paginator проверка зазбиения page.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_user')
        cls.count_posts = settings.PAGE_CONSTANT + 3
        objs = (Post(text='Test %s' % i,
                     author=cls.user)
                for i in range(cls.count_posts))
        Post.objects.bulk_create(objs)

    def test_first_index_page_contains_page_constant(self):
        """
        Приложение posts test_views paginator ограничение постов на странице.
        """
        cache.clear()
        response = self.client.get(reverse('index'))
        self.assertEqual(len(response.context.get('page')),
                         settings.PAGE_CONSTANT)

    def test_second_index_page_contains_records(self):
        """
        Приложение posts test_views paginator вторая страница.
        """
        response = self.client.get(reverse('index'), {'page': 2})
        self.assertEqual(len(
            response.context.get('page')),
            PaginatorViewsTest.count_posts - settings.PAGE_CONSTANT)
