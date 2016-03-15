# coding=utf-8

import unittest
import os
import json

from lxml import html
from httmock import urlmatch, HTTMock

from metacrawler import Handler
from metacrawler.items import Field, Item
from metacrawler.crawlers import Crawler
from metacrawler.pagination import Pagination
from metacrawler.settings import Settings

@urlmatch(netloc=r'(.*\.)?test\.com$')
def server(*args, **kwargs):
    """Simple webserver."""
    return '<html><body><a id="id" href="href">A</a></body></html>'


class FieldTest(unittest.TestCase):

    """Test `metacrawler.Field` class."""

    page = html.fromstring('<html><body><a href="test">Link</a></body></html>')

    def test_parse_value__error(self):
        """Test error parse value."""
        field = Field()

        with self.assertRaises(AttributeError):
            field.parse(self.page)

    def test_parse_value__not_found(self):
        """Test error parse value."""
        field = Field(xpath='//a/@id')
        value = field.parse(self.page)

        self.assertEqual(value, None)

    def test_parse_value__by_xpath(self):
        """Test parse value by xpath."""
        field = Field(xpath='//a/@href')
        value = field.parse(self.page)

        self.assertEqual(value, 'test')

    def test_parse_value__by_function(self):
        """Test parse value by function."""
        field = Field(function=lambda x: x.xpath('//a/@href'))
        value = field.parse(self.page)

        self.assertEqual(value, 'test')

    def test_parse_value__with_postprocessing(self):
        """Test parse value with postprocessing."""
        field = Field(xpath='//a/@href', postprocessing=lambda x: x[:2])
        value = field.parse(self.page)

        self.assertEqual(value, 'te')

    def test_parse_value__with_to_list(self):
        """Test parse value by xpath."""
        field = Field(xpath='//a/@href', to=list)
        value = field.parse(self.page)

        self.assertEqual(value, ['test'])

    def test_parse_value__with_to_list_with_not_string(self):
        """Test parse value by xpath."""
        field = Field(xpath='//a', to=list)

        with self.assertRaises(ValueError):
            field.parse(self.page)


class ItemTest(unittest.TestCase):

    """Test `metacrawler.Item` class."""

    page = html.fromstring('<html><body><a href="test">Link</a></body></html>')

    def setUp(self):
        """Setup test."""
        self.fields = {
            'text': Field(xpath='//a/text()'),
            'href': Field(xpath='//a/@href'),
        }
        self.item = Item(xpath='//a', fields=self.fields)
        self.nested_item = Item(xpath='//body', fields={'links': self.item})

    def test_parse__with_class_fields(self):
        """Test parse with class fields."""
        item = type(
            'TestItem', (Item,),
            {'field': self.fields['text'], 'item': self.item}
        )()
        data = item.parse(self.page)

        self.assertEqual(data[0]['field'], 'Link')
        self.assertEqual(data[0]['item'][0]['text'], 'Link')
        self.assertEqual(data[0]['item'][0]['href'], 'test')

    def test_parse__item_with_items(self):
        """Test parse (item with items)."""
        data = self.nested_item.parse(self.page)

        self.assertEqual(data[0]['links'][0]['text'], 'Link')
        self.assertEqual(data[0]['links'][0]['href'], 'test')

    def test_parse(self):
        """Test parse."""
        data = self.item.parse(self.page)

        self.assertEqual(data[0]['text'], 'Link')
        self.assertEqual(data[0]['href'], 'test')

    def test_convert_data_to_json(self):
        """Test convert data to json."""
        data = self.item.parse(self.page)

        json.dumps(data)


