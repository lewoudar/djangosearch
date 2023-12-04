from django.db import models


class Character(models.Model):
    name = models.CharField(max_length=100, unique=True)
    height = models.IntegerField()
    mass = models.FloatField()
    skin_color = models.CharField(max_length=50)
    hair_color = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    birth_year = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'name={self.name}'


class Movie(models.Model):
    title = models.CharField(max_length=50, unique=True)
    episode_id = models.IntegerField()
    opening_crawl = models.TextField()
    release_date = models.DateField()
    director = models.CharField(max_length=100)
    producer = models.CharField(max_length=200)
    characters = models.ManyToManyField(Character, related_name='movies')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-release_date']

    def __str__(self):
        return f'title={self.title}'
