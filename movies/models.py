from django.db import models
from django.utils.translation import gettext_lazy as _

class Movie(models.Model):
    english_title = models.CharField(_('English title'), max_length=128, unique=True)
    russian_title = models.CharField(_('Russian title'), max_length=128, unique=True)
    my_rating = models.PositiveIntegerField(_('my rating'), choices=list(range(1, 10 + 1)))
    release_year = models.PositiveIntegerField(_('release year'))
    my_comment = models.TextField(_('my review'), blank=True)
    times_watched = models.PositiveIntegerField(_('times watched'), default=False)
    watched_date = models.DateField(_('watched date'), null=True, blank=True)
    is_to_rewatch = models.BooleanField(_('is marked to rewatch?'), default=False)

    class Meta:
        verbose_name = _('movie')
        verbose_name_plural = _('movies')

class Person(models.Model):
    name = models.CharField(_('person', 'name'), max_length=128, unique=True)

class Actor(Person):
    movie = models.ManyToManyField(Movie, verbose_name=_('movie'))

class Director(Person):
    movie = models.ManyToManyField(Movie, verbose_name=_('movie'))

class Writer(Person):
    movie = models.ManyToManyField(Movie, verbose_name=_('movie'))

class Producer(Person):
    movie = models.ManyToManyField(Movie, verbose_name=_('movie'))