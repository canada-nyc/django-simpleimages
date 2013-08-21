import PIL
import pytest

from django.core.files.images import get_image_dimensions
import django.core.files

import simpleimages.transforms


class TestPILTransform:
    @pytest.fixture()
    def Transform(self):
        return simpleimages.transforms.BasePILTransform()

    @pytest.fixture()
    def Transform_Blank(self, Transform):
        Transform.transform_pil_image = lambda pil_image: pil_image
        return Transform

    def test_callable(self, image, Transform_Blank):
        transformed = Transform_Blank(image.django_file)

        assert isinstance(transformed, django.core.files.File)

    def test_to_pil_image(self, image, Transform):
        pil_image = Transform.django_file_to_pil_image(image.django_file)

        assert isinstance(pil_image, PIL.Image.Image)

    def test_correct_size(self, image, Transform):
        pil_image = Transform.django_file_to_pil_image(image.django_file)

        assert pil_image.size == image.dimensions

    @pytest.fixture(params=[100, 5000])
    def large_and_small_image(self, image, request):
        image.dimensions = (request.param,) * 2
        return image

    def test_to_django_file(self, large_and_small_image, Transform):
        django_file = Transform.pil_image_to_django_file(large_and_small_image.pil_image)

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
        new_height, new_width = get_image_dimensions(new_image)
        assert get_image_dimensions(new_image) == (transformed_size,) * 2

    def test_over_large(self, image):
        '''
        if specified dimension is larger than image, it shouldn't enlarge
        the image
        '''
        transformed_size = 200

        transform = simpleimages.transforms.Scale(width=transformed_size)
        new_image = transform(image.django_file)
        new_height, new_width = get_image_dimensions(new_image)
        assert get_image_dimensions(new_image) == image.dimensions
