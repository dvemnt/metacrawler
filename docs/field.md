next_url:   crawler.html
next_title: Crawler
prev_title: API
prev_url:   api.html

## Usage ##

```python
import requests
from lxml import html

from metacrawler.fields import Field


response = requests.get('https://github.com/pyvim/metacrawler')
page = html.fromstring(response.text)
field = Field(xpath='//span[@itemprop="about"]/text()')
content = field.crawl(page)
print(content)

# Output:
#
# A lightweight Python crawling framework.
```


## metacralwer.fields.Field(self, value=None, xpath=None, fields=None, to=str) ##

### Initialization arguments ###
- `value` *(optional)*:
Any value. Using as cap.

- `xpath` *(optional)*: `str`.
XPath for extact value.

- `fields` *(optional)*:  `dict`.
Nested fields. Format: `{'field_name': field_instance}`.

- `to` *(optional)*: `type`.
Value representation. May be on of `(list, dict, int, float, str)`.
  - `list`: values in result `list` should not be a `lxml.Element`.
  - `dict`: using with nested fields.
  - `int`, `float`, `str`: first found value.


### Initialization class attributes ###
- `value` *(optional)*:
Any value. Using as cap.

- `xpath` *(optional)*: `str`.
XPath for extact value.

- `fields` *(optional)*:  `dict`.
Nested fields. Format: `{'field_name': field_instance}`.

- `to` *(optional)*: `type`.
Value representation. May be on of `(list, dict, int, float, str)`.
  - `list`: values in `list` should not be a `lxml.Element`.
  - `dict`: using with nested fields.
  - `int`, `float`, `str`: first found value.
- any nested field instance *(optional)*: `metacrawler.fields.Field` instance.


### Public attributes ###
- `value` *(optional)*:
Any value. Using as cap.

- `xpath` *(optional)*: `str`.
XPath for extact value.

- `fields` *(optional)*:  `dict`.
Nested fields. Format: `{'field_name': field_instance}`.

- `to` *(optional)*: `type`.
Value representation. May be on of `(list, dict, int, float, str)`.
  - `list`: values in `list` should not be a `lxml.Element`.
  - `dict`: using with nested fields.
  - `int`, `float`, `str`: first found value.


### Public methods ###
- `before(self)`
Call before start crawling. May use for *any* actions (dynamic set values and other).

- `clean(self, value)`
Call after finish crawling. May use for *any* actions with raw data. Must return result.
  - `value`: raw data.

- `crawl(self, page)`
Start crawling.
  - `page`: `lxml.Element`
  `lxml` reperesentation of website page.

- `get_ATTRIBUTE_NAME(self)`:
Set attribute `ATTRIBUTE_NAME` (any attribute name) by returned value at initialization.
