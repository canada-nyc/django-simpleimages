import PIL
import pytest

from django.core.files.images import get_image_dimensions
import django.core.files

import simpleimages.transforms


class TestPILtransform:
    def test_callable(self, image, transform_return_same):
        transformed = transform_return_same(image.django_file)

        assert isinstance(transformed, django.core.files.File)

    def test_to_pil_image(self, image, transform):
        pil_image = transform.django_file_to_pil_image(image.django_file)

        assert isinstance(pil_image, PIL.Image.Image)

    def test_correct_size(self, image, transform):
        pil_image = transform.django_file_to_pil_image(image.django_file)

        assert pil_image.size == image.dimensions

    @pytest.fixture(params=[100, 5000])
    def large_and_small_image(self, image, request):
        image.dimensions = (request.param,) * 2
        return image

    def test_to_django_file(self, large_and_small_image, transform):
        django_file = transform.pil_image_to_django_file(large_and_small_image.pil_image)

        assert isinstance(django_file, django.core.files.File)


class TestScale:
    def test_width(self, image):
        '''
        Make sure that if width shrinks, then height shrinks
        proportionally
        '''
        transformed_size = 10

        transform = simpleimages.transforms.Scale(width=transformed_size)
        new_image = transform(image.django_file)
        assert get_image_dimensions(new_image) == (transformed_size,) * 2

    def test_width_and_height(self, image):
        '''
        Make sure that if both are set, will shrink to max of either
        '''

        transform = simpleimages.transforms.Scale(width=10, height=10)

        image.dimensions = (100, 10)
        new_image = transform(image.django_file)
        assert get_image_dimensions(new_image)[0] == 10

        image.dimensions = (10, 100)
        new_image = transform(image.django_file)
        assert get_image_dimensions(new_image)[1] == 10

    def test_over_large(self, image):
        '''
        if specified dimension is larger than image, it shouldn't enlarge
        the image
        '''
        transformed_size = 200

        transform = simpleimages.transforms.Scale(width=transformed_size)
        new_image = transform(image.django_file)
        assert get_image_dimensions(new_image) == image.dimensions

    def test_will_shrink_height(self, image):
        '''
        if specified dimension is larger than image, it shouldn't enlarge
        the image
        '''

        transform = simpleimages.transforms.Scale(height=500)
        image.dimensions = [600, 700]

        new_image = transform(image.django_file)

        new_height, new_width = get_image_dimensions(new_image)
        assert new_height == 500
