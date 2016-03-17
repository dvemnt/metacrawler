# coding=utf-8

import unittest
import os
import sys

from lxml import html
from httmock import urlmatch, HTTMock

from metacrawler.handlers import Handler
from metacrawler.fields import Field
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

    def test_crawl_value__error(self):
        """Test error crawl value."""
        field = Field()

        with self.assertRaises(AttributeError):
            field.crawl(self.page)

    def test_crawl_value__not_found(self):
        """Test error crawl value."""
        field = Field(xpath='//a/@id')
        value = field.crawl(self.page)

        self.assertEqual(value, None)

    def test_crawl_value__by_xpath(self):
        """Test crawl value by xpath."""
        field = Field(xpath='//a/@href')
        value = field.crawl(self.page)

        self.assertEqual(value, 'test')

    def test_crawl_value__with_postprocessing(self):
        """Test crawl value with postprocessing."""
        field = Field(xpath='//a/@href', postprocessing=lambda x: x[:2])
        value = field.crawl(self.page)

        self.assertEqual(value, 'te')

    def test_crawl_value__with_to_list(self):
        """Test crawl value by xpath."""
        field = Field(xpath='//a/@href', to=list)
        value = field.crawl(self.page)

        self.assertEqual(value, ['test'])

    def test_crawl_value__with_to_list_with_not_string(self):
        """Test crawl value by xpath."""
        field = Field(xpath='//a', to=list)

        with self.assertRaises(ValueError):
            field.crawl(self.page)

    def test_nested_fields_error(self):
        """Test nested fields list."""
        field = Field(xpath='text()')
        nested_field = Field(xpath='//a', fields={'text': field})

        with self.assertRaises(ValueError):
            nested_field.crawl(self.page)

    def test_nested_fields_list(self):
        """Test nested fields list."""
        field = Field(xpath='text()')
        nested_field = Field(xpath='//a', to=list, fields={'text': field})

        value = nested_field.crawl(self.page)

        self.assertEqual(value, [{'text': 'Link'}])

    def test_nested_fields_list_error(self):
        """Test nested fields list."""
        field = Field(xpath='text()')
        nested_field = Field(to=list, fields={'text': field})

        with self.assertRaises(AttributeError):
            nested_field.crawl(self.page)

    def test_nested_fields_dict(self):
        """Test nested fields list."""
        field = Field(xpath='//a/text()')
        nested_field = Field(to=dict, fields={'text': field})

        value = nested_field.crawl(self.page)

        self.assertEqual(value, {'text': 'Link'})

    def test_nested_fields_dict_error(self):
        """Test nested fields list (error)."""
        field = Field(xpath='//a/@test')
        nested_field = Field(xpath='//test', to=dict, fields={'text': field})

        value = nested_field.crawl(self.page)

        self.assertEqual(value, {'text': None})


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

    def test_crawler__with_fields(self):
        """Test crawler (with fields)."""
        fields = {
            'text': Field(xpath='//a/text()'),
            'href': Field(xpath='//a/@href'),
        }
        crawler = Crawler('http://test.com', fields=fields)

        with HTTMock(server):
            data = crawler.crawl()

        self.assertEqual(data, {'text': 'A', 'href': 'href'})

    def test_crawler__with_class_fields(self):
        """Test crawler (with class items)."""
        field = Field(xpath='//a/text()')
        crawler = type(
            'TestCrawler', (Crawler,), {'field': field}
        )('http://test.com')

        with HTTMock(server):
            data = crawler.crawl()

        self.assertEqual(data, {'field': 'A'})

    def test_crawler__with_class_crawlers(self):
        """Test crawler (with class crawlers)."""
        fields = {
            'text': Field(xpath='//a/text()'),
            'href': Field(xpath='//a/@href'),
        }
        crawler = Crawler('http://test.com', fields=fields)
        nested_crawler = type(
            'TestCrawler', (Crawler,), {'crawler': crawler}
        )('http://test.com')

        with HTTMock(server):
            data = nested_crawler.crawl()

        self.assertEqual(data, {'crawler': {'text': 'A', 'href': 'href'}})

    def test_crawler__nested(self):
        """Test crawler (nested)."""
        fields = {
            'text': Field(xpath='//a/text()'),
            'href': Field(xpath='//a/@href'),
        }
        crawler = Crawler('http://test.com', fields=fields)
        crawlers = {'friends': crawler}
        nested_crawler = Crawler('http://test.com', fields=crawlers)

        with HTTMock(server):
            data = nested_crawler.crawl()

        self.assertEqual(data, {'friends': {'text': 'A', 'href': 'href'}})

    def test_crawler_collapse__error(self):
        """Test crawler collapse (error)."""
        fields = {
            'text': Field(xpath='//a/text()'),
            'href': Field(xpath='//a/@href'),
        }

        with self.assertRaises(ValueError):
            Crawler('http://test.com', fields=fields, collapse=True)

    def test_crawler_collapse(self):
        """Test crawler collapse."""
        fields = {'text': Field(xpath='//a/text()')}
        crawler = Crawler('http://test.com', fields=fields, collapse=True)

        with HTTMock(server):
            data = crawler.crawl()

        self.assertEqual(data, 'A')

    def test_crawler_collapse__list(self):
        """Test crawler collapse (list)."""
        fields = {'text': Field(xpath='//a/text()', to=list)}
        crawler = Crawler('http://test.com', fields=fields, collapse=True)

        with HTTMock(server):
            data = crawler.crawl()

        self.assertEqual(data, 'A')

    def test_crawler_pagination(self):
        """Test crawler pagination."""
        pagination = Pagination(xpath='//a/@test', host='http://test.com')
        fields = {'text': Field(xpath='//a/text()')}
        crawler = Crawler(
            'http://test.com', fields=fields, pagination=pagination
        )

        with HTTMock(server):
            data = crawler.crawl()

        self.assertEqual(data, [{'text': 'A'}])

    def test_crawler_pagination_with_collapse(self):
        """Test crawler pagination."""
        pagination = Pagination(xpath='//a/@test', host='http://test.com')
        fields = {'text': Field(xpath='//a/text()')}
        crawler = Crawler(
            'http://test.com', fields=fields, pagination=pagination,
            collapse=True
        )

        with HTTMock(server):
            data = crawler.crawl()

        self.assertEqual(data, ['A'])


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
        configspec = {'test': 'string(default="proxies.txt")'}
        settings_class = type(
            'TestSettings', (Settings,), {'configspec': configspec}
        )
        settings_class.create_configuration_file(path)

        self.assertTrue(os.path.exists(path))
        settings = settings_class.load_from_file(path)
        self.assertEqual(settings.test, 'string(default="proxies.txt")')

    def test_from_file__error(self):
        """Testing from file (error)."""
        path = 'test.conf'
        settings_class = type(
            'TestSettings', (Settings,), {'configspec': self.configspec}
        )
        settings_class.create_configuration_file(path)

        with self.assertRaises(ValueError):
            settings_class.load_from_file(path)

    def test_get_nested_settings(self):
        """Test get nested settings."""
        settings = Settings(configuration=self.configspec)

        self.assertEqual(
            settings.proxy.enabled, self.configspec['proxy']['enabled']
        )


