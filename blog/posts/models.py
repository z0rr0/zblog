from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class StatusManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class PublishManager(StatusManager):

    def get_queryset(self):
        return super().get_queryset().filter(publish__lte=timezone.now())


class PublishTagManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(posts__status='published', posts__publish__lte=timezone.now())


class StatusModel(models.Model):
    PUBLISHED = 'published'
    DRAFT = 'draft'
    DELETED = 'deleted'
    STATUS_CHOICES = (
        (PUBLISHED, _('published')),
        (DRAFT, _('draft')),
        (DELETED, _('deleted')),
    )
    status = models.CharField(
        verbose_name=_('status'), max_length=16,
        choices=STATUS_CHOICES, default=DRAFT, db_index=True,
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
    name = models.SlugField(_('name'), max_length=64, unique=True)

    objects = models.Manager()
    published = PublishTagManager()

    class Meta:
        ordering = ('name',)
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self) -> str:
        return self.name

    @property
    def url(self):
        return reverse_lazy('tag_filter', args=(self.name))


class Post(StatusModel, CreatedUpdatedModel):
    title = models.CharField(_('title'), max_length=512, db_index=True)
    slug = models.SlugField(_('slug'), unique_for_date='publish')
    body = models.TextField(_('body'))
    publish = models.DateTimeField(_('date of publication'), db_index=True, default=timezone.now)
    tags = models.ManyToManyField(Tag, verbose_name=_('tags'), blank=True, related_name='posts')

    objects = models.Manager()
    active = StatusManager()
    published = PublishManager()

    class Meta:
        ordering = ('-publish', '-id')
        verbose_name = _('post')
        verbose_name_plural = _('posts')

    def __str__(self) -> str:
        return self.title

    @property
    def url(self):
        tz = timezone.get_current_timezone()
        local = tz.normalize(self.publish)
        return reverse_lazy('read', args=(local.year, local.month, local.day, self.slug))

    def get_absolute_url(self):
        return self.url


class Comment(StatusModel, CreatedUpdatedModel):
    post = models.ForeignKey(Post, verbose_name=_('post'), related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(_('author'), max_length=512, null=True, blank=True)
    message = models.TextField(_('message'), help_text=_('comment text'))
    reply = models.ForeignKey(
        'self', verbose_name=_('reply'), on_delete=models.DO_NOTHING,
        help_text=_('reply to comment'), null=True, blank=True,
    )

    class Meta:
        ordering = ('post', '-pk')
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    def __str__(self) -> str:
        return 'Comment #{} for post "{}"'.format(self.pk, self.post)


class Attachment(CreatedUpdatedModel):
    name = models.CharField(_('name'), max_length=255)
    data = models.FileField(_('data'), max_length=1024)

    class Meta:
        verbose_name = _('attachment')
        verbose_name_plural = _('attachments')

    def __str__(self) -> str:
        return self.data.url
