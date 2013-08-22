from django.core.management.base import BaseCommand, CommandError
from django.db.models import get_model

import simpleimages.utils


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
            self.stdout.write('Transforming {0}'.format(arg))
            model, field_name = parse_model_specifier(arg)

            instances = model._default_manager.all()
            number_instances = instances.count()
            if not number_instances:
                raise CommandError('   No instances found')
            else:
                self.stdout.write(
                    '    {0} models found'.format(instances.count())
                )
            if field_name:
                self.stdout.write(
                    '    From source field name "{}"'.format(field_name)
                )
            field_names = field_name or None
            simpleimages.utils.perform_multiple_transformations(
                instances,
                field_names
            )
