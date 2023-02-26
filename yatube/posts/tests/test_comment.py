from django.test import Client, TestCase
from django.urls import reverse

from ..models import Comment, Post, User


class PostsCommentTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='test_user')
        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.user)
        cls.form_comment = {
            'text': 'Тестовый коммент'}

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PostsCommentTests.post.author)

    def test_authorized_user_comments(self):
        """
        Приложение posts test_comment проверка комментировать
        авторизованным пользователем.
        """
        username = PostsCommentTests.post.author.username
        post_id = PostsCommentTests.post.id
        # Считаем комменты до объявления
        count_before = Comment.objects.count()
        response = self.authorized_client.post(reverse(
            'add_comment', args=(username, post_id)),
            data=PostsCommentTests.form_comment, follow=True)
        self.assertRedirects(
            response, reverse('post', args=(username, post_id)))
        self.assertEqual(Comment.objects.count(), count_before + 1)
        last_comment = Comment.objects.last()
        compare_data = (
            (last_comment.text, PostsCommentTests.form_comment['text']),
            (last_comment.author, PostsCommentTests.post.author),
            (last_comment.post, PostsCommentTests.post))
        for comm_attr, expected in compare_data:
            with self.subTest(comm_attr=comm_attr):
                self.assertEqual(comm_attr, expected)

    def test_guest_user_comments(self):
        """
        Приложение posts test_comment проверка комментировать гостем.
        """
        username = PostsCommentTests.post.author.username
        post_id = PostsCommentTests.post.id
        count_before = Comment.objects.count()
        response = self.client.post(reverse(
            'add_comment', args=(username, post_id)),
            data=PostsCommentTests.form_comment, follow=True)
        self.assertEqual(Comment.objects.count(), count_before)
        self.assertRedirects(
            response, reverse('login') + '?next=' + reverse(
                'add_comment', args=(username, post_id)))
