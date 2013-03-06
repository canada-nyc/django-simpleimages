from django.db import models

import simpleimages


class TestModel(models.Model):
    image = simpleimages.fields.ImageTransformField(
        upload_to="store/product_images",
        thumbs={
            'large': (
                simpleimages.utils.append_to_filename('_large'),
                simpleimages.transforms.scale(height=20),
            )
        }
    )
