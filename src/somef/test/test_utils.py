import unittest

from somef.test.utils_for_tests import almost_equal

class TestAlmostEqual(unittest.TestCase):

    def test_basic(self):

        a = {
            'b': [5, 7],
            'a': 1
        }

        b = {
            'a': 1,
            'b': [5, 7]
        }

        self.assertTrue(almost_equal(a, b))

    def test_false(self):
        a = {
            'b': [5, 6],
            'a': 1
        }

        b = {
            'a': 1,
            'b': [5, 7]
        }

        self.assertFalse(almost_equal(a, b))

    def test_with_exclusion(self):

        a = {
            "use": "use",
            "no": "no"
        }

        b = {
            "use": "use",
            "no": "yes"
        }

        self.assertFalse(almost_equal(a, b))
        self.assertTrue(almost_equal(a, b, exclude_paths=[["no"]]))

        # more layers

        a2 = [a, b, a, b]
        b2 = [b, a, a, b]

        self.assertFalse(almost_equal(a2, b2))
        self.assertTrue(almost_equal(a2, b2, exclude_paths=[["no"]]))

        a3 = {
            "yes": a2,
            "no": 0
        }

        b3 = {
            "yes": b2,
            "no": 1
        }

        self.assertFalse(almost_equal(a3, b3))
        self.assertFalse(almost_equal(a3, b3, exclude_paths=[["no"]]))
        self.assertFalse(almost_equal(a3, b3, exclude_paths=[["yes", "no"]]))
        self.assertTrue(almost_equal(a3, b3, exclude_paths=[["no"], ["yes", "no"]]))

    def test_different_array_len(self):
        a = [1, 2]
        b = [1, 2, 3]

        self.assertFalse(almost_equal(a, b))
        self.assertFalse(almost_equal(b, a))

    def test_different_keys(self):
        a = {}
        b = {"hi": "hi"}

        self.assertFalse(almost_equal(a, b))
        self.assertFalse(almost_equal(b, a))