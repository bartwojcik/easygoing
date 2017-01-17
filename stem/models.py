from django.contrib.auth.models import User
from django.db import models
from solo.models import SingletonModel


class Website(SingletonModel):
    """Website configuration singleton."""
    title = models.CharField(max_length=1024)
    header = models.TextField()
    sidebar = models.TextField()
    truncate_word_limit = models.IntegerField(null=True)
    page_size = models.IntegerField(null=True)

    def __str__(self):
        return 'Website configuration'

    class Meta:
        verbose_name = 'Website Configuration'


# conforming to https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
LANGUAGES = (
    ('en', 'English'),
    ('pl', 'Polski'),
)


class Post(models.Model):
    author = models.ForeignKey(User)
    created = models.DateTimeField()
    edited = models.DateTimeField(null=True)
    language = models.CharField(max_length=2, choices=LANGUAGES)
    title = models.CharField(max_length=1024)
    content = models.TextField()
    blog_post = models.BooleanField()
    hidden = models.BooleanField()
    comments_closed = models.BooleanField()
    number_of_comments = models.IntegerField()


class Comment(models.Model):
    author = models.ForeignKey(User, null=True)
    post = models.ForeignKey('Post')
    ip_address = models.GenericIPAddressField()  # just in case
    date = models.DateTimeField()
    author_name = models.CharField(max_length=255)
    author_email = models.EmailField()
    content = models.TextField()
    taken_down = models.BooleanField()
