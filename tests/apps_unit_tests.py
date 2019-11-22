import glob
import os
import shutil
import sys
import tempfile
import unittest

import artifacts
import artifacts.copy_artifacts_app
import artifacts.deploy_artifacts_app


class apps_test_cases(unittest.TestCase):

    def setUp(self):
        self.workspace = tempfile.mkdtemp()
        self.repository = tempfile.mkdtemp()
        search_path = [self.repository, '/tmp','/your/home']
        artifacts.package_search_pathes(search_path)

    def tearDown(self):
        shutil.rmtree(self.workspace, ignore_errors=True)
        shutil.rmtree(self.repository, ignore_errors=True)

    def test_version_identification(self):
        if hasattr(artifacts,'__version__'):
            print(artifacts.__version__)
        else:
            self.fail('No artifacts has no __version__ attribute ')

    def test_deploy_app_help(self):
        with self.assertRaises(SystemExit):
            sys.argv = [
                "{}.deploy_app_test".format(__name__),
                '-h'
            ]

            artifacts.deploy_artifacts_app.main()

    def test_deploy_app(self):
        self.test_copy_app()
        sys.argv = [
            "{}.deploy_app_test".format(__name__),
            '--packages-home', self.repository,
            '--target-arch', 'x86',
            '--install-dir', self.workspace,
            'tests/dependencies.yml'
        ]
        artifacts.deploy_artifacts_app.main()

    def test_copy_app_help(self):
        with self.assertRaises(SystemExit):
            sys.argv = [
                "{}.copy_app_test".format(__name__),
                '-h'
            ]
            artifacts.copy_artifacts_app.main()

    def test_copy_app(self):
        sys.argv = [
            "{}.copy_app_test".format(__name__),
            'tests/fixtures/', 'tests/fixtures/artifact-qnx-2.3.4-snapshot-x86.tar.gz','tests/fixtures/cpp-pthread-Darwin-1.11.0-x86.tar.gz',
            self.repository
        ]
        artifacts.copy_artifacts_app.main()
        archives = glob.glob(os.path.join(self.repository, '*.tar.gz'))
        self.assertEqual(2, len(archives))

    def test_copy_app_with_package_arg(self):
        sys.argv = [
            "{}.copy_app_test".format(__name__),
            '--packages-home', self.repository,
            'tests/fixtures/', 'tests/fixtures/artifact-qnx-2.3.4-snapshot-x86.tar.gz','tests/fixtures/cpp-pthread-Darwin-1.11.0-x86.tar.gz',
        ]
        artifacts.copy_artifacts_app.main()
        archives = glob.glob(os.path.join(self.repository, '*.tar.gz'))
        self.assertEqual(2, len(archives))

if __name__ == '__main__':
    unittest.main()
