"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from mock import Mock

from django.test import TestCase
from django.db.models import signals

import url_tracker
from url_tracker.models import URLChangeRecord


class TestTracking(TestCase):

    def setUp(self):
        class DoesNotExist(BaseException):
            pass

        self.model_mock = Mock

        self.tracked_model = self.model_mock(name='TrackedModel')
        self.model_mock.get_absolute_url = lambda self: 'old/url'

        def raise_exception(*args, **kwargs):
            raise self.tracked_model.__class__.DoesNotExist

        class_objects = Mock(name="MockModelManager")
        class_objects.get = raise_exception

        self.tracked_model.__class__.objects = class_objects
        self.tracked_model.__class__.DoesNotExist = DoesNotExist

        self.tracked_db_model = self.model_mock(name='TrackeDatabaseModel')

        self.old_url = 'old/url'
        self.oldest_url = 'oldest/url'
        self.new_url = 'new/url'

        def dispatch_uid(absolute_url_method='get_absolute_url'):
            return 'urltracker.track_url_changes_for_model.' + absolute_url_method

        self.dispatch_uid = dispatch_uid

    def tearDown(self):
        signals.post_delete.receivers = signals.post_save.receivers = signals.pre_save.receivers = []

    def test_tracking_model_without_url_method(self):

        class EmptyModel(object):
            pass

        self.assertRaises(
            url_tracker.URLTrackingError,
            url_tracker.track_url_changes_for_model,
            EmptyModel(),
        )

    def test__lookup_url_with_new_instance(self):
        url_tracker.track_url_changes_for_model(Mock)
        url_tracker.lookup_previous_url(
            'get_absolute_url',
            self.tracked_model)

        post_save_function = signals.post_save.receivers[0][1]
        post_save_old_url = post_save_function.keywords['old_url']
        self.assertEquals(post_save_old_url, None)

    def test_lookup_url_with_existing_instance(self):
        def return_instance(pk):
            return self.tracked_db_model

        class_objects = Mock(name='MockModelManager')
        class_objects.get = return_instance
        self.tracked_model.__class__.objects = class_objects

        url_tracker.lookup_previous_url(
            'get_absolute_url',
            self.tracked_model)

        post_save_function = signals.post_save.receivers[0][1]
        post_save_old_url = post_save_function.keywords['old_url']

        self.assertEqual(post_save_old_url, self.old_url)

    def test_loopup_url_with_existing_instance_with_multiple_urls(self):
        def return_instance(pk):
            return self.tracked_db_model

        class_objects = Mock(name='MockModelManager')
        class_objects.get = return_instance
        self.tracked_model.__class__.objects = class_objects
        old_url1 = self.old_url + '1'
        old_url2 = self.old_url + '2'
        self.model_mock.get_absolute_url = lambda self: old_url1
        self.model_mock.get_absolute_url2 = lambda self: old_url2

        url_tracker.lookup_previous_url(
            'get_absolute_url',
            self.tracked_model)
        url_tracker.lookup_previous_url(
            'get_absolute_url2',
            self.tracked_model)

        post_save_function1 = signals.post_save.receivers[0][1]
        post_save_old_url1 = post_save_function1.keywords['old_url']
        self.assertEqual(post_save_old_url1, old_url1)

        post_save_function2 = signals.post_save.receivers[1][1]
        post_save_old_url2 = post_save_function2.keywords['old_url']
        self.assertEqual(post_save_old_url2, old_url2)

    def test_track_changed_url_with_new_instance(self):
        instance = self.tracked_model
        instance.get_absolute_url = lambda: self.old_url

        url_tracker.track_changed_url(
            old_url=None,
            absolute_url_method='get_absolute_url',
            instance=instance,
            signal_dispatch_uid=self.dispatch_uid()
        )
        self.assertEquals(URLChangeRecord.objects.count(), 0)

    def test_track_changed_url_without_existing_records(self):
        instance = self.tracked_model
        instance.get_absolute_url = lambda: self.new_url

        url_tracker.track_changed_url(
            old_url='old/url',
            absolute_url_method='get_absolute_url',
            instance=instance,
            signal_dispatch_uid=self.dispatch_uid())

        self.assertEquals(URLChangeRecord.objects.count(), 1)
        record = URLChangeRecord.objects.all()[0]
        self.assertEquals(record.new_url, self.new_url)
        self.assertEquals(record.old_url, self.old_url)
        self.assertEquals(record.deleted, False)

    def test_track_changed_url_with_existing_records(self):
        URLChangeRecord.objects.create(
            old_url=self.oldest_url,
            new_url=self.old_url)

        instance = self.tracked_model
        instance.get_absolute_url = lambda: self.new_url

        url_tracker.track_changed_url(
            old_url=self.old_url,
            absolute_url_method='get_absolute_url',
            instance=instance,
            signal_dispatch_uid=self.dispatch_uid()
        )
        self.assertEquals(URLChangeRecord.objects.count(), 2)
        record = URLChangeRecord.objects.get(pk=1)
        self.assertEquals(record.old_url, self.oldest_url)
        self.assertEquals(record.new_url, self.new_url)
        self.assertEquals(record.deleted, False)
        record = URLChangeRecord.objects.get(pk=2)
        self.assertEquals(record.old_url, self.old_url)
        self.assertEquals(record.new_url, self.new_url)
        self.assertEquals(record.deleted, False)

    def test_track_changed_url_with_existing_records_and_old_url(self):
        URLChangeRecord.objects.create(
            old_url=self.oldest_url,
            new_url=self.old_url)
        URLChangeRecord.objects.create(
            old_url=self.old_url,
            new_url=self.new_url)

        instance = self.tracked_model
        instance.get_absolute_url = lambda: self.new_url

        url_tracker.track_changed_url(
            old_url=self.old_url,
            absolute_url_method='get_absolute_url',
            instance=instance,
            signal_dispatch_uid=self.dispatch_uid()
        )

        self.assertEquals(URLChangeRecord.objects.count(), 2)
        record = URLChangeRecord.objects.get(pk=1)
        self.assertEquals(record.old_url, self.oldest_url)
        self.assertEquals(record.new_url, self.new_url)
        self.assertEquals(record.deleted, False)
        record = URLChangeRecord.objects.get(pk=2)
        self.assertEquals(record.old_url, self.old_url)
        self.assertEquals(record.new_url, self.new_url)
        self.assertEquals(record.deleted, False)

    def test_track_changed_url_with_existing_deleted_record(self):
        URLChangeRecord.objects.create(old_url=self.oldest_url,
                                       new_url=self.old_url,
                                       deleted=True)

        instance = self.tracked_model
        instance.get_absolute_url = lambda: self.new_url

        url_tracker.track_changed_url(
            old_url=self.old_url,
            absolute_url_method='get_absolute_url',
            instance=instance,
            signal_dispatch_uid=self.dispatch_uid()
        )
        record = URLChangeRecord.objects.get(pk=2)
        self.assertEquals(record.old_url, self.old_url)
        self.assertEquals(record.new_url, self.new_url)
        self.assertEquals(record.deleted, False)

    def test_track_changed_url_with_existing_records_and_no_new_url(self):
        URLChangeRecord.objects.create(
            old_url=self.oldest_url,
            new_url=self.old_url)

        instance = self.tracked_model
        instance.get_absolute_url = lambda: ''

        url_tracker.track_changed_url(
            old_url=self.old_url,
            absolute_url_method='get_absolute_url',
            instance=instance,
            signal_dispatch_uid=self.dispatch_uid()
        )
        self.assertEquals(URLChangeRecord.objects.count(), 2)
        record = URLChangeRecord.objects.get(pk=1)
        self.assertEquals(record.old_url, self.oldest_url)
        self.assertFalse(record.new_url)
        self.assertEquals(record.deleted, True)
        record = URLChangeRecord.objects.get(pk=2)
        self.assertEquals(record.old_url, self.old_url)
        self.assertFalse(record.new_url)
        self.assertEquals(record.deleted, True)

    def test_track_deleted_url_without_existing_records(self):
        instance = self.tracked_model
        instance.get_absolute_url = lambda: self.new_url

        url_tracker.track_deleted_url(
            absolute_url_method='get_absolute_url',
            instance=instance
        )

        self.assertEquals(URLChangeRecord.objects.count(), 1)
        record = URLChangeRecord.objects.all()[0]
        self.assertEquals(record.new_url, None)
        self.assertEquals(record.old_url, self.new_url)
        self.assertEquals(record.deleted, True)


class TestUrlRecord(TestCase):

    def test_invalid_url(self):
        response = self.client.get('/work/an-invalid-project/')
        self.assertEquals(response.status_code, 404)

    def test_changed_url(self):
        URLChangeRecord.objects.create(
            old_url='/the/old-url/',
            new_url='/the/new/url/',
        )

        response = self.client.get('/the/old-url/')
        self.assertEquals(response.status_code, 301)
        self.assertEquals(response['location'], 'http://testserver/the/new/url/')

    def test_deleted_url(self):
        URLChangeRecord.objects.create(
            old_url='/the/old-url/',
            new_url='',
            deleted=True
        )

        response = self.client.get('/the/old-url/')
        self.assertEquals(response.status_code, 410)

    def test_redirecting_from_a_url_with_get_parameters(self):
        old_url = '/the/old-url/afile.php?q=test&another=45'
        URLChangeRecord.objects.create(
            old_url=old_url,
            new_url='/the/new/url/',
        )

        response = self.client.get(old_url)
        self.assertEquals(response.status_code, 301)
