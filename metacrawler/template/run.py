# coding=utf-8

from elements.handlers import YourHandler

if __name__ == '__main__':
    YourHandler.settings.load_from_file('settings.config')
    YourHandler().run()
