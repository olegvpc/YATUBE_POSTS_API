from django.test import TestCase

from ..models import Group, Post, User


class PostGroupModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Любители музыки',
            slug='test_slug',
            description='Описание тестовой группы')
        cls.author = User.objects.create_user(username='TestAuthor')
        cls.post = Post.objects.create(
            text='Заголовок тестового поста - более 15 символов',
            author=cls.author,
            group=cls.group)

    def test_post_group___str__(self):
        """
        Приложение posts test_models проверка __str__ post и group.
        """
        group = PostGroupModelTest.group
        post = PostGroupModelTest.post
        post_group_data = (
            (post, post.text[:15]),
            (group, group.title))
        for name, expected_field in post_group_data:
            with self.subTest(name=name):
                self.assertEqual(str(name), expected_field)
