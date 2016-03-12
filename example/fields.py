# coding=utf-8


from metacrawler.items import Field


name = Field(xpath='//h1/text()')
projects = Field(xpath='//h5/text()', to=list)
