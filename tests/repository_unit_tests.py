import unittest
import artifacts
import tempfile
import shutil

class repository_test_cases(unittest.TestCase):

    def setUp(self):
        self.workspace = tempfile.mkdtemp()
        self.repository = tempfile.mkdtemp()
        search_path = [self.repository, '/tmp','/your/home']
        artifacts.package_search_pathes(search_path)

    def tearDown(self):
        shutil.rmtree(self.workspace, ignore_errors=True)
        shutil.rmtree(self.repository, ignore_errors=True)

    def test_change_search_path(self):
        search_path = ['/tmp','/your/home']
        artifacts.package_search_pathes(search_path)

        self.assertEqual(2, len(artifacts.PACKAGES_HOME_PATH))
        self.assertTrue('/tmp'       in artifacts.PACKAGES_HOME_PATH, "'/tmp' not in path")
        self.assertTrue('/your/home' in artifacts.PACKAGES_HOME_PATH, "'/your/home' not in path")

    def test_install_package(self):
        self.test_copy_stable_package()
        artifacts.install_package(artifacts.Artifact('cpp-pthread-Darwin-1.11.0'), 'x86', self.workspace)
        artifacts.install_package(artifacts.Artifact('cpp-pthread-Darwin-1.11.0'), 'x86', self.workspace)
        artifacts.install_package(artifacts.Artifact('cpp-pthread-Darwin-1.11.0'), 'x86', self.workspace)

    def test_copy_stable_package(self):
        self.assertTrue(artifacts.copy_package('tests/fixtures/cpp-pthread-Darwin-1.11.0-x86.tar.gz', self.repository))
        self.assertFalse(artifacts.copy_package('tests/fixtures/cpp-pthread-Darwin-1.11.0-x86.tar.gz', self.repository))
        self.assertFalse(artifacts.copy_package('tests/fixtures/cpp-pthread-Darwin-1.11.0-x86.tar.gz', self.repository))

    def test_copy_snapshot_package(self):
        self.assertTrue(artifacts.copy_package('tests/fixtures/artifact-qnx-2.3.4-snapshot-x86.tar.gz', self.repository))
        self.assertTrue(artifacts.copy_package('tests/fixtures/artifact-qnx-2.3.4-snapshot-x86.tar.gz', self.repository))

if __name__ == '__main__':
    unittest.main()
