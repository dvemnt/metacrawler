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

    def test_parse_value__error(self):
        """Test error parse value."""
        field = fields.Field()

        with self.assertRaises(AttributeError):
            field.parse(self.page)

    def test_parse_value__not_found(self):
        """Test error parse value."""
        field = fields.Field(xpath='//a/@id')
        field.parse(self.page)

        self.assertEqual(field.value, None)

    def test_parse_value__with_value(self):
        """Test parse value by xpath."""
        field = fields.Field(value='Test')
        field.parse(self.page)

        self.assertEqual(field.value, 'Test')

    def test_parse_value__by_xpath(self):
        """Test parse value by xpath."""
        field = fields.Field(xpath='//a/@href')
        field.parse(self.page)

        self.assertEqual(field.value, 'test')

    def test_parse_value__by_function(self):
        """Test parse value by function."""
        field = fields.Field(function=lambda x: x.xpath('//a/@href'))
        field.parse(self.page)

        self.assertEqual(field.value, 'test')

    def test_parse_value__with_postprocessing(self):
        """Test parse value with postprocessing."""
        field = fields.Field(xpath='//a/@href', postprocessing=lambda x: x[:2])
        field.parse(self.page)

        self.assertEqual(field.value, 'te')

    def test_parse_value__with_to_list(self):
        """Test parse value by xpath."""
        field = fields.Field(xpath='//a/@href', to=list)
        field.parse(self.page)

        self.assertEqual(field.value, ['test'])


class ItemTest(unittest.TestCase):

    """Test `metacrawler.fields.Item` class."""

    page = html.fromstring('<html><body><a href="test">Link</a></body></html>')

    class LinkItem(fields.Item):

        """Link item."""

        name = fields.Field(xpath='//a/text()')
        link = fields.Field(xpath='//a/@href')

    def get_composite_item(self):
        class LinksItem(fields.Item):

            """Links item."""

            links = ItemTest.LinkItem
        return LinksItem

    def test_get_fields__no_fields(self):
        """Test get fields (no fields)."""
        self.assertFalse(list(self.get_composite_item().get_fields()))

    def test_get_items__no_items(self):
        """Test get items (no items)."""
        self.assertFalse(list(self.LinkItem.get_items()))

    def test_get_fields(self):
        """Test get fields."""
        self.assertEqual(len(list(self.LinkItem.get_fields())), 2)

    def test_get_items(self):
        """Test get items."""
        self.assertEqual(len(list(self.get_composite_item().get_items())), 1)

    def test_parse__item_with_items(self):
        """Test parse (item with items)."""
        self.get_composite_item().parse(self.page)

        self.assertEqual(self.get_composite_item().links.name.value, 'Link')
        self.assertEqual(self.get_composite_item().links.link.value, 'test')

    def test_parse(self):
        """Test parse."""
        self.LinkItem.parse(self.page)

        self.assertEqual(self.LinkItem.name.value, 'Link')
        self.assertEqual(self.LinkItem.link.value, 'test')

    def test_as_dict__item_with_items(self):
        """Test as dict (item with items)."""
        self.get_composite_item().parse(self.page)
        d = self.get_composite_item().as_dict()

        self.assertEqual(d, {'links': {'name': 'Link', 'link': 'test'}})

    def test_as_dict(self):
        """Test as dict."""
        self.LinkItem.parse(self.page)
        d = self.LinkItem.as_dict()

        self.assertEqual(d, {'name': 'Link', 'link': 'test'})
