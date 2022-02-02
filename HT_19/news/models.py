from django.db import models

# Create your models here.

class AskStories(models.Model):
    by = models.CharField(max_length=100, default='')
    descendants = models.PositiveIntegerField(default=0)
    id_news = models.PositiveIntegerField(default=0)
    kids = models.TextField(default='')
    score = models.PositiveIntegerField(default=0)
    title = models.TextField(default='')
    text = models.TextField(default='')
    time = models.TextField(default='')
    type = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ask storie'
        verbose_name_plural = 'Ask stories'

class ShowStories(models.Model):
    by = models.CharField(max_length=200, default='')
    descendants = models.PositiveIntegerField(default=0)
    id_news = models.PositiveIntegerField(default=0)
    kids = models.TextField(default='')
    score = models.PositiveIntegerField(default=0)
    title = models.TextField(default='')
    text = models.TextField(default='')
    time = models.TextField(default='')
    type = models.CharField(max_length=50, default='')
    url = models.TextField(default='')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Show storie'
        verbose_name_plural = 'Show stories'

class NewStories(models.Model):
    by = models.CharField(max_length=200, default='')
    descendants = models.PositiveIntegerField(default=0)
    id_news = models.PositiveIntegerField(default=0)
    kids = models.TextField(default='')
    score = models.PositiveIntegerField(default=0)
    title = models.TextField(default='')
    text = models.TextField(default='')
    time = models.TextField(default='')
    type = models.CharField(max_length=50, default='')
    url = models.TextField(default='')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'New storie'
        verbose_name_plural = 'New stories'

class JobStories(models.Model):
    by = models.CharField(max_length=100, default='')
    id_news = models.PositiveIntegerField(default=0)
    score = models.PositiveIntegerField(default=0)
    title = models.TextField(default='')
    text = models.TextField(default='')
    time = models.TextField(default='')
    type = models.CharField(max_length=50, default='')
    url = models.TextField(default='')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Job storie'
        verbose_name_plural = 'Job stories'
