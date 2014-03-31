import pytest

from django.core.management import call_command

from simpleimages.management.commands.retransform import parse_model_specifier

from .models import TestModel


@pytest.mark.usefixtures("transactional_db")
class TestRetransform:
    def test_retransform_specific_model(self, instance):
        call_command('retransform', 'tests.TestModel')
        non_cached_instance = instance.retrieve_from_database()

        assert non_cached_instance.thumbnail

    def test_retransform_specific_field(self, instance):
        call_command('retransform', 'tests.TestModel.image')
        non_cached_instance = instance.retrieve_from_database()

        assert non_cached_instance.thumbnail

    def test_retransform_save_width_field(self, instance):
        call_command('retransform', 'tests.TestModel.image')
        non_cached_instance = instance.retrieve_from_database()

        assert non_cached_instance.thumbnail_width


class TestParseModelSpecifier:
    def test_model(self):
        model, field = parse_model_specifier('tests.TestModel')

        assert model == TestModel
        assert not field

    def test_model_and_field(self):
        model, field = parse_model_specifier('tests.TestModel.image')

        assert model == TestModel
        assert field == 'image'
