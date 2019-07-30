# Zblog

It's django based simple personal blog.

## Localization

Read Django docs ["Internationalization and localization"](https://docs.djangoproject.com/en/2.2/topics/i18n/) for more details.

```shell script
cd blog
python manage.py makemessages -l <LANG>
# edit locale/<LANG>/LC_MESSAGES/django.po
python manage.py compilemessages
```

## Deploy

```shell script
cd blog
python manage.py migrate
python manage.py createsuperuser
```

## Roadmap

1. ~~base models~~
1. ~~admin pages~~
1. base template
1. error pages
1. flat pages
1. index/post pages
1. site map
1. rss feed
1. comments support