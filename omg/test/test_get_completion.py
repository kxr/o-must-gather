# -*- coding: utf-8 -*-
import unittest

from omg.cmd.get.complete_get import generate_completions


class TestGetCompletion(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testTypeCompletion(self):
        expected = ["service"]
        results = generate_completions((), "servi", None)
        self.assertEqual(expected, results)
        
    def testTypeCompletion(self):
        expected = ["servicemeshcontrolplane"]
        results = generate_completions((), "servicemeshc", None)
        self.assertEqual(expected, results)
        
    def testTypeCompletion(self):
        expected = ["servicemeshmemberroll"]
        results = generate_completions((), "servicemeshm", None)
        self.assertEqual(expected, results)
        
    def testTypeCompletion(self):
        expected = ["serviceentry"]
        results = generate_completions((), "serviceen", None)
        self.assertEqual(expected, results)

    def testNoTypeCompletion(self):
        expected = []
        results = generate_completions((), "asdf", None)
        self.assertEqual(expected, results)

    def testMultiTypeComma(self):
        expected = []
        results = generate_completions((), "pods,services,endpoi", None)
        self.assertEqual(expected, results)
