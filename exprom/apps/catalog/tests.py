from unittest import TestCase

from apps.catalog.utils.slug import slugify


class CatalogTestCase(TestCase):
    def test_slugify(self):
        text = 'hello world'
        text2 = 'привет мир'
        result = slugify(text)
        result2 = slugify(text2)

        self.assert_(result, 'hello-world')
        self.assert_(result2, 'privet-mir')