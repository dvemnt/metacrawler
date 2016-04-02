next_url:   contributing.html
next_title: Contributing
prev_title: Pagination
prev_url:   pagination.html


## metacrawler.authentication.Authentication(self, url, xpath=None, **data) ##

### Initialization arguments ###
- `url`: `str`
Authentication page URL.

- `xpath` *(optional)*: `str`
XPath for extact form. By default extract first `form` tag.

- `**data`: `keywords arguments`
Form data. For example, `username=username, password=password`. See form `input`s `name` attributes.


### Public attributes ###
- `url`: `str`
Authentication page URL.

- `xpath` *(optional)*: `str`
XPath for extact form. By default extract first `form` tag.

- `data`: `dict`
Passed form data.


### Public methods ###
- `get_form(self, page)`
Return form element.
  - `page`: `lxml.Element`
  `lxml` reperesentation of authentication page.

- `get_login_url(self, form)`
Return login url from form.
  - `form`: `lxml.Element`
  `lxml` reperesentation of form.

- `get_form_data(self, form)`
Return data for submit.
  - `form`: `lxml.Element`
  `lxml` reperesentation of form.

- `authentication(self, session=None)`
Return session after submit form (with cookies).
  - `session`: `requests.Session`
  Using for authentication and save cookies.
