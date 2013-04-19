import logging


logger = logging.getLogger(__name__)


def perform_transformation(instances, field_names=None):
    '''
    Transforms the images, from the field_name to any fields that are transformed
    from that field. Will transform the images in each of the instances. By
    default it will not save the model after transforming. Also if the
    `field_names` is false, it will resave all the fields on the model.
    '''
    for instance in instances:
        updated_fields = []
        transformed_fields_dict = instance.transformed_fields
        for original_field_name, destination_dict in transformed_fields_dict.items():
            if field_names and not original_field_name in field_names:
                break
            original_field = getattr(instance, original_field_name)
            if not original_field:
                break
            original_name = original_field.name

            for destination_field_name, transformation in destination_dict.items():
                destination_field = getattr(instance, destination_field_name)
                try:
                    new_image = transformation(original_field)
                except:
                    new_image = None
                    logger.error(
                        'The image on {} cannot be transformed from {} -> {}. None has been saved to the resulting field'.format(
                            instance,
                            original_field_name,
                            destination_field_name
                        )
                    )
                if new_image:
                    destination_field.save(
                        original_name,
                        new_image,
                        save=False
                    )
                else:
                    if destination_field:
                        destination_field.delete(
                            save=False
                        )
                updated_fields.append(destination_field_name)
        instance.save(update_fields=updated_fields)
