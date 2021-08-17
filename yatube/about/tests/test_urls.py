from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class StaticURLTests(TestCase):

    def test_about(self):
        """
        Приложение about test_urls Запросы страницы author и tech.
        """
        url_names = (
            '/about/author/',
            '/about/tech/',
        )
        for address in url_names:
            with self.subTest(address=address):
                response = self.client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_about_check_reverse_and_right_address(self):
        """
        Приложение about test_urls соответствие address - reverse(name).
        """
        url_names = (
            ('/about/author/', 'about:author'),
            ('/about/tech/', 'about:tech'),
        )
        for address, name in url_names:
            with self.subTest(address=address):
                self.assertEqual(address, reverse(name))
