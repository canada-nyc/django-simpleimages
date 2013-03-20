from itertools import repeat

from django.core.management.base import BaseCommand
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
            model = get_model(app_name, model_name)
            instances = model._default_manager.all()
            self.stdout.write('Transforming {0}.{1}'.format(instances, field_name))

            utils.perform_transformation(
                instances=instances,
                field_names=[field_name]
            )
