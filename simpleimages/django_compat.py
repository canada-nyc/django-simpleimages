'''
Code that is necessary for supporting older Django versions
'''

try:
    from django.apps.config import get_model
except ImportError:  # Django < 1.8 pragma: no cover
    from django.db.models import get_model


def import_by_path(dotted_path, error_prefix=''):  # pragma: no cover
    """
    Added in Django 1.6 to django.utils.module_loading

    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImproperlyConfigured if something goes wrong.
    """
    from importlib import import_module
    import sys

    from django.core.exceptions import ImproperlyConfigured
    from django.utils import six

    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        raise ImproperlyConfigured("%s%s doesn't look like a module path" % (
            error_prefix, dotted_path))
    try:
        module = import_module(module_path)
    except ImportError as e:
        msg = '%sError importing module %s: "%s"' % (
            error_prefix, module_path, e)
        six.reraise(ImproperlyConfigured, ImproperlyConfigured(msg),
                    sys.exc_info()[2])
    try:
        attr = getattr(module, class_name)
    except AttributeError:
        raise ImproperlyConfigured('%sModule "%s" does not define a "%s" attribute/class' % (
            error_prefix, module_path, class_name))
    return attr
