next_url:   handler.html
next_title: Handler
prev_title: Field
prev_url:   field.html

## Usage ##

```python
from metacrawler.fields import Field
from metacrawler.crawlers import Crawler


class GithubRepoCrawler(Crawler):

    repo_name = Field(xpath='//strong[@itemprop="name"]/a/text()')
    author_url = Field(xpath='//a[@rel="author"]/@href')
    description = Field(xpath='//span[@itemprop="about"]/text()')


crawler = GithubRepoCrawler()
crawler.url = 'https://github.com/pyvim/metacrawler'
content = crawler.crawl()
print(content)

# Output:
#
#{'repo_name': 'metacrawler', 'description': ' A lightweight Python crawling framework.', 'author_url': '/pyvim'}
```


## metacrawler.crawlers.Crawler(self) ##


### Initialization class attributes ###
- `url` *(optional)*:  `str`.
URL of page for crawling.

- `collapse` *(optional)*:  `bool`.
Collapse crawler key in result data. For example, `{'crawler': {'field': []}}` to `{'cralwer': []}`. Work only with single field. If fields will be more raise `ValueError` exception.

- `session` *(optional)*: `requests.Session` instance.
Using for make requests.

- `pagination` *(optional)*: `metacrawler.pagination.Pagination` instance.
Using for navigate on website pages.

- `authentication` *(optional)*: `metacrawler.authentication.Authentication` instance.
Using for authentication on website.

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

- `authentication` *(optional)*: `metacrawler.authentication.Authentication` instance.
Using for authentication on website.

- `limit` *(optional)*: `int`.
Limit of results. Count of result may be more than limit due pagination.

- `timeout` *(optional)*: `float`.
Timeout before current connection will be closed.

- `data`: `dict` or `list`.
Contains data after crawling.


### Public methods ###
- `before(self)`
Call before start crawling. May use for *any* actions (dynamic set values and other).

- `clean(self, value)`
Call after finish crawling. May use for *any* actions with raw data. Must return result.
  - `value`: raw data.

- `crawl(self, *args, **kwargs)`
Start crawling.

- `paginate(self, page)`:
Return next url for crawling if has `pagination` attribute.
  - `page`: `lxml.Element`
  `lxml` reperesentation of website page.

- `get_ATTRIBUTE_NAME(self)`:
Set attribute `ATTRIBUTE_NAME` (any attribute name) by returned value at initialization.
