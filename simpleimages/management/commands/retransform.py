from clint.textui import puts, indent, progress

from django.core.management.base import BaseCommand

import simpleimages.utils
from simpleimages.django_compat import get_model


def parse_model_specifier(specifier):
    '''
    Parses a string that specifies either a model or a field.
    The string should look like ``app.model.[field]``.

    >>> print parse_model_specifier('tests.TestModel')
    (<class 'tests.models.TestModel'>, None)
    >>> print parse_model_specifier('tests.TestModel.image')
    (<class 'tests.models.TestModel'>, 'image')

    :return: model and (optionally) field name
    :rtype: tuple of :py:class:`~django.db.models.Model` and str or None
    '''
    values = specifier.split('.')

    if len(values) == 2:
        values.append(None)
    elif len(values) != 3:
        raise ValueError(
            'Model specifier must be in app.model.[field] format. It'
            'has {} parts instead of 2 or 3 (when split on ".")'.format(
                len(values)
            )
        )

    app_name, model_name, field_name = values
    model = get_model(app_name, model_name)
    if not model:
        raise ValueError(
            'Model {} on app {} can not be found'.format(
                model_name,
                app_name,
            )
        )
    return model, field_name


class Command(BaseCommand):
    args = '[<app.model.[field], app.model.[field], ...>]'
    help = 'Retransforms imagefields for the model(s)'

    def handle(self, *args, **options):
        for arg in args:
            puts('Transforming {0}'.format(arg))
            model, field_name = parse_model_specifier(arg)

            instances = model._default_manager.all()
            number_instances = instances.count()
            with indent(4):
                if not number_instances:
                    puts('No instances found')
                    continue

                else:
                    puts('{0} models found'.format(instances.count()))
                if field_name:
                    puts('From source field name "{0}"'.format(field_name))
            field_names = field_name or None

            for instance in progress.bar(instances):
                simpleimages.utils.perform_transformation(instance, field_names)
