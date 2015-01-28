import os
import shutil
import sys
import tempfile

sys.path.insert(0, ".")
import unittest
from coalib.parsing.Glob import glob, _Selector


class GlobTest(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp(prefix='coala_import_test_dir_')
        self.tmp_subdir = tempfile.mkdtemp(prefix='pref', dir=self.tmp_dir)
        self.tmp_subdir2 = tempfile.mkdtemp(prefix='random', dir=self.tmp_subdir)
        self.tmp_subdir3 = tempfile.mkdtemp(prefix='random2', dir=self.tmp_subdir2)
        (self.testfile1, self.testfile1_path) = tempfile.mkstemp(suffix='.py', prefix='testfile1_', dir=self.tmp_subdir2)
        (self.testfile2, self.testfile2_path) = tempfile.mkstemp(suffix='.c', prefix='testfile2_', dir=self.tmp_subdir2)
        (self.testfile3, self.testfile3_path) = tempfile.mkstemp(suffix='.py', prefix='testfile3_', dir=self.tmp_subdir3)
        # We don't need the file opened
        os.close(self.testfile1)
        os.close(self.testfile2)
        os.close(self.testfile3)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_files(self):
        file_name_list = sorted(list(glob(os.path.join(self.tmp_dir, "pref*", "**", "*.py"), dirs=False)))
        self.assertEqual(file_name_list, sorted([self.testfile1_path, self.testfile3_path]))

    def test_dirs(self):
        dir_name_list = sorted(list(glob(os.path.join(self.tmp_dir, "**", "random*"), files=False)))
        self.assertEqual(dir_name_list, sorted([self.tmp_subdir2, self.tmp_subdir3]))

    def test_miss(self):
        dir_name_list = sorted(list(glob(os.path.join("*", "something", "that", "isnt", "there"))))
        self.assertEqual(dir_name_list, [])

    def test_none(self):
        dir_name_list = sorted(list(glob(os.path.join(self.tmp_dir, "**", "*"), files=False, dirs=False)))
        self.assertEqual(dir_name_list, [])

    def test_wrong_wildcard(self):
        with self.assertRaises(ValueError):
            a = list(glob(os.path.join("**", "a**b", "**")))

    def test_Selector_Error(self):
        with self.assertRaises(NotImplementedError):
            a = _Selector(False)
            b = a._collect("stuff")


if __name__ == '__main__':
    unittest.main(verbosity=2)
