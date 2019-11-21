import unittest
import artifacts

class requirements_test_cases(unittest.TestCase):
    def test_load_from_yaml_file(self):
        path_to_yaml_files = ['tests/dependencies.yml', 'tests/dependencies-dict.yml']

        expected_values = ['ipcm-api-qnx-1.42.0-armv7', 'common-qnx-2.0.1-armv7', 'my-lib-qnx-2.0.1-snapshot-armv7']

        for path_to_yaml_file in path_to_yaml_files:
            requirements = artifacts.load_requirements_from(path_to_yaml_file)

            self.assertIsNotNone(requirements, msg="failed to load requirements from file '{}'".format(path_to_yaml_file))
            self.assertEqual(2, len(requirements), msg="unexpected number requirements found in '{}'".format(path_to_yaml_file))

            for artefact in requirements:
                package = artifacts.Package(artefact, 'armv7')
                # DEBUG print ("{}: {}".format(__name__, package.id()))
                self.assertTrue(package.id() in expected_values,
                                "Expect {} found in {} to be in {}".format(
                                    package.id(),
                                    path_to_yaml_file,
                                    expected_values))

    def test_load_from_text_file(self):
        path_to_text_file = 'tests/dependencies.txt'
        expected_values= ['ipcm-api-qnx-1.42.0-armv7','common-qnx-2.0.1-armv7','cpp-pthread-Darwin-1.11.0-armv7']

        requirements = artifacts.load_requirements_from(path_to_text_file)

        self.assertIsNotNone(requirements, msg="failed to load requirements from file '{}'".format(path_to_text_file))
        self.assertEqual(len(requirements), 3, msg="unexpected number requirments found in '{}'".format(path_to_text_file))

        for artefact in requirements:
            package = artifacts.Package(artefact, 'armv7')
            # DEBUG  print ("{}: {}".format(__name__, package.id()))
            self.assertTrue(package.id() in expected_values,
                            "Expect {} found in {} to be in {}".format(
                                package.id(),
                                path_to_text_file,
                                expected_values))


if __name__ == '__main__':
    unittest.main()
