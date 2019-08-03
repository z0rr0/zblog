# Zblog

[![version](https://img.shields.io/github/tag/z0rr0/zblog.svg)](https://github.com/z0rr0/zblog/releases/latest)
[![Build Status](https://travis-ci.com/z0rr0/zblog.svg?branch=master)](https://travis-ci.com/z0rr0/zblog)
[![license](https://img.shields.io/github/license/z0rr0/zblog.svg)](https://github.com/z0rr0/zblog/blob/master/LICENSE)

It's django based simple personal blog.

## Localization

Read Django docs ["Internationalization and localization"](https://docs.djangoproject.com/en/2.2/topics/i18n/) for more details.

```sh
cd blog
python manage.py makemessages -l <LANG>
# edit locale/<LANG>/LC_MESSAGES/django.po
python manage.py compilemessages
```

## Deploy

```sh
cd blog
python manage.py migrate
python manage.py createsuperuser
python manage.py compilemessages
```

## Roadmap

1. ~~base models~~
1. ~~admin pages~~
1. ~~base template~~
1. ~~flat pages~~
1. ~~index/post pages~~
1. ~~site map~~
1. ~~rss feed~~
1. error pages
1. markdown support
1. comments support

## License

This source code is governed by a MIT license that can be found in the [LICENSE](https://github.com/z0rr0/zblog/blob/master/LICENSE) file.