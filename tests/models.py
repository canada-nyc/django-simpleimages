from django.db import models
from django.core.files.images import get_image_dimensions

import simpleimages.utils
import simpleimages.transforms


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
            'thumbnail': simpleimages.transforms.Scale(width=10),
        }
    }

    def _transform(self, transformation=lambda file: file):
        simpleimages.utils.transform_field(
            instance=self,
            source_field_name='image',
            destination_field_name='thumbnail',
            transformation=transformation
        )

    @property
    def image_dimensions(self):
        self.image.open()
        return get_image_dimensions(self.image)

    @property
    def thumbnail_dimensions(self):
        self.thumbnail.open()
        return get_image_dimensions(self.thumbnail)
