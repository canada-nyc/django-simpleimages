from django.db import models

from ..transforms import scale


class TestModel(models.Model):
    image = models.ImageField(
        upload_to='testing/'
    )
    thumbnail = models.ImageField(
        blank=True,
        null=True,
        editable=False,
        upload_to='testing/thumbnails/'
    )

    transformed_fields = {
        'image': {
            'thumbnail': scale(width=10),
        }
    }
