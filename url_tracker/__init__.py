from functools import partial
import logging
logger = logging.getLogger(__file__)

from django.db.models import signals

from url_tracker.models import URLChangeRecord


class URLTrackingError(Exception):
    """
    Exception raised when an error occures during URL tracking.
    """
    pass


def get_dispatch_uid(absolute_url_method):
    """
    Return a dispatch_uid to use in all signals based on the
    *absolute_url_method* for the model.
    """
    return 'urltracker.track_url_changes_for_model.' + absolute_url_method


def lookup_previous_url(absolute_url_method, instance, **kwargs):
    """
    Look up the absolute URL of *instance* from the database while it is
    in a ``pre_save`` state. Adds a post save signal that will compare the
    previous url to the new url based on the *absoulute_url_method*.

    If the instance has not been saved to the database (i.e. is new) the
    old_url will sent as ``None`` which will prevent further tracking
    after saving the instance.
    """
    model = instance.__class__
    try:
        db_instance = model.objects.get(pk=instance.pk)
    except model.DoesNotExist:
        logger.debug("new instance, no URL tracking required")
        old_url = None
    else:
        logger.debug("saving old URL for instance '%s' URL", instance.__class__.__name__)
        old_url = getattr(db_instance, absolute_url_method)()

    # Send the dispatch_uid to the signal, so that it will disconnect itself
    # since the signal function is specific to the only this old_url
    track_changed_url_for_model = partial(
        track_changed_url,
        old_url=old_url,
        absolute_url_method=absolute_url_method,
        signal_dispatch_uid=get_dispatch_uid(absolute_url_method),
    )
    signals.post_save.connect(
        track_changed_url_for_model,
        sender=model,
        weak=False,
        dispatch_uid=get_dispatch_uid(absolute_url_method)
    )


def track_changed_url(old_url, absolute_url_method, signal_dispatch_uid, instance, **kwargs):
    """
    Deactivate the signal that called this function,
    based on the *signal_dispatch_uid*, because this function is specific
    to a certain *old_url* and has to be recreated on every pre_save.

    Then call ``change_urls`` with the *old_url*, *absolute_url_method*,
    and *instance*.
    """
    signals.post_save.disconnect(
        weak=False,
        sender=instance.__class__,
        dispatch_uid=signal_dispatch_uid
    )
    change_urls(old_url, absolute_url_method, instance)


def change_urls(old_url, absolute_url_method, instance):
    """
    Track a URL change for *instance* after a new instance was saved. If
    the *old_url* is ``None`` (i.e. *instance* is new) or the new URL and
    the old one are equal (i.e. URL is unchanged), nothing will be changed
    in the database.

    For URL changes, the database will be checked for existing records that
    have a *new_url* entry equal to the old URL of *instance* and updates
    these records. Then, a new ``URLChangeRecord`` is created for the
    *instance*
    """
    new_url = getattr(instance, absolute_url_method)()

    # Don't save a record if the urls are equal, or if the url was previously
    # blank, or the object was just created.
    if not ((old_url == new_url) or old_url):
        return

    # If the new_url is blank, then delete all records for this object
    if not new_url:
        delete_urls(old_url)
        return

    logger.debug(
        "tracking URL change for instance '%s' URL",
        instance.__class__.__name__
    )

    # check if the new URL is already in the table and
    # remove these entries
    URLChangeRecord.objects.filter(old_url=new_url).delete()

    # updated existing records with the old URL being
    # the new URL in the record
    URLChangeRecord.objects.filter(new_url=old_url).update(
        new_url=new_url,
        deleted=False)

    # create a new/updated record for this combination of old and
    # new URL. If the record already exists, it is assumed that the
    # current change is to be used and the existing new_url will be
    # detached from the old_url.
    record, created = URLChangeRecord.objects.get_or_create(old_url=old_url)
    record.new_url = new_url
    record.deleted = False
    record.save()


def track_deleted_url(absolute_url_method, instance, **kwargs):
    """
    Track the URL of a deleted *instance*. It updates all existing
    records with ``new_url`` being set to the *instance*'s old URL and
    marks this record as deleted URL.

    A new ``URLChangeRecord`` is created for the old URL of *instance*
    that is marked as deleted.
    """
    logger.debug("tracking deleted instance '%s' URL", instance.__class__.__name__)
    old_url = getattr(instance, absolute_url_method)()
    if not old_url:
        return
    delete_urls(old_url)


def delete_urls(current_url):
    '''
    Updates all instances of ``URLChangeRecord`` with the *current_url* as
    their ``new_url`` are updated with their ``new_url`` being switched to
    their ``old_url`` and recorded as ``deleted``.
    '''
    URLChangeRecord.objects.filter(new_url=current_url).update(
        new_url='',
        deleted=True)
    record, created = URLChangeRecord.objects.get_or_create(
        old_url=current_url)
    record.deleted = True
    record.save()


def track_url_changes_for_model(model, absolute_url_method='get_absolute_url'):
    """
    Keep track of URL changes of the specified *model*. This will connect the
    *model*'s ``pre_save`` and ``post_delete`` signals to the
    tracking methods ``lookup_previous_url``
    and ``track_deleted_url`` respectively. URL changes will be logged in the
    ``URLChangeRecord`` table and are handled by the tracking middleware when
    a changed URL is called.
    """
    try:
        getattr(model, absolute_url_method)
    except AttributeError:
        raise URLTrackingError(
            "cannot track instance %s without method %s",
            model.__class__.__name__,
            absolute_url_method,
        )

    # Creates specialized functions that know the absolute_url_method
    # so that when the pre_save and post_save signals are called, they know
    # where to look to get the url
    lookup_previous_url_for_model = partial(lookup_previous_url, absolute_url_method)
    track_deleted_url_for_model = partial(track_deleted_url, absolute_url_method)
    signals.pre_save.connect(
        lookup_previous_url_for_model,
        sender=model,
        weak=False,
        dispatch_uid=get_dispatch_uid(absolute_url_method))
    signals.post_delete.connect(
        track_deleted_url_for_model,
        sender=model,
        weak=False,
        dispatch_uid=get_dispatch_uid(absolute_url_method))
