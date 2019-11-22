import unittest
import artifacts

class artifacts_test_cases(unittest.TestCase):

    def test_explicit_artifact_init(self):

        artefact = artifacts.Artifact('one', version='2.2.1', os='qnx', description='very clever...')
        self.assertEqual(artefact.__str__(),
                         "one-qnx-2.2.1-snapshot")

        artefact = artifacts.Artifact('two', version='2.2.1', build_type='stable', os='qnx', description='very clever...')
        self.assertEqual(artefact,
                         "two-qnx-2.2.1")

        with self.assertRaises(Exception, msg="Wouaw is not a valid build type value"):
            artefact = artifacts.Artifact('two', version='2.2.1', build_type='Wouaw', os='qnx', description='very clever...')

    def test_description_string(self):

        artefact = artifacts.Artifact('common', version='2.2.1', os='qnx', description='very clever...')
        self.assertEqual("common / 2.2.1 (os: qnx, build type: snapshot): very clever...",
                         artefact.desc(),
                         msg="description string is not what we expected")

        artefact = artifacts.Artifact('artefact-name-qnx-1.2.3-SNAPSHOT', description='very clever snapshot version...')
        self.assertEqual("artefact-name / 1.2.3 (os: qnx, build type: snapshot): very clever snapshot version...",
                         artefact.desc(),
                         msg="description string is not what we expected")

    def test_parse_artifact_description_string_init(self):
        artifact = artifacts.Artifact('one-1.2.3')
        self.assertEqual("one-1.2.3",
                         artifact.id(),
                         msg="pattern 'one-1.2.3' init failed")

        artifact = artifacts.Artifact('two-qnx-1.2.3')
        self.assertEqual(artifact,
                         "two-qnx-1.2.3",
                         msg="pattern 'two-qnx-1.2.3' init failed")

        artifact = artifacts.Artifact('three-1.2.3-snapshot')
        self.assertEqual(artifact,
                         "three-1.2.3-snapshot",
                         msg="pattern 'three-1.2.3-snapshot' init failed")

        artifact = artifacts.Artifact('five-qnx-1.2.3-SNAPSHOT')
        self.assertEqual(artifact,
                         "five-qnx-1.2.3-snapshot",
                         msg="pattern 'five-qnx-1.2.3-SNAPSHOT' init failed")

        with self.assertRaises(Exception, msg="pattern 'six-qnx-1.2.3-Wouaw' should not be accpeted"):
            artifacts.Artifact('six-qnx-1.2.3-Wouaw')

        artifact = artifacts.Artifact('seven-qnx-1.2.3', build_type='stable')
        self.assertEqual(artifact,
                         "seven-qnx-1.2.3",
                         msg="pattern 'seven-1.2.3-snapshot' plus attribute build_type='stable' init failed")


if __name__ == '__main__':
    unittest.main()
