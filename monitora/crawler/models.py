from django.db import models
from unidecode import unidecode


class Movie(models.Model):
    name = models.CharField(max_length=200)
    stripped_name = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        self.stripped_name = unidecode(self.name.lower().replace(" ", ""))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=200)
    stripped_name = models.CharField(max_length=200)
    movies = models.ManyToManyField(Movie)

    def save(self, *args, **kwargs):
        self.stripped_name = unidecode(self.name.lower().replace(" ", ""))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
