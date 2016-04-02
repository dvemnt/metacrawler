next_url:   settings.html
next_title: Settings
prev_title: Crawler
prev_url:   crawler.html

## Usage ##

```python
from metacrawler.fields import Field
from metacrawler.crawlers import Crawler
from metacrawler.handlers import Handler


class GithubRepoCrawler(Crawler):

    name = Field(xpath='//strong[@itemprop="name"]/a/text()')
    author_url = Field(xpath='//a[@rel="author"]/@href')
    description = Field(xpath='//span[@itemprop="about"]/text()')


class CustomHandler(Handler):

    repo = GithubRepoCrawler()

    def get_argparser(self):
        argparser = super().get_argparser()
        argparser.add_argument('url')
        return argparser

    def get_repo(self):
        self.repo.url = self.cli['url']
        return self.repo

if __name__ == '__main__':
    handler = CustomHandler()
    data = handler.start()
    print(data)

# Run: python file.py https://github.com/pyvim/metacrawler
# Output:
#
#{'repo': {'name': 'metacrawler', 'author_url': '/pyvim', 'description': ' A lightweight Python crawling framework.'}}
```


## metacrawler.handlers.Handler(self) ##


### Initialization class attributes ###
- `settings` *(optional)*: `metacrawler.settings.Settings` instance.
Project settings. If not passed, used empty instance.

- `authentication` *(optional)*: `metacrawler.authentication.Authentication` instance.
Using for authentication on website.

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

- `authentication`: `metacrawler.authentication.Authentication` instance.
Using for authentication on website.


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


### Public methods ###
- `before(self)`
Call before start crawling. May use for *any* actions (dynamic set values and other).

- `clean(self, value)`
Call after finish crawling. May use for *any* actions with raw data. Must return result.
  - `value`: raw data.

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
