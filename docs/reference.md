title:      Library Reference
prev_title: Installation
prev_url:   install


# Using MetaCrawler #

## The Basics ##

Default architecture of cralwer using MetaCrawler have next hierarchy:

- `Handler` - manages crawlers, settings and the crawl process;
- `Crawler` - load web-pages and manages items;
- `Item` - finds need blocks on the web-page and manages fields;
- `Field` - parse concrete values;

For successfully crawling need define all elements.

## Example usage ##

See [example on Github](https://github.com/pyvim/metacrawler/tree/master/example).
