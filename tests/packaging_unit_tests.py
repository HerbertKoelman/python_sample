import unittest
import utils

class packaging_test_cases(unittest.TestCase):

    def test_packaging_archive_digest(self):
        package = utils.Package(utils.Artifact('common-qnx-1.2.3'), 'x86')
        self.assertEqual(package.archive_digest(),
                         "common-qnx-1.2.3-x86.tar.gz.md5",
                         msg="wrong packaging archive digest name for artefact '{}'".format(package))

        package.target_arch('armv7')
        self.assertEqual(package.archive_digest(),
                         "common-qnx-1.2.3-armv7.tar.gz.md5",
                         msg="wrong packaging archive digest name for artefact '{}'".format(package))

    def test_packaging_archive(self):
        package = utils.Package(utils.Artifact('common-qnx-1.2.3'), 'x86')
        self.assertEqual(package.archive(),
                         "common-qnx-1.2.3-x86.tar.gz",
                         msg="wrong packaging archive name for package \n{}".format(package))

        package.target_arch('armv7')
        self.assertEqual(package.archive(),
                         "common-qnx-1.2.3-armv7.tar.gz",
                         msg="wrong packaging archive name for package \n{}".format(package))

if __name__ == '__main__':
    unittest.main()
