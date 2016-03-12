# coding=utf-8

from metacrawler.items import Item

import fields


page = Item(fields={'name': fields.name, 'projects': fields.projects})
