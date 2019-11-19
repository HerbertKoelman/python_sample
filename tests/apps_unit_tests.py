import unittest
import artifacts
import artifacts.deploy_artifacts_app
import artifacts.copy_artifacts_app
import tempfile
import shutil

class deploy_app_test_cases(unittest.TestCase):

    def setUp(self):
        self.workspace = tempfile.mkdtemp()
        self.repository = tempfile.mkdtemp()
        search_path = [self.repository, '/tmp','/your/home']
        artifacts.package_search_pathes(search_path)

    def tearDown(self):
        shutil.rmtree(self.workspace, ignore_errors=True)
        shutil.rmtree(self.repository, ignore_errors=True)

    def test_deploy_app(self):
        with self.assertRaises(SystemExit):
            artifacts.deploy_artifacts_app.main()

    def test_copy_app(self):
        with self.assertRaises(SystemExit):
            artifacts.copy_artifacts_app.main()

if __name__ == '__main__':
    unittest.main()
