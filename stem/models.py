from django.contrib.auth.models import User
from django.db import models
from solo.models import SingletonModel


class Website(SingletonModel):
    """Website configuration singleton."""
    sidebar = models.TextField()

    def __str__(self):
        return 'Website configuration'

    class Meta:
        verbose_name = 'Website Configuration'


# conforming to https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
LANGUAGES = (
    ('en', 'English'),
    ('pl', 'Polski'),
)


class Article(models.Model):
    author = models.ForeignKey(User)
    created = models.DateTimeField()
    edited = models.DateTimeField()
    language = models.CharField(max_length=2, choices=LANGUAGES)
    title = models.CharField(max_length=4096)
    content = models.TextField()
    blog_post = models.BooleanField()
    hidden = models.BooleanField()


class Comment(models.Model):
    author = models.ForeignKey(User, null=True)
    article = models.ForeignKey('Article')
    ip_address = models.GenericIPAddressField()  # just in case
    date = models.DateTimeField()
    author_name = models.CharField(max_length=255)
    title = models.CharField(max_length=2048)
    content = models.TextField()
    taken_down = models.BooleanField()
