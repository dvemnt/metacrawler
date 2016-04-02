next_url:   authentication.html
next_title: Authentication
prev_title: Settings
prev_url:   settings.html


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
