from django.db import models

import simpleimages.utils
import simpleimages.transforms


class TestModel(models.Model):
    transform_max_width = 5

    image = models.ImageField(
        upload_to='originals/'
    )
    thumbnail = models.ImageField(
        blank=True,
        null=True,
        editable=False,
        upload_to='thumbnails/',
        width_field='thumbnail_width',
        height_field='thumbnail_height'
    )

    thumbnail_width = models.PositiveIntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    thumbnail_height = models.PositiveIntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    transformed_fields = {
        'image': {
            'thumbnail': simpleimages.transforms.Scale(width=transform_max_width),
        }
    }

    def retrieve_from_database(self):
        return TestModel.objects.get(pk=self.pk)
