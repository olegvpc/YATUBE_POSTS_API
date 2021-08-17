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
            ('index.html', 'index', None),
            ('group.html', 'group', (TestPostImages.group.slug,)),
            ('profile.html', 'profile', (TestPostImages.user.username,)),
            # ('post.html', 'post', (TestPostImages.user.username,
            #                        TestPostImages.post.id)),
        )
        for template, reverse_name, args_value in url_name_arg:
            with self.subTest(reverse_name=reverse_name):
                # cache.clear()
                response = self.authorized_user.get(reverse(
                    reverse_name, args=args_value))
                image_check = response.context['page'][0].image
                print(image_check)
                self.assertEqual(
                    image_check, TestPostImages.post.image.name,)

    def test_new_post_and_post_edit_shows_correct_context(self):
        """
        Приложение posts test_views проверяем context new_post и edit.
        """
        name_patterns = (
            ('new_post', None, True),
            ('post_edit', (TestPostImages.user.username,
                           TestPostImages.post.id), False))

        for name, args_value, value_new in name_patterns:
            with self.subTest(name=name):
                response = self.authorized_user.get(
                    reverse(name, args=args_value))
                self.assertIn('new_post', response.context)
                self.assertIs(response.context['new_post'], value_new)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], PostForm)
                self.assertTrue(Post.objects.filter(
                    text=TestPostImages.post.text,
                    image='posts/small.gif',
                ).exists())
