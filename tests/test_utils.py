class TestTransformField:
    def test_blank_transform_wont_save(self, instance_with_source):
        instance_with_source._transform(lambda file: None)

        assert not instance_with_source.thumbnail

    def test_will_save(self, instance_with_source):
        instance_with_source._transform()

        assert instance_with_source.thumbnail

    def test_no_overwrite(self, settings, instance_with_source_and_thumb):
        settings.SIMPLEIMAGES_OVERWRITE = False

        instance_with_source_and_thumb._transform()

        assert not instance_with_source_and_thumb.thumbnail.width == instance_with_source_and_thumb.image.width

    def test_yes_overwrite(self, settings, instance_with_source_and_thumb):
        settings.SIMPLEIMAGES_OVERWRITE = True

        instance_with_source_and_thumb._transform()

        assert instance_with_source_and_thumb.thumbnail.width == instance_with_source_and_thumb.image.width
