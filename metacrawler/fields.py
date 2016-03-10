# coding=utf-8

import inspect


class Field(object):

    """Field is minimum structure unit. Contains certain value."""

    def __init__(self, value=None, xpath=None,
                 function=None, postprocessing=None, to=str):
        """Override initialization instance.

        :param value (optional): value of field.
        :param xpath (optional): `str` xpath for extracting value from page.
        :param function (optional): `function` function for getting value.
        :param postprocessing (optional): `function` postprocessing function.
        :param to (optional): `type` to representation as.
        """
        self.__value = value
        self.__xpath = xpath
        self.__function = function
        self.__postprocessing = postprocessing
        self.__to = to

    @property
    def value(self):
        """The value property."""
        return self.__value

    @value.setter
    def value(self, value):
        """The value setter."""
        self.__value = self.__to(value)

    def parse(self, page):
        """Parse value from page.

        :param page: `lxml.Element` instance.
        """
        if self.__value is not None:
            return
        elif self.__xpath is not None:
            value = page.xpath(self.__xpath)
        elif self.__function is not None:
            value = self.__function(page)
        else:
            raise AttributeError(
                'Cannot call `.search()` as no `value=`, `xpath=` or '
                '`function=` keywords argument was passed when instantiating '
                'the field instance.'
            )

        if self.__to in (list, tuple):
            self.value = value
        else:
            try:
                self.value = value[0]
            except IndexError:
                self.__value = None

        if self.__value is not None and self.__postprocessing is not None:
            self.value = self.__postprocessing(self.value)


class Item(object):

    """Item is aggregate of fields. Items can be nested."""

    @classmethod
    def get_fields(cls):
        """Return all fields.

        :returns: `generator` fields generator.
        """
        for key, value in cls.__dict__.items():
            if issubclass(value.__class__, Field):
                yield {'name': key, 'field': value}

    @classmethod
    def get_items(cls):
        """Return all items.

        :returns: `generator` items generator.
        """
        for key, value in cls.__dict__.items():
            if inspect.isclass(value) and issubclass(value, Item):
                yield {'name': key, 'item': value}

    @classmethod
    def parse(cls, page):
        """Parse process.

        :param page: `lxml.Element` instance.
        """
        for field in cls.get_fields():
            field['field'].parse(page)

        for item in cls.get_items():
            item['item'].parse(page)

    @classmethod
    def as_dict(cls):
        """Convert class to dict.

        :returns: `dict` dict representation.
        """
        value = {}

        for field in cls.get_fields():
            value[field['name']] = field['field'].value

        for item in cls.get_items():
            value[item['name']] = item['item'].as_dict()

        return value
