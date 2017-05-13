#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from __future__ import unicode_literals
import datetime

AUTHOR = u'oneWayOut'
SITENAME = u'NutShellKing Blog'
# SITESUBTITLE = u'Samael500'
SITEURL = 'https://oneWayOut.github.io'
KEYWORDS = u'NutShellKing Blog'

PATH = 'content'

# languages settings
TIMEZONE = 'Asia/Shanghai'
DEFAULT_LANG = 'en'

# ARCHIVES_TEXT = u'归档'
# ARTICLESCATEGORY_TEXT = u'分类'
# ARTICLESTAG_TEXT = u'标签'
# AUTHOR_TEXT = u'作者'
# AUTHORS_TEXT = u'作者'
# CATEGORIES_TEXT = u'分类'
# CATEGORY_TEXT = u'分类'
# TAGS_TEXT = u'标签'
# COMMENTS_TEXT = u'评论'
# CONTENT_TEXT = u'内容'
# FIRST_TEXT = u'第一'
# LAST_TEXT = u'最后'
# READMORE_TEXT = u'继续阅读...'

# Feed generation is usually not desired when developing
FEED_DOMAIN = SITEURL

# Blogroll
LINKS = (
    ('Pixhawk', 'http://dev.px4.io/'),
    ('Python.org', 'http://python.org/'),
    ('Jinja2', 'http://jinja.pocoo.org/'),
    # ('You can modify those links in your config file', '#'),
)

# Social widget
SOCIAL = (
    # ('<i class="fa-li fa fa-vk"></i> ВКонтакте', 'https://vk.com/id44829586'),
    # ('<i class="fa-li fa fa-facebook"></i> Facebook', 'https://www.facebook.com/samael500'),
    # ('<i class="fa-li fa fa-twitter"></i> Twitter', 'https://twitter.com/samael500'),
    ('<i class="fa-li fa fa-github"></i> Github', 'https://github.com/oneWayOut'),
)

# TWITTER_USERNAME = 'samael500'
GITHUB_URL = 'https://github.com/oneWayOut'
#GOOGLE_CUSTOM_SEARCH = '006263355362628034990:cuxoisonrno'

THEME = './w3-personal-blog'

DISPLAY_PAGES_ON_MENU = True
DEFAULT_PAGINATION = 10

# url and path settings
RELATIVE_URLS = True
CACHE_CONTENT = False

STATIC_PATHS = ['images', ]
# article
ARTICLE_URL = u'articles/{category}/{slug}/'
ARTICLE_SAVE_AS = u'articles/{category}/{slug}/index.html'
# page
PAGE_URL = u'{slug}/'
PAGE_SAVE_AS = u'{slug}/index.html'
# author
AUTHOR_URL = u'author/{slug}/'
AUTHOR_SAVE_AS = u'author/{slug}/index.html'
# authors
AUTHORS_URL = u'authors/'
AUTHORS_SAVE_AS = u'authors/index.html'
# category
CATEGORY_URL = u'category/{slug}.html'
CATEGORY_SAVE_AS = u'category/{slug}.html'
# tag
TAG_URL = u'tag/{slug}/'
TAG_SAVE_AS = u'tag/{slug}/index.html'


MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
        'markdown.extensions.mathjax': {},
    },
    'output_format': 'html5',
}


CURRENT_YEAR = datetime.date.today().year
LICENSE_ROW = '''
<p><a rel="license" href="http://creativecommons.org/licenses/by/4.0/">
<img alt="Creative Commons License"
    style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/80x15.png" /></a>
This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">
Creative Commons Attribution 4.0 International License</a>.</p>'''
