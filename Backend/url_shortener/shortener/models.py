from django.db import models


class URL(models.Model):
    """
    Model to store URLs and their shortened versions.

    This model represents a URL and its corresponding shortened version.
    Each URL object has fields to store the original URL, a slug for identification,
    and a shortened URL. The original URL must be unique to ensure that no duplicates
    are stored. The slug is a short string used for identification purposes. The short
    URL is the actual shortened version of the original URL.

    Attributes:
        url_id (AutoField): The primary key representing the URL's unique identifier.
        original_url (URLField): The original URL to be shortened.
        slug (CharField): A short string used for identification.
        short_url (CharField): The shortened version of the original URL.

    Methods:
        save(): Overrides the default save method to assign a unique URL ID to each URL object.
    """
    url_id = models.AutoField(primary_key=True)
    original_url = models.URLField(unique=True)
    slug = models.CharField(max_length=20)
    short_url = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        self.url_id = (URL.objects.count()) + 1
        super().save(*args, **kwargs)


