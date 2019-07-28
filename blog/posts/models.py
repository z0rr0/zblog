from datetime import datetime

from django.db import models


class StatusManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(status='active')


class PublishManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().active().filter(published__gte=datetime.now())


class StatusModel(models.Model):
    ACTIVE = 'active'
    DRAFT = 'draft'
    STATUS_CHOICES = (
        (ACTIVE, ACTIVE),
        (DRAFT, DRAFT),
    )
    status = models.CharField('status', max_length=16, choices=STATUS_CHOICES, default=DRAFT, db_index=True, blank=True)

    objects = models.Manager()
    active = StatusManager()

    class Meta:
        abstract = True


class CreatedUpdatedModel(models.Model):
    created = models.DateTimeField('created', auto_now_add=True, blank=True)
    updated = models.DateTimeField('updated', auto_now=True, blank=True)

    class Meta:
        abstract = True


class Tag(CreatedUpdatedModel):
    name = models.CharField('name', max_length=64, unique=True)

    class Meta:
        ordering = ('name',)


class Post(StatusModel, CreatedUpdatedModel):
    title = models.CharField('title', max_length=1024)
    slug = models.SlugField('slug', unique=True)
    content = models.TextField('content')
    published = models.DateTimeField('published', db_index=True)
    tags = models.ManyToManyField(Tag, blank=True)

    objects = models.Manager()
    active = StatusManager()
    public = PublishManager()

    class Meta:
        ordering = ('published', 'id')
