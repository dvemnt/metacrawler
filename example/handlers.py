# coding=utf-8

from metacrawler import Handler

import crawlers


class PyvimHandler(Handler):

    """Custom handler."""

    def before(self):
        """Actions before start crawling."""
        # Change referer from settings.
        self.session.headers.update({'Referer': self.settings.referer})

handler = PyvimHandler(crawlers={'pyvim': crawlers.pyvim})
handler.settings.load_from_file('example.config')
