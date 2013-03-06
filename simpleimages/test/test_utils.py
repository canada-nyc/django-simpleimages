from django.utils import unittest

from simpleimages import utils


class FilenameAppendTest(unittest.TestCase):
    def test_normal(self):
        '''
        Makes sure it appends correctly to a file path
        '''
        old_path = 'path/img.ending'
        appender = utils.append_to_filename('_large')
        new_path = appender(old_path)

        self.assertEqual('path/img_large.ending', new_path)
