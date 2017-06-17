import re
import uuid

import mistune
import os
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from pygments import highlight
from pygments.formatters import html
from pygments.lexers import get_lexer_by_name
from solo.models import SingletonModel

from easygoing import settings


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


class HighlightRenderer(mistune.Renderer):
    def block_code(self, code, lang):
        if not lang:
            return '\n<pre><code>{}</code></pre>\n'.format(mistune.escape(code))
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter()
        return highlight(code, lexer, formatter)


renderer = HighlightRenderer()
markdown = mistune.Markdown(renderer=renderer, hard_wrap=True)


def favicon_path(*args, **kwargs):
    return 'favicon'


def navbar_logo_path(*args, **kwargs):
    return 'navbar_logo'


class Website(SingletonModel):
    """Website configuration singleton."""
    title = models.CharField(
        max_length=1024,
        default="Don't forget to edit me!",
        verbose_name=_('Title')
    )
    favicon = models.ImageField(null=True, blank=True, upload_to=favicon_path, storage=OverwriteStorage())
    navbar_logo = models.ImageField(null=True, blank=True, upload_to=navbar_logo_path, storage=OverwriteStorage())
    sidebar = models.TextField(default="###Don't forget to edit me!###", blank=True, verbose_name=_('Sidebar'))
    sidebar_processed = models.TextField()
    footer = models.TextField(default="##Don't forget to edit me!##", blank=True, verbose_name=_('Footer'))
    footer_processed = models.TextField()
    truncate_word_limit = models.IntegerField(default=150, verbose_name=_('Truncate word limit'))
    page_size = models.IntegerField(default=10, verbose_name=_('Page size'))

    def __str__(self):
        return 'Website configuration'

    def save(self, *args, **kwargs):
        self.sidebar_processed = markdown(self.sidebar)
        self.footer_processed = markdown(self.footer)
        favicon_full_path = os.path.join(settings.MEDIA_ROOT, favicon_path())
        if not self.favicon and os.path.exists(favicon_full_path):
            os.remove(favicon_full_path)
        navbar_logo_full_path = os.path.join(settings.MEDIA_ROOT, navbar_logo_path())
        if not self.navbar_logo and os.path.exists(navbar_logo_full_path):
            os.remove(navbar_logo_full_path)
        super().save(*args, **kwargs)

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
    created = models.DateTimeField(verbose_name=_('Created'), auto_now_add=True)
    edited = models.DateTimeField(null=True, verbose_name=_('Edited'), default=None)
    language = models.CharField(max_length=2, choices=LANGUAGES, verbose_name=_('Language'))
    title = models.CharField(max_length=1024, verbose_name=_('Title'))
    content = models.TextField(verbose_name=_('Content'))
    content_processed = models.TextField()
    content_length = models.IntegerField()
    blog_post = models.BooleanField(verbose_name=_('Is visible on main site'), default=True)
    hidden = models.BooleanField(verbose_name=_('Is inaccessible to guests'), default=True)
    comments_closed = models.BooleanField(verbose_name=_('Has closed comments'), default=False)
    number_of_comments = models.IntegerField(verbose_name=_('Number of comments'), default=0)

    @property
    def flag(self):
        return LANGUAGE_TO_FLAG_MAP[str(self.language)]

    def save(self, *args, **kwargs):
        self.content_length = len(re.findall(r'\w+', str(self.content)))
        self.content_processed = markdown(self.content)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post', args=[str(self.pk)])

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')


class Comment(models.Model):
    author = models.ForeignKey(User, null=True, verbose_name=_('Author'))
    post = models.ForeignKey('Post', verbose_name=_('Post'))
    date = models.DateTimeField(verbose_name=_('Date'))
    author_name = models.CharField(max_length=255, verbose_name=_('Nick'))
    author_email = models.EmailField(blank=True, verbose_name=_('e-mail'))
    content = models.TextField(verbose_name=_('Comment text'))
    taken_down = models.BooleanField(verbose_name=_('Hidden'))

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')


def gen_uuid():
    return uuid.uuid4().hex


def get_upload_path(instance, filename):
    instance.filename = filename
    return instance.uuid


class UploadedFile(models.Model):
    file = models.FileField(verbose_name=_('File'), upload_to=get_upload_path)
    uuid = models.CharField(max_length=36, default=gen_uuid, unique=True, db_index=True)
    filename = models.CharField(max_length=255, verbose_name=_("File's name"))
    owner = models.ForeignKey(User, null=True, verbose_name=_('Owner'))
    hidden = models.BooleanField(verbose_name=_('Is inaccessible to guests'), default=True)
    upload_date = models.DateTimeField(verbose_name=_('Upload Date'))
    description = models.CharField(max_length=255, verbose_name=_("File's description"))

    class Meta:
        verbose_name = _('Uploaded File')
        verbose_name_plural = _('Uploaded File')
