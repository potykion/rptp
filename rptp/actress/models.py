from random import randint
from typing import Optional

from django.contrib.postgres.fields import ArrayField
from django.db import models

DEFAULT_ACTRESS = 'Sasha'


class ActressManager(models.Manager):
    """
    Provide custom bulk operations for Actress model.
    """

    def get_random(self) -> Optional['Actress']:
        """
        Count Actress entities, get random actress.
        Returns:
            Random actress or None if no actress present.

        """
        count = self.count()

        if count:
            random_index = randint(0, count - 1)
            return self.all()[random_index]
        else:
            return None


class Actress(models.Model):
    """
    Actress model.
    """
    name = models.CharField(max_length=200)
    other_names = ArrayField(models.CharField(max_length=200))
    debut_year = models.IntegerField()
    ptg_link = models.URLField()

    photo = models.URLField()
    thumb = models.URLField()

    vk_video_count = models.IntegerField()
    vk_last_video_date = models.DateTimeField(null=True)

    objects = ActressManager()

    def __str__(self):
        return 'Actress(name={})'.format(self.name)
