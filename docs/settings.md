next_url:   pagination.html
next_title: Pagination
prev_title: Handler
prev_url:   handler.html

## metacrawler.settings.Settings(self, configspec=None, configuration=None) ##

### Initialization arguments ###
- `configspec` *(optional)*: `dict`.
Validation specification. See http://www.voidspace.org.uk/python/configobj.html#configspec.
- `configuration` *(optional)*: `dict`.
Concrete configuration.


### Public attributes ###
For `configuration` using dynamic access using `configuration` key as attribute name.
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
