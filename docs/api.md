## metacrawler.handlers.Handler(crawlers=None, settings=None) ##

### Initialization arguments ###
- `crawlers` *(optional)*:  `dict`.
Crawler instances. Format: `{'crawler_name': crawler_instance}`
- `settings` *(optional)*: `metacrawler.settings.Settings` instance.
Project settings. If not passed, used empty instance.


### Initialization class attributes ###
- `settings` *(optional)*: `metacrawler.settings.Settings` instance.
Project settings. If not passed, used empty instance.
- any crawler instance *(optional)*: `metacrawler.crawlers.Crawler` instance.


### Public attributes ###
- `session`: `requests.Session` instance.
Using for make requests.
- `argparser`: `argparse.ArgumentParser` instance.
Using for parse CLI.
- `data`: `dict`.
Contains data after crawling.
- `cli`: `property`.
Contains CLI arguments.


### Public methods ###
- `before(self)`
Call before start crawling. May use for *any* actions (dynamic set values and other).
- `start(self)`
Start crawling.
- `output(self, compact=False, data=None)`:
Write JSON result in file.
  - `compact`: `bool`:
  Use indent in output JSON.
  - `data`:
  JSON serializable data.
- `get_ATTRIBUTE_NAME(self)`:
Set attribute `ATTRIBUTE_NAME` (any attribute name) by returned value at initialization.



## metacrawler.crawlers.Crawler(self, url=None, fields=None, collapse=False, session=None, pagination=None, limit=None, timeout=3.0) ##

### Initialization arguments ###
- `url` *(optional)*:  `str`.
URL of page for crawling.
- `fields` *(optional)*:  `dict`.
Fields or nested crawlers. Format: `{'field_name': crawler_instance or field_instance}`.
- `collapse` *(optional)*:  `bool`.
Collapse crawler key in result data. For example, `{'crawler': {'field': []}}` to `{'cralwer': []}`. Work only with single field. If fields will be more raise `ValueError` exception.
- `session` *(optional)*: `requests.Session` instance.
Using for make requests.
- `pagination` *(optional)*: `metacrawler.pagination.Pagination` instance.
Using for navigate on website pages.
- `limit` *(optional)*: `int`.
Limit of results. Count of result may be more than limit due pagination.
- `timeout` *(optional)*: `float`.
Timeout before current connection will be closed.


### Initialization class attributes ###
- `url` *(optional)*:  `str`.
URL of page for crawling.
- `collapse` *(optional)*:  `bool`.
Collapse crawler key in result data. For example, `{'crawler': {'field': []}}` to `{'cralwer': []}`. Work only with single field. If fields will be more raise `ValueError` exception.
- `session` *(optional)*: `requests.Session` instance.
Using for make requests.
- `pagination` *(optional)*: `metacrawler.pagination.Pagination` instance.
Using for navigate on website pages.
- `limit` *(optional)*: `int`.
Limit of results. Count of result may be more than limit due pagination.
- `timeout` *(optional)*: `float`.
Timeout before current connection will be closed.
- any crawler or field instance *(optional)*: `metacrawler.crawlers.Crawler` or `metacrawler.fields.Field` instance.


### Public attributes ###
- `url` *(optional)*:  `str`.
URL of page for crawling.
- `collapse` *(optional)*:  `bool`.
Collapse crawler key in result data. For example, `{'crawler': {'field': []}}` to `{'cralwer': []}`. Work only with single field. If fields will be more raise `ValueError` exception.
- `session` *(optional)*: `requests.Session` instance.
Using for make requests.
- `pagination` *(optional)*: `metacrawler.pagination.Pagination` instance.
Using for navigate on website pages.
- `limit` *(optional)*: `int`.
Limit of results. Count of result may be more than limit due pagination.
- `timeout` *(optional)*: `float`.
Timeout before current connection will be closed.
- `data`: `dict` or `list`.
Contains data after crawling.


### Public methods ###
- `before(self)`
Call before start crawling. May use for *any* actions (dynamic set values and other).
- `crawl(self, *args, **kwargs)`
Start crawling.
- `paginate(self, page)`:
Return next url for crawling if has `pagination` attribute.
  - `page`: `lxml.Element`
  `lxml` reperesentation of website page.
