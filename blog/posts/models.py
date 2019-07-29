from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class StatusManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class PublishManager(StatusManager):

    def get_queryset(self):
        return super().get_queryset().filter(published__gte=timezone.now())


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
    name = models.CharField(_('name'), max_length=64, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return self.name


class Post(StatusModel, CreatedUpdatedModel):
    title = models.CharField(_('title'), max_length=512, db_index=True)
    slug = models.SlugField(_('slug'), unique=True)
    content = models.TextField(_('content'))
    published = models.DateTimeField(_('published'), db_index=True)
    tags = models.ManyToManyField(Tag, verbose_name=_('tags'), blank=True)

    objects = models.Manager()
    active = StatusManager()
    public = PublishManager()

    class Meta:
        ordering = ('published', 'id')
        verbose_name = _('post')
        verbose_name_plural = _('posts')

    def __str__(self):
        return self.title


class Comment(StatusModel, CreatedUpdatedModel):
    post = models.ForeignKey(Post, verbose_name=_('post'), on_delete=models.CASCADE)
    author = models.CharField(_('author'), max_length=512, null=True, blank=True)
    message = models.TextField(_('message'), help_text=_('comment text'))
    like = models.PositiveIntegerField(_('like'), default=0, blank=True)
    dislike = models.PositiveIntegerField(_('dislike'), default=0, blank=True)
    reply = models.ForeignKey(
        'self', verbose_name=_('reply'), on_delete=models.DO_NOTHING,
        help_text=_('reply to comment'), null=True, blank=True,
    )

    class Meta:
        ordering = ('post', '-pk')
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    def __str__(self):
        return 'Comment #{} for post "{}"'.format(self.pk, self.post)
