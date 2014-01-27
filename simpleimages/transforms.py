import six

from PIL import Image

from django.core.files.base import ContentFile
import django.core.files


class BasePILTransform(object):
    '''
    Base transform object that provides helper methods to transform
    :py:class:`django.core.files.images.ImageFile` using
    :py:mod:`PIL`.

    Must subclass and override :py:meth:`~.BasePILTransform.transform_pil_image`.
    '''

    IMAGE_QUALITY = 85

    def __call__(self, original_django_file):
        '''
        Returns the transformed version of :py:class:`PIL.Image.Image`

        Uses :py:meth:`~.BasePILTransform.transform_pil_image` to transform
        the :py:class:`PIL.Image.Image`.

        :param original_django_file: source file
        :type original_django_file: :py:class:`django.core.files.images.ImageFile`
        :return: transformed file
        :rtype: :py:class:`django.core.files.File`
        '''
        if not isinstance(original_django_file, django.core.files.File):
            raise TypeError(
                'image is a {0}, not a django File'.format(type(original_django_file))
            )
        if not original_django_file.file:
            raise ValueError(
                'the django file has no file saved to it.'
            )

        return self.pil_image_to_django_file(
            self.transform_pil_image(
                self.django_file_to_pil_image(original_django_file)
            )
        )

    def pil_image_to_django_file(self, pil_image):
        '''
        Gets a PIL image ready to be able to be saved using
        :py:meth:`django.db.models.fields.files.FieldFile.save`

        It converts the mode first to ``RGB`` or ``L``, so that it can
        then save it as a ``JPEG``. It will save it as a progressive
        ``JPEG`` with a quality of :py:attr:`IMAGE_QUALITY`.

        :param pil_image: original image
        :type pil_image: :py:class:`PIL.Image.Image`
        :return: transformed image
        :rtype: :py:class:`django.core.files.base.ContentFile`
        '''
        if pil_image.mode not in ('L', 'RGB'):
            pil_image = pil_image.convert("RGB")
        temp_io = six.BytesIO()

        pil_image.save(
            temp_io,
            "JPEG",
            quality=self.IMAGE_QUALITY,
            optimize=True,
            progressive=True
        )

        temp_io.seek(0)
        django_file = ContentFile(temp_io.getvalue())
        return django_file

    def transform_pil_image(self, pil_image):
        '''
        Returns the transformed version of the :py:class:`PIL.Image.Image`
        Do some logic on :py:class:`PIL.Image.Image`.

        Must subclass method to provide transformation logic.

        :param pil_image: original image
        :type pil_image: :py:class:`PIL.Image.Image`
        :return: transformed image
        :rtype: :py:class:`PIL.Image.Image`
        '''
        raise NotImplementedError

    def django_file_to_pil_image(self, django_file):
        '''
        Converts a the file returned by
        :py:class:`django.db.models.fields.ImageField` to a PIL image.

        :param django_file: django file
        :type django_file: :py:class:`django.db.models.fields.files.FieldFile`
        :rtype: :py:class:`PIL.Image.Image`
        '''
        django_file.open()
        pil_image = Image.open(django_file.file)
        return pil_image


class Scale(BasePILTransform):
    '''
    Scales down an image to max height and/or width. If the original
    image is smaller than both/either specified dimensions than it will
    be left unchanged.
    '''

    def __init__(self, width=None, height=None):
        '''
        Initialize this class with a max height and/or width (in pixels).

        :param height: max height of scaled image
        :param width: max width of scaled image
        :type height: int or float
        :type width: int or float
        '''
        self.dimensions = (width, height)
        if not any(self.dimensions):
            raise ValueError(
                'Must be called with either `height` or `width`'
            )

    def transform_pil_image(self, pil_image):
        '''
        Uses :py:meth:`PIL.Image.Image.transform` to scale
        down the image.

        Based on `this stackoverflow discussions <http://stackoverflow.com/a/940368/907060>`_, uses
        :attr:`PIL.Image.ANTIALIAS`
        '''
        max_width = min(self.dimensions[0] or float('inf'), pil_image.size[0])
        max_height = min(self.dimensions[1] or float('inf'), pil_image.size[1])
        max_dimensions = (max_width, max_height)

        pil_image.thumbnail(max_dimensions, Image.ANTIALIAS)
        return pil_image
