import shutil
import tempfile

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..models import Group, Post, User

TEMP_MEDIA = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class PostCreateFormTest(TestCase):

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
        # cls.post = Post.objects.create(
        #     author=cls.user,
        #     text='Тестовый пост с картинкой',
        #     group=cls.group,
        #     image=cls.uploaded)
        cls.form_data = {
            'text': 'Тестовый пост из Класса',
            'group': cls.group.id,
            'image': cls.uploaded,
        }

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PostCreateFormTest.user)

    def test_create_post_by_authorized_user(self):
        """
        Приложение posts test_forms проверка добавления поста
        авторизованным пользователем.
        """
        posts_count = Post.objects.count()
        response = self.authorized_client.post(
            reverse('new_post'), data=PostCreateFormTest.form_data,
            follow=True)
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertRedirects(response, reverse('index'))
        post_latest = Post.objects.first()
        compare_data = (
            (post_latest.text, PostCreateFormTest.form_data['text']),
            (post_latest.group, PostCreateFormTest.group),
            (post_latest.author, PostCreateFormTest.user),
            (post_latest.image,
             f'posts/{PostCreateFormTest.form_data["image"].name}',),
        )
        for post_attr, expected in compare_data:
            with self.subTest(post_attr=post_attr):
                self.assertEqual(post_attr, expected)

    def test_create_post_by_guest_user(self):
        """
        Приложение posts test_forms проверка добавления поста гостем.
        """
        posts_count = Post.objects.count()
        response = self.client.post(
            reverse('new_post'), data=PostCreateFormTest.form_data,
            follow=True)
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertRedirects(response,
                             reverse('login') + '?next=' + reverse('new_post'))

    def test_edit_existing_post_by_author(self):
        """
        Приложение posts test_forms проверка редактирования поста автором.
        """
        post_group = Post.objects.create(
            text='Текст первого поста автора test_user_author',
            author=PostCreateFormTest.user,
            group=PostCreateFormTest.group,
        )
        group_two = Group.objects.create(
            title='Вторая группа',
            slug='test_slug_2',
            description='Описание второй группы')
        post_group_two_data = {
            'text': 'Второй пост test_user_author',
            'group': group_two.id,
        }
        count_posts_before = Post.objects.count()
        params_revers = (post_group.author.username, post_group.id)
        response = self.authorized_client.post(reverse(
            'post_edit', args=params_revers), data=post_group_two_data)
        self.assertRedirects(response, reverse(
            'post', args=params_revers))
        edited_post = Post.objects.get(id=post_group.id)
        test_data = (
            (edited_post.text, post_group_two_data['text']),
            (edited_post.group, group_two),
            (edited_post.author, post_group.author))
        for post_attr, expected in test_data:
            with self.subTest(post_attr=post_attr):
                self.assertEqual(post_attr, expected)
        self.assertEqual(Post.objects.count(), count_posts_before)

    def test_edit_existing_post_not_author(self):
        """
        Приложение posts test_forms проверка ред поста не автором.
        """
        post = Post.objects.create(
            text='Текст поста автора test_user',
            author=PostCreateFormTest.user,
            group=PostCreateFormTest.group)
        user_not_author = User.objects.create_user(
            username='test_user_not_author')
        authorized_not_author = Client()
        authorized_not_author.force_login(user_not_author)
        count_posts_before = Post.objects.count()
        response = authorized_not_author.post(reverse(
            'post_edit', kwargs={
                'username': post.author.username,
                'post_id': post.id}), data=PostCreateFormTest.form_data)
        self.assertRedirects(response, reverse(
            'post', kwargs={'username': post.author.username,
                            'post_id': post.id}))
        edited_post = Post.objects.get(id=post.id)
        self.assertNotEqual(edited_post.text,
                            PostCreateFormTest.form_data['text'])
        test_data = (
            (edited_post.group, post.group),
            (edited_post.author, post.author))
        for post_attr, expected in test_data:
            with self.subTest(post_attr=post_attr):
                self.assertEqual(post_attr, expected)
        self.assertEqual(Post.objects.count(), count_posts_before)
