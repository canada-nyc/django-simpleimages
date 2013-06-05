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
        logger.debug('Transforming images on "{0}"'.format(instance))
        updated_fields = []
        transformed_fields_dict = instance.transformed_fields
        for original_field_name, destination_dict in transformed_fields_dict.items():
            if field_names and not original_field_name in field_names:
                logger.debug('"{0}" field isnt being transformed'.format(
                    original_field_name
                ))
                break
            original_field = getattr(instance, original_field_name)
            if not original_field:
                logger.debug('"{0}" field is empty'.format(original_field_name))
                break
            original_name = original_field.name
            logger.debug('Transforming "{0}" file from "{1}" field'.format(
                original_name,
                original_field_name
            ))
            for destination_field_name, transformation in destination_dict.items():
                logger.debug('Performing transformation to "{0}" field'.format(
                    destination_field_name
                ))
                destination_field = getattr(instance, destination_field_name)
                new_image = transformation(original_field)
                if new_image:
                    logger.debug('Saving new image')
                    destination_field.save(
                        original_name,
                        new_image,
                        save=False
                    )
                else:
                    logger.error(
                        'The image on {0} was not transformed from {1} -> {2}'.format(
                            instance,
                            original_field_name,
                            destination_field_name
                        )
                    )
                updated_fields.append(destination_field_name)
        if updated_fields:
            logger.debug('{0}fields updated, saving instance'.format(
                ', '.join(updated_fields)
            ))
            instance.save(update_fields=updated_fields)
        else:
            logger.debug('No fields updated')
