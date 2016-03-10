# coding=utf-8

import unittest

from lxml import html

from metacrawler import fields


class FieldTest(unittest.TestCase):

    """Test `metacrawler.fields.Field` class."""

    page = html.fromstring('<html><body><a href="test">Link</a></body></html>')

    def test_initialization(self):
        """Test initialization."""
        field = fields.Field()

        self.assertIsInstance(field, fields.Field)

    def test_search_value__error(self):
        """Test error search value."""
        field = fields.Field()

        with self.assertRaises(AttributeError):
            field.search(self.page)

    def test_search_value__not_found(self):
        """Test error search value."""
        field = fields.Field(xpath='//a/@id')
        field.search(self.page)

        self.assertEqual(field.value, None)

    def test_search_value__with_value(self):
        """Test search value by xpath."""
        field = fields.Field(value='Test')
        field.search(self.page)

        self.assertEqual(field.value, 'Test')

    def test_search_value__by_xpath(self):
        """Test search value by xpath."""
        field = fields.Field(xpath='//a/@href')
        field.search(self.page)

        self.assertEqual(field.value, 'test')

    def test_search_value__by_function(self):
        """Test search value by function."""
        field = fields.Field(function=lambda x: x.xpath('//a/@href'))
        field.search(self.page)

        self.assertEqual(field.value, 'test')

    def test_search_value__with_postprocessing(self):
        """Test search value with postprocessing."""
        field = fields.Field(xpath='//a/@href', postprocessing=lambda x: x[:2])
        field.search(self.page)

        self.assertEqual(field.value, 'te')

    def test_search_value__with_to_list(self):
        """Test search value by xpath."""
        field = fields.Field(xpath='//a/@href', to=list)
        field.search(self.page)

        self.assertEqual(field.value, ['test'])
