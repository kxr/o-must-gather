import unittest

from omg.cmd.get.complete_get import generate_completions


class TestGetCompletion(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testTypeCompletion(self):
        expected = ['service']
        results = generate_completions((), "servi", None)
        self.assertEqual(expected, results)

    def testNoTypeCompletion(self):
        expected = []
        results = generate_completions((), "asdf", None)
        self.assertEqual(expected, results)

    def testMultiTypeComma(self):
        expected = []
        results = generate_completions((), "pods,services,endpoi", None)
        self.assertEqual(expected, results)
