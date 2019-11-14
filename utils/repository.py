import hashlib
import os
import tarfile
import utils
import shutil

# singleton
PACKAGES_HOME = '/share/modules'

def install_package(requirement, arch, here):
    print("installing '{}' for '{}' here '{}'".format(requirement, arch, here))
    package = utils.Package(requirement, arch)

    archive_file = os.path.join(PACKAGES_HOME, package.archive())
    assert os.path.isfile(archive_file), "archive file '{}' not found.".format(archive_file)

    digest_file  = os.path.join(PACKAGES_HOME, package.archive_digest())
    assert os.path.isfile(digest_file), "archive digest file '{}' not found.".format(digest_file)

    check_integrity(archive_file, digest_file)

    with tarfile.open(archive_file, "r:gz") as archive_reader:
        archive_reader.extractall(path=here)

def remove_all_artifacts_found(here):
    shutil.rmtree(here)

def check_integrity(archive_file, digest_file):

    with open(digest_file) as digest_file_reader:
        target_md5_digest = digest_file_reader.readline().split()[0]

    md5_digest_calculator = hashlib.md5()
    with open(archive_file, "rb") as archive_reader:
        for bytes in iter(lambda: archive_reader.read(4096), b""):
            md5_digest_calculator.update(bytes)

    source_md5_digest = md5_digest_calculator.hexdigest()
    assert (source_md5_digest == target_md5_digest), "integrity control of '{}' failed (digest: '{}', expected: '{}')".format(archive_file,source_md5_digest, target_md5_digest)
