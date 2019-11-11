import unittest
import utils

class artifacts_test_cases(unittest.TestCase):

    def test_explicit_artifact_init(self):

        artefact = utils.Artifact('common', version='2.2.1')
        self.assertEqual(artefact.__str__(),
                         "common (version: 2.2.1, os: None, arch: x86_64, build type: stable)",
                         msg="common init failed")

    def test_parse_artifact_description_string_init(self):
        artefact = utils.Artifact('common-1.2.3')
        self.assertEqual(artefact.__str__(),
                         "common (version: 1.2.3, os: None, arch: x86_64, build type: stable)",
                         msg="pattern 'common-1.2.3' init failed")
        self.assertEqual(artefact.id(),"common-1.2.3-x86_64", msg="pattern 'common-1.2.3' returns a wrong artifact ID")

        artefact = utils.Artifact('common-qnx-1.2.3')
        self.assertEqual(artefact.__str__(),
                         "common (version: 1.2.3, os: qnx, arch: x86_64, build type: stable)",
                         msg="pattern 'common-qnx-1.2.3' init failed")
        self.assertEqual(artefact.id(), "common-qnx-1.2.3-x86_64", msg="pattern 'common-qnx-1.2.3' returns a wrong artifact ID")

        artefact = utils.Artifact('common-1.2.3-snapshot')
        self.assertEqual(artefact.__str__(),
                         "common (version: 1.2.3, os: None, arch: x86_64, build type: snapshot)",
                         msg="pattern 'common-1.2.3-snapshot' init failed")
        self.assertEqual(artefact.id(), "common-1.2.3-snapshot-x86_64", msg="pattern 'common-1.2.3-snapshot' returns a wrong artifact ID")

        artefact = utils.Artifact('common-qnx-1.2.3-SNAPSHOT')
        self.assertEqual(artefact.__str__(),
                         "common (version: 1.2.3, os: qnx, arch: x86_64, build type: snapshot)",
                         msg="pattern 'common-qnx-1.2.3-SNAPSHOT' init failed")

        with self.assertRaises(Exception, msg="pattern 'common-qnx-1.2.3-Wouaw' should not be accpeted"):
            utils.Artifact('common-qnx-1.2.3-Wouaw')

        artefact = utils.Artifact('common-qnx-1.2.3', build_type='stable')
        self.assertEqual(artefact.__str__(),
                         "common (version: 1.2.3, os: qnx, arch: x86_64, build type: stable)",
                         msg="pattern 'common-1.2.3-snapshot' plus attribute build_type='stable' init failed")

    def test_artefact_packaging(self):
        artefact = utils.Artifact('common-qnx-1.2.3')
        print("Artifact 'common-qnx-1.2.3': ", artefact )
        self.assertEqual(artefact.package.archive(),
                         "common-qnx-1.2.3-x86_64.tar.gz",
                         msg="artefact '{}' packaging name is not the one expected".format(artefact))

        artefact = utils.Artifact('common', os = 'qnx', version='1.2.3', description='does common things..."')
        self.assertEqual(artefact.package.archive(),
                         "common-qnx-1.2.3-x86_64.tar.gz",
                         msg="artefact '{}' packaging name is not the one expected".format(artefact))

    def test_artefact_change_attr(self):
        artefact = utils.Artifact('common-qnx-1.2.3-SNAPSHOT')
        artefact.target_arch = 'x86'

        self.assertEqual("common-qnx-1.2.3-snapshot-x86", artefact.id(),
                         msg="Changing attr target_arch to 'x86' for 'common-qnx-1.2.3-SNAPSHOT' failed")

        self.assertEqual("common-qnx-1.2.3-snapshot-x86.tar.gz", artefact.package.archive(),
                         msg="Changing attr target_arch to 'x86' for 'common-qnx-1.2.3-SNAPSHOT' failed to change archive name")



if __name__ == '__main__':
    unittest.main()
