from omg.cmd.get_main import generate_completions

import unittest


class TestGetCompletion(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testTypeCompletion(self):
        expected = ["service"]
        results = generate_completions(None, (), "servi")
        self.assertEqual(expected, results)

    def testNoTypeCompletion(self):
        expected = []
        results = generate_completions(None, (), "asdf")
        self.assertEqual(expected, results)

    def testMultiTypeComma(self):
        expected = []
        results = generate_completions(None, (), "pods,services,endpoi")
        self.assertEqual(expected, results)

    def testNoRaise(self):
        expected = []
        results = generate_completions(None, None, None)
        self.assertEqual(expected, results)

        results = generate_completions(None, ("12312323",), "1231231231231")  # Bogus input
        self.assertEqual(expected, results)
