from django.db import models

from ..transforms import scale


class TestModel(models.Model):
    image = models.ImageField(
        upload_to='originals/'
    )
    thumbnail = models.ImageField(
        blank=True,
        null=True,
        editable=False,
        upload_to='thumbnails/',
        width_field='thumbnail_width'
    )

    thumbnail_width = models.PositiveIntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    transformed_fields = {
        'image': {
            'thumbnail': scale(width=10),
        }
    }
