from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class StatusManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(status='active')


class PublishManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().active().filter(published__gte=timezone.now())


class StatusModel(models.Model):
    ACTIVE = 'active'
    DRAFT = 'draft'
    STATUS_CHOICES = (
        (ACTIVE, ACTIVE),
        (DRAFT, DRAFT),
    )
    status = models.CharField(
        verbose_name=_('status'), max_length=16,
        choices=STATUS_CHOICES, default=DRAFT, db_index=True
    )

    objects = models.Manager()
    active = StatusManager()

    class Meta:
        abstract = True


class CreatedUpdatedModel(models.Model):
    created = models.DateTimeField(_('created'), auto_now_add=True, blank=True)
    updated = models.DateTimeField(_('updated'), auto_now=True, blank=True)

    class Meta:
        abstract = True


class Tag(CreatedUpdatedModel):
    name = models.CharField(_('name'), max_length=64, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'tag'

    def __str__(self):
        return self.name


class Post(StatusModel, CreatedUpdatedModel):
    title = models.CharField(_('title'), max_length=1024)
    slug = models.SlugField(_('slug'), unique=True)
    content = models.TextField(_('content'))
    published = models.DateTimeField(_('published'), db_index=True)
    tags = models.ManyToManyField(Tag, verbose_name=_('tags'), blank=True)

    objects = models.Manager()
    active = StatusManager()
    public = PublishManager()

    class Meta:
        ordering = ('published', 'id')

    def __str__(self):
        return self.title
