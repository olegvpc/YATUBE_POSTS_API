from django.test import TestCase
from django.urls import reverse


class StaticViewsTests(TestCase):

    def test_about_page_uses_correct_template(self):
        """
        Приложение about test_views шаблоны /author.html, /tech.html верные.
        """
        templates_pages_names = (
            ('about/author.html', 'about:author'),
            ('about/tech.html', 'about:tech')
        )
        for template, name in templates_pages_names:
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertTemplateUsed(response, template)
