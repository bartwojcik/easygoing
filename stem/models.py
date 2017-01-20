from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel


class Website(SingletonModel):
    """Website configuration singleton."""
    title = models.CharField(
        max_length=1024,
        default="Don't forget to edit me!",
        verbose_name=_('Title')
    )
    header = models.TextField(default="#Don't forget to edit me!#", verbose_name=_('Header'))
    sidebar = models.TextField(default="##Don't forget to edit me!##", verbose_name=_('Sidebar'))
    footer = models.TextField(default="###Don't forget to edit me!###", verbose_name=_('Footer'))
    truncate_word_limit = models.IntegerField(default=200, verbose_name=_('Truncate word limit'))
    page_size = models.IntegerField(default=15, verbose_name=_('Page size'))

    def __str__(self):
        return 'Website configuration'

    class Meta:
        verbose_name = _('Website Configuration')


# conforming to https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
LANGUAGES = (
    ('en', 'English'),
    ('pl', 'Polski'),
)
# conforming to https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
LANGUAGE_TO_FLAG_MAP = {
    'en': 'us',
    'pl': 'pl',
}


class Post(models.Model):
    author = models.ForeignKey(User, verbose_name=_('Author'))
    created = models.DateTimeField(verbose_name=_('Created'))
    edited = models.DateTimeField(null=True, verbose_name=_('Edited'))
    language = models.CharField(max_length=2, choices=LANGUAGES, verbose_name=_('Language'))
    title = models.CharField(max_length=1024, verbose_name=_('Title'))
    content = models.TextField(verbose_name=_('Content'))
    blog_post = models.BooleanField(verbose_name=_('Is a blog post'))
    hidden = models.BooleanField(verbose_name=_('Is hidden'))
    comments_closed = models.BooleanField(verbose_name=_('Has closed comments'))
    number_of_comments = models.IntegerField(verbose_name=_('Number of comments'))

    @property
    def flag(self):
        return LANGUAGE_TO_FLAG_MAP[str(self.language)]

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')


class Comment(models.Model):
    author = models.ForeignKey(User, null=True, verbose_name=_('Author'))
    post = models.ForeignKey('Post', verbose_name=_('Post'))
    date = models.DateTimeField(verbose_name=_('Date'))
    author_name = models.CharField(max_length=255, verbose_name=_('Nick'))
    author_email = models.EmailField(blank=True, verbose_name=_('E-mail'))
    content = models.TextField(verbose_name=_('Comment text'))
    taken_down = models.BooleanField(verbose_name=_('Hidden'))

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