- `get_ATTRIBUTE_NAME(self)`:
Set attribute `ATTRIBUTE_NAME` (any attribute name) by returned value at initialization.


## metacralwer.fields.Field(self, value=None, xpath=None, fields=None, postprocessing=None, to=str) ##

### Initialization arguments ###
- `value` *(optional)*:
Any value. Using as cap.
- `xpath` *(optional)*: `str`.
XPath for extact value.
- `fields` *(optional)*:  `dict`.
Nested fields. Format: `{'field_name': field_instance}`.
- `postprocessing` *(optional)*:  any callable object.
Using for clean or/and validate raw data. Must accept single argument and return value.
- `to` *(optional)*: `type`.
Value representation. May be on of `(list, dict, int, float, str)`.
  - `list`: values in `list` should not be a `lxml.Element`.
  - `dict`: using with nested fields.
  - `int`, `float`, `str`: first found value.


### Initialization class attributes ###
- `value` *(optional)*:
Any value. Using as cap.
- `xpath` *(optional)*: `str`.
XPath for extact value.
- `fields` *(optional)*:  `dict`.
Nested fields. Format: `{'field_name': field_instance}`.
- `postprocessing` *(optional)*:  any callable object.
Using for clean or/and validate raw data. Must accept single argument and return value.
- `to` *(optional)*: `type`.
Value representation. May be on of `(list, dict, int, float, str)`.
  - `list`: values in `list` should not be a `lxml.Element`.
  - `dict`: using with nested fields.
  - `int`, `float`, `str`: first found value.
- any field instance *(optional)*: `metacrawler.fields.Field` instance.


### Public attributes ###
- `value` *(optional)*:
Any value. Using as cap.
- `xpath` *(optional)*: `str`.
XPath for extact value.
- `fields` *(optional)*:  `dict`.
Nested fields. Format: `{'field_name': field_instance}`.
- `postprocessing` *(optional)*:  any callable object.
Using for clean or/and validate raw data. Must accept single argument and return value.
- `to` *(optional)*: `type`.
Value representation. May be on of `(list, dict, int, float, str)`.
  - `list`: values in `list` should not be a `lxml.Element`.
  - `dict`: using with nested fields.
  - `int`, `float`, `str`: first found value.


### Public methods ###
- `before(self)`
Call before start crawling. May use for *any* actions (dynamic set values and other).
- `crawl(self, page)`
Start crawling.
  - `page`: `lxml.Element`
  `lxml` reperesentation of website page.
- `get_ATTRIBUTE_NAME(self)`:
Set attribute `ATTRIBUTE_NAME` (any attribute name) by returned value at initialization.


## metacrawler.pagination.Pagination(self, xpath=None, host=None, urls=None) ##

### Initialization arguments ###
- `xpath` *(optional)*: `str`.
XPath for extact value.
- `host` *(optional)*: `str`.
Website host. Using for concatenation with extracted value by XPath.
- `urls` *(optional)*:  `list`.
List of urls for paginate.


### Public attributes ###
- `xpath` *(optional)*: `str`.
XPath for extact value.
- `host` *(optional)*: `str`.
Website host. Using for concatenation with extracted value by XPath.
- `urls` *(optional)*:  `list`.
List of urls for paginate.
- `index` *(optional)*: `int`.
Current position in `urls` list.


### Public methods ###
- `next(self, page=None)`
Return next url.
  - `page`: `lxml.Element`
  `lxml` reperesentation of website page.

### Other ###
May using in iteration context if `urls` passed.


## metacrawler.settings.Settings(self, configspec=None, configuration=None) ##

### Initialization arguments ###
- `configspec` *(optional)*: `dict`.
Validation specification. See http://www.voidspace.org.uk/python/configobj.html#configspec.
- `configuration` *(optional)*: `dict`.
Concrete configuration.


### Public attributes ###
For `configuration` using dynamic access by dot.
For `{'name': 'value'}` configuration you can get value by `settings_instance.name`. Support any depth.


### Class methods ###
- `load_from_file(cls, filename)`
Return settings instance loaded from file.
  - `filename`: `str`
  Name of file for load.
- `create_configuration_file(cls, filename)`
Create configuration file with `configspec` as template.
  - `filename`: `str`
  Name of file for write.
