# coding=utf-8

from metacrawler.crawlers import Crawler

import items

pyvim = Crawler(url='https://pyvim.com', items={'page': items.page})