class HandlerTest(unittest.TestCase):

    """Test `metacrawler.Handler` class."""

    def test_cli(self):
        """Test CLI."""
        handler = Handler()
        handler.argparser.add_argument('test')
        sys.argv = ['run.py', 'test']

        self.assertEqual(handler.cli['output'], 'output.json')

    def test_output(self):
        """Test output."""
        sys.argv = ['run.py', 'test']
        fields = {
            'text': Field(xpath='//a/text()'),
            'href': Field(xpath='//a/@href'),
        }
        crawler = Crawler('http://test.com', fields=fields)
        handler = Handler({'page': crawler})
        handler.argparser.add_argument('test')

        with HTTMock(server):
            handler.start()
            handler.output()

        self.assertTrue(os.path.exists('output.json'))
        os.remove('output.json')

    def test_output__compact(self):
        """Test output (compact)."""
        sys.argv = ['run.py', 'test']
        fields = {
            'text': Field(xpath='//a/text()'),
            'href': Field(xpath='//a/@href'),
        }
        crawler = Crawler('http://test.com', fields=fields)
        handler = Handler({'page': crawler})
        handler.argparser.add_argument('test')

        with HTTMock(server):
            handler.start()
            handler.output(compact=True)

        self.assertTrue(os.path.exists('output.json'))
        os.remove('output.json')

    def test_handler(self):
        """Test handler."""
        fields = {
            'text': Field(xpath='//a/text()'),
            'href': Field(xpath='//a/@href'),
        }
        crawler = Crawler('http://test.com', fields=fields)
        handler = Handler({'page': crawler})

        with HTTMock(server):
            data = handler.start()

        self.assertEqual(data, {'page': {'text': 'A', 'href': 'href'}})

    def test_handler__with_class_crawlers(self):
        """Test handler (with class crawlers)."""
        fields = {
            'text': Field(xpath='//a/text()'),
            'href': Field(xpath='//a/@href'),
        }
        crawler = Crawler('http://test.com', fields=fields)
        handler = type('TestHandler', (Handler,), {'crawler': crawler})()

        with HTTMock(server):
            data = handler.start()

        self.assertEqual(data, {'crawler': {'text': 'A', 'href': 'href'}})
