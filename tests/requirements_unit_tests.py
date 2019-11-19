import unittest
import artifacts

class requirements_test_cases(unittest.TestCase):
    def test_load_from_yaml_file(self):
        path_to_yaml_file = 'tests/sample.yml'

        requirements = artifacts.load_requirements_from(path_to_yaml_file)

        self.assertIsNotNone(requirements, msg="failed to load requirements from file '{}'".format(path_to_yaml_file))
        self.assertEqual(len(requirements), 7, msg="unexpected number requirments found in '{}'".format(path_to_yaml_file))

        for artefact in requirements:
            print (artifacts.Package(artefact, 'armv7').archive())

    def test_load_from_text_file(self):
        path_to_text_file = 'tests/dependencies.yml'

        requirements = artifacts.load_requirements_from(path_to_text_file)

        self.assertIsNotNone(requirements, msg="failed to load requirements from file '{}'".format(path_to_text_file))
        self.assertEqual(len(requirements), 2, msg="unexpected number requirments found in '{}'".format(path_to_text_file))

        for artefact in requirements:
            print (artifacts.Package(artefact, 'armv7').archive())

if __name__ == '__main__':
    unittest.main()
