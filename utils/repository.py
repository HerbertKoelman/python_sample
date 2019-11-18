import hashlib
import os
import tarfile
import utils
import shutil
import glob

# singleton
PACKAGES_HOME_PATH = os.getenv('PACKAGES_HOME_PATH', '/share/modules').split(':')
PACKAGES = {}

def install_package(requirement, arch, here):
    package = utils.Package(requirement, arch)
    if package.id() not in PACKAGES:
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
                PACKAGES[package.id()] = package
            except AssertionError as err:
                print(err)
    else:
        print("artifact '{}' already deployed.")

def copy_package(archive, to):
    """
    copy given archive to a directory.

    The archive parameter is expected to contain a valid package and artifact descrption string. Before copying, the
    archive file is checked against the content of the archive's digest file. If the digests match, the archive will be
    copied.

    :param archive: relative or absolute path to an archive
    :param to: target directory.
    :return:
    """
    basename = os.path.basename(archive)
    dirname  = os.path.dirname(archive)

    package = utils.Package(basename)

    source_archive        = os.path.join(dirname, package.archive())
    source_archive_digest = os.path.join(dirname, package.archive_digest())
    target_archive        = os.path.join(to, package.archive())
    target_archive_digest = os.path.join(to, package.archive_digest())

    if package.artifact.is_snapshot():
        check_integrity(source_archive, source_archive_digest)
        shutil.copy(source_archive, target_archive)
        shutil.copy(source_archive_digest, target_archive_digest)
        print ("copied {} to {}".format(os.path.join(dirname, package.archive()), os.path.join(to, package.archive())))

    elif not package.artifact.is_snapshot() and not os.path.isfile(target_archive):
        check_integrity(source_archive, source_archive_digest)
        shutil.copy(source_archive, target_archive)
        shutil.copy(source_archive_digest, target_archive_digest)
        print("copied {} to {}".format(os.path.join(dirname, package.archive()), os.path.join(to, package.archive())))

    else:
        print ("package {} is stable and {} exists, {} will NOT be copied into {}".format(
            package.id(),
            target_archive,
            package.artifact.id(),
            to
        ))

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