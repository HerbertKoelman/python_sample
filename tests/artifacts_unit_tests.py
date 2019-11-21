import unittest
import artifacts

class artifacts_test_cases(unittest.TestCase):

    def test_explicit_artifact_init(self):

        artefact = artifacts.Artifact('common', version='2.2.1')
        self.assertEqual(artefact.__str__(),
                         "common-2.2.1",
                         msg="common init failed")

    def test_description_string(self):

        artefact = artifacts.Artifact('common', version='2.2.1', os='qnx', description='very clever...')
        self.assertEqual("common / 2.2.1 (os: qnx, build type: stable): very clever...",
                         artefact.desc(),
                         msg="description string is not what we expected")

        artefact = artifacts.Artifact('artefact-name-qnx-1.2.3-SNAPSHOT', description='very clever snapshot version...')
        self.assertEqual("artefact-name / 1.2.3 (os: qnx, build type: snapshot): very clever snapshot version...",
                         artefact.desc(),
                         msg="description string is not what we expected")

    def test_parse_artifact_description_string_init(self):
        artefact = artifacts.Artifact('common-1.2.3')
        self.assertEqual(artefact.__str__(),
                         "common-1.2.3",
                         msg="pattern 'common-1.2.3' init failed")
        self.assertEqual(artefact.id(),"common-1.2.3", msg="pattern 'common-1.2.3' returns a wrong artifact ID")

        artefact = artifacts.Artifact('common-qnx-1.2.3')
        self.assertEqual(artefact.__str__(),
                         "common-qnx-1.2.3",
                         msg="pattern 'common-qnx-1.2.3' init failed")
        self.assertEqual(artefact.id(), "common-qnx-1.2.3", msg="pattern 'common-qnx-1.2.3' returns a wrong artifact ID")

        artefact = artifacts.Artifact('common-1.2.3-snapshot')
        self.assertEqual(artefact.__str__(),
                         "common-1.2.3-snapshot",
                         msg="pattern 'common-1.2.3-snapshot' init failed")

        self.assertEqual(artefact.id(),
                         "common-1.2.3-snapshot",
                         msg="pattern 'common-1.2.3-snapshot' returns a wrong artifact ID")

        artefact = artifacts.Artifact('common-qnx-1.2.3-SNAPSHOT')
        self.assertEqual(artefact.__str__(),
                         "common-qnx-1.2.3-snapshot",
                         msg="pattern 'common-qnx-1.2.3-SNAPSHOT' init failed")

        with self.assertRaises(Exception, msg="pattern 'common-qnx-1.2.3-Wouaw' should not be accpeted"):
            artifacts.Artifact('common-qnx-1.2.3-Wouaw')

        artefact = artifacts.Artifact('common-qnx-1.2.3', build_type='stable')
        self.assertEqual(artefact.__str__(),
                         "common-qnx-1.2.3",
                         msg="pattern 'common-1.2.3-snapshot' plus attribute build_type='stable' init failed")


if __name__ == '__main__':
    unittest.main()
