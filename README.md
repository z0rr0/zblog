# zorro.website


### Localization

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
