import unittest

from omg.cmd.get import parse


class TestGetParse(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testAllTypes(self):
        args = ("all",)
        rl = parse.ResourceList(args)

        for expected_type in parse.ALL_TYPES:
            self.assertIn(expected_type, rl)

        for _, n in rl:
            self.assertEqual({parse.ALL_RESOURCES}, n)

    def testAllResource(self):
        args = ("pods",)
        rl = parse.ResourceList(args)
        r_type, r_name = next(rl)
        self.assertEqual(1, len(rl))
        self.assertEqual("pod", r_type)
        self.assertEqual({parse.ALL_RESOURCES}, r_name)

    def testSingleResource(self):
        args = ("pod", "mypod")
        rl = parse.ResourceList(args)
        r_type, r_name = next(rl)
        self.assertEqual(1, len(rl))
        self.assertEqual("pod", r_type)
        self.assertEqual({"mypod"}, r_name)

    def testSingleTypeMultiResource(self):
        args = ("pod", "mypod", "myotherpod")
        rl = parse.ResourceList(args)
        r_type, r_name = next(rl)
        self.assertEqual(1, len(rl))
        self.assertEqual("pod", r_type)
        self.assertEqual({"mypod", "myotherpod"}, r_name)

    def testMultipleResources(self):
        expected_args = ["endpoint", "service", "pod"]
        args = ("pods,svc,endpoints",)
        rl = parse.ResourceList(args)
        for r_type, r_name in rl:
            expected = expected_args.pop()
            self.assertEqual(expected, r_type)
            self.assertEqual({parse.ALL_RESOURCES}, r_name)

    def testMultipleResourcesOneName(self):
        expected_args = ["endpoint", "service"]
        args = ("svc,endpoints", "dns-default")
        rl = parse.ResourceList(args)
        for r_type, r_name in rl:
            expected = expected_args.pop()
            self.assertEqual(expected, r_type)
            self.assertEqual({"dns-default"}, r_name)

    def testSingleSlash(self):
        args = ("pods/mypod",)
        rl = parse.ResourceList(args)
        r_type, r_name = next(rl)
        self.assertEqual(1, len(rl))
        self.assertEqual("pod", r_type)
        self.assertEqual({"mypod"}, r_name)

    def testMultiSlash(self):
        args = ("pods/mypod", "svc/default")
        rl = parse.ResourceList(args)
        self.assertEqual(2, len(rl))

        r_type, r_name = next(rl)
        self.assertEqual("pod", r_type)
        self.assertEqual({"mypod"}, r_name)

        r_type, r_name = next(rl)
        self.assertEqual("service", r_type)
        self.assertEqual({"default"}, r_name)

    def testInvalidType(self):
        args = ("podzzzz",)
        with self.assertRaises(parse.ResourceParseError):
            parse.ResourceList(args)

    def testInvalidMultiTypeComma(self):
        args = ("pods,svc,asdf",)
        with self.assertRaises(parse.ResourceParseError):
            parse.ResourceList(args)

    def testInvalidMultiTypeMultiResource(self):
        args = ("pods/mypod", "svc/myservice", "blarg/bad")
        with self.assertRaises(parse.ResourceParseError):
            parse.ResourceList(args)


if __name__ == "__main__":
    unittest.main()
