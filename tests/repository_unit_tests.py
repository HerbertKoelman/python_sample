import unittest
import artifacts

class repository_test_cases(unittest.TestCase):
    def test_change_search_path(self):
        search_path = ['/tmp','/your/home']
        artifacts.package_search_pathes(search_path)

        self.assertTrue('/tmp'       in artifacts.PACKAGES_HOME_PATH, "'/tmp' not in path")
        self.assertTrue('/your/home' in artifacts.PACKAGES_HOME_PATH, "'/your/home' not in path")

if __name__ == '__main__':
    unittest.main()
