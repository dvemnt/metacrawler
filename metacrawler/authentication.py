# coding=utf-8

import requests
from lxml import html


class Authentication(object):

    """Authentication model."""

    def __init__(self, url=None, xpath=None, **data):
        """Override initialization instance.

        :param xpath (optional): `str` XPath string for find form.
        :param **data (optional): key-value form data.
        """
        self.url = url
        self.xpath = xpath
        self.data = data

    def get_form(self, page):
        """Get form element from page.

        :param page: `lxml.Element` instance.
        :returns: `lxml.Element` form.
        """
        assert self.xpath, (
            'Cannot call `.get_form()` as no `xpath`'
            '`function=` keywords argument was passed when instantiating '
            'the field instance.'
        )

        return page.xpath(self.xpath)

    def get_login_url(self, form):
        """Get login url in form.

        :param form: `lxml.Element` instance.
        :returns: `str` login URL.
        """
        return form.xpath('@action')[0]

    def get_form_data(self, form):
        """Get data for submit form.

        :param form: `lxml.Element` instance.
        :returns: `dict` form submit data.
        """
        data = {}

        for field in form.xpath('.//input'):
            try:
                data[field.xpath('@name')[0]] = field.xpath('@value')[0]
            except IndexError:
                continue

        data.update(self.data)

        return data

    def authentication(self, page=None, session=None):
        """Authentication.

        :param page: `lxml.Element` authentication page.
        :param session (optional): `requests.Session` instance.
        :returns: `requests.Session` instance.
        """
        session = session or requests.Session()

        if not page and self.url:
            page = html.fromstring(session.get(self.url).content)
        elif not (page or self.url):
            raise ValueError(
                'For call `authentication` method '
                'need pass page as first argument or pass `url` '
                'keyword argument in initialization call.'
            )

        form = self.get_form(page)
        data = self.get_form_data(form)
        url = self.get_login_url(form)

        session.post(url, data=data)

        return session
