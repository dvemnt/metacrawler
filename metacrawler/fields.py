# coding=utf-8


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

    def search(self, page):
        """Search value on page.

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
