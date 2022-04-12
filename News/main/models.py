from django.db import models
# Create your models here.
from News.accounts.models import NewsUser


class Profile(models.Model):
    email = models.EmailField(

    )
    first_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    profile_image = models.ImageField(
        null=True,
        blank=True,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    user = models.OneToOneField(
        NewsUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        return self.email

    def get_short_name(self):
        if self.first_name:
            return f'{self.first_name}'
        return self.email


class NewsSite(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField(
        null=True,
        blank=True,
    )
    image = models.ImageField(
        null=True,
        blank=True,
    )


    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    content = models.TextField(
        null=True,
        blank=True,
    )
    news_site = models.ForeignKey(
        NewsSite,
        on_delete=models.CASCADE,
    )

    date_published = models.DateTimeField(
        null=True,
        blank=True,
    )

    date_modified = models.DateTimeField(
        null=True,
        blank=True,
    )

    image = models.URLField(
        null=True,
        blank=True,
    )

    saved_by = models.ManyToManyField(
        Profile, related_name='saved', blank=True,
    )

    liked_by = models.ManyToManyField(
        Profile, related_name='liked', blank=True,
    )

    disliked_by = models.ManyToManyField(
        Profile, related_name='disliked', blank=True,
    )

    def get_likes(self):
        return self.liked_by.count()

    def get_dislikes(self):
        return self.disliked_by.count()

    def get_likes_dislikes_sum(self):
        return int(self.get_likes()) - int(self.get_dislikes())

    def __str__(self):
        return self.title


