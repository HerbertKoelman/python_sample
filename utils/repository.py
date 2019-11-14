import hashlib
import os
import tarfile
import utils
import shutil

# singleton
PACKAGES_HOME_PATH = os.getenv('PACKAGES_HOME_PATH', '/share/modules').split(':')

def install_package(requirement, arch, here):
    package = utils.Package(requirement, arch)

    for packages_home in PACKAGES_HOME_PATH:
        try:
            archive_file = os.path.join(packages_home, package.archive())
            assert os.path.isfile(archive_file), "archive file '{}' not found here {}.".format(
                archive_file,
                packages_home)

            digest_file  = os.path.join(packages_home, package.archive_digest())
            assert os.path.isfile(digest_file), "archive digest file '{}' not found here {}.".format(
                digest_file,
                packages_home)

            check_integrity(archive_file, digest_file)

            with tarfile.open(archive_file, "r:gz") as archive_reader:
                archive_reader.extractall(path=here)

            print("installed '{}' found here '{}' for '{}', here '{}'".format(package.artifact.id(),
                                                                              packages_home,
                                                                              arch,
                                                                              here))

        except AssertionError as err:
            print(err)

def remove_all_artifacts_found(here):
    shutil.rmtree(here, ignore_errors=True)

def check_integrity(archive_file, digest_file):

    with open(digest_file) as digest_file_reader:
        target_md5_digest = digest_file_reader.readline().split()[0]

    md5_digest_calculator = hashlib.md5()
    with open(archive_file, "rb") as archive_reader:
        for bytes in iter(lambda: archive_reader.read(4096), b""):
            md5_digest_calculator.update(bytes)

    source_md5_digest = md5_digest_calculator.hexdigest()
    assert (source_md5_digest == target_md5_digest), "integrity control of '{}' failed (digest: '{}', expected: '{}')".format(archive_file,source_md5_digest, target_md5_digest)
