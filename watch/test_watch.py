from watch.watch import Watch

from unittest import TestCase
from unittest.mock import patch


@patch("watch.watch.all_files")
class TestWatch(TestCase):
    def test_created(self, mock_all_files):
        mock_all_files.return_value = {}
        watch = Watch()
        with self.subTest(msg="before create"):
            self.assertEqual(watch.created, [])

        mock_all_files.return_value = {"foo.txt": 1}
        with self.subTest(msg="after create"):
            self.assertEqual(watch.created, ["foo.txt"])

        watch.ack()
        with self.subTest(msg="after ack"):
            self.assertEqual(watch.created, [])

    def test_modified(self, mock_all_files):
        mock_all_files.return_value = {"foo.txt": 1}
        watch = Watch()
        with self.subTest(msg="before modify"):
            self.assertEqual(watch.modified, [])

        mock_all_files.return_value = {"foo.txt": 2}
        with self.subTest(msg="after modify"):
            self.assertEqual(watch.modified, ["foo.txt"])

        watch.ack()
        with self.subTest(msg="after ack"):
            self.assertEqual(watch.modified, [])

    def test_removed(self, mock_all_files):
        mock_all_files.return_value = {"foo.txt": 1}
        watch = Watch()
        with self.subTest(msg="before remove"):
            self.assertEqual(watch.removed, [])

        mock_all_files.return_value = {}
        with self.subTest(msg="after remove"):
            self.assertEqual(watch.removed, ["foo.txt"])

        watch.ack()
        with self.subTest(msg="after ack"):
            self.assertEqual(watch.removed, [])
