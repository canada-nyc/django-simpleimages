from itertools import repeat

from django.core.management.base import BaseCommand, CommandError
from django.db.models import get_model

from ... import utils


class Command(BaseCommand):
    args = '[<app.model.[field], app.model.[field], ...>]'
    help = 'Retransforms imagefields for the model(s)'

    def handle(self, *args, **options):
        for arg in args:
            self.stdout.write('Transforming {0}'.format(arg))
            arg_values = arg.split('.')
            arg_values.extend(repeat(None, 3 - len(arg_values)))
            app_name, model_name, field_name = arg_values
            self.stdout.write('app: {0}'.format(app_name))
            self.stdout.write('model: {0}'.format(model_name))
            if field_name:
                self.stdout.write('field: {0}'.format(field_name))
            model = get_model(app_name, model_name)
            if not model:
                raise CommandError('That model-app pair can not be found')
            instances = model._default_manager.all()
            self.stdout.write(
                'Transforming {0} models'.format(instances.count())
            )

            if field_name:
                utils.perform_transformation(
                    instances=instances,
                    field_names=[field_name]
                )
            else:
                utils.perform_transformation(
                    instances=instances,
                )