class PaginationTest(unittest.TestCase):

    """Pagination test."""

    page = html.fromstring('<html><body><a href="/test">A</a></body></html>')

    def test_error_initialization(self):
        """Test error initialization."""
        pagination = Pagination()

        with self.assertRaises(AttributeError):
            pagination.next()

    def test_pagination__by_xpath__error(self):
        """Test pagination by xpath (error)."""
        pagination = Pagination(xpath='//a/@id', host='http://host')

        url = pagination.next(self.page)

        self.assertEqual(url, None)

    def test_pagination__by_xpath(self):
        """Test pagination by xpath."""
        pagination = Pagination(xpath='//a/@href', host='http://host')

        url = pagination.next(self.page)

        self.assertEqual(url, 'http://host/test')

    def test_pagination__by_function_list(self):
        """Test pagination by list function."""
        def paginate(*args, **kwargs):
            """Simple pagination iterable function."""
            return ['http://host/test']

        pagination = Pagination(function=paginate)

        for url in pagination:
            self.assertEqual(url, 'http://host/test')

    def test_pagination__by_not_iterable_function(self):
        """Test pagination by not iterable function."""
        def paginate(*args, **kwargs):
            """Simple pagination iterable function."""
            return 0

        pagination = Pagination(function=paginate)

        for url in pagination:
            self.assertEqual(url, 0)

    def test_pagination__by_function(self):
        """Test pagination by function."""
        def paginate(page=None):
            """Simple pagination iterable function."""
            return 'http://host' + page.xpath('//a/@href')[0]

        pagination = Pagination(function=paginate)

        url = pagination.next(self.page)

        self.assertEqual(url, 'http://host/test')

    def test_pagination__by_iterable_function(self):
        """Test pagination by iterable function."""
        def paginate(*args, **kwargs):
            """Simple pagination iterable function."""
            url = 'http://host/test'
            for i in range(5):
                yield url + '?page={}'.format(i)

        pagination = Pagination(function=paginate)

        for i, url in enumerate(pagination):
            self.assertEqual(url, 'http://host/test?page={}'.format(i))


class CrawlerTest(unittest.TestCase):

    """Test `metacrawler.crawlers.Crawler` class."""

    def test_crawler__with_items(self):
        """Test crawler (with items)."""
        fields = {
            'text': Field(xpath='text()'),
            'href': Field(xpath='@href'),
        }
        items = {'links': Item(xpath='//a', fields=fields)}
        crawler = Crawler('http://test.com', items=items)

        with HTTMock(server):
            data = crawler.crawl()

        self.assertEqual(data, {'links': [{'text': 'A', 'href': 'href'}]})

    def test_crawler__nested(self):
        """Test crawler (nested)."""
        fields = {
            'text': Field(xpath='text()'),
            'href': Field(xpath='@href'),
        }
        items = {'links': Item(xpath='//a', fields=fields)}
        crawler = Crawler('http://test.com', items=items)
        crawlers = {'friends': crawler}
        nested_crawler = Crawler(
            'http://test.com', items=items, crawlers=crawlers
        )

        with HTTMock(server):
            data = nested_crawler.crawl()

        self.assertEqual(
            data,
            {
                'friends': {'links': [{'text': 'A', 'href': 'href'}]},
                'links': [{'text': 'A', 'href': 'href'}]
            }
        )


class SettingsTests(unittest.TestCase):

    """Test `metacrawler.settings.Settings` class."""

    configspec = {
        'proxy': {
            'enabled': 'boolean(default=True)',
            'file': 'string(default="proxies.txt")',
        }
    }

    path = 'test.conf'

    def tearDown(self):
        """Clear after test."""
        try:
            os.remove(self.path)
        except OSError:
            pass

    def test_create_configuration_file(self):
        """Testing create configuration file."""
        path = 'test.conf'
        settings = Settings(configspec=self.configspec)
        settings.create_configuration_file(path)

        self.assertTrue(os.path.exists(path))
        settings.load_from_file(path)
        self.assertEqual(settings.proxy.file, 'string(default="proxies.txt")')

    def test_create_settings_from_dict(self):
        """Testing create settings from dict."""
        settings = Settings()
        settings.load_from_dict(self.configspec)
        self.assertEqual(settings.proxy.file, 'string(default="proxies.txt")')


class HandlerTest(unittest.TestCase):

    """Test `metacrawler.Handler` class."""

    def test_handler(self):
        """Test handler (with items)."""
        fields = {
            'text': Field(xpath='text()'),
            'href': Field(xpath='@href'),
        }
        items = {'links': Item(xpath='//a', fields=fields)}
        crawler = Crawler('http://test.com', items=items)
        handler = Handler({'page': crawler})

        with HTTMock(server):
            data = handler.start()

        self.assertEqual(
            data, {'page': {'links': [{'text': 'A', 'href': 'href'}]}}
        )
