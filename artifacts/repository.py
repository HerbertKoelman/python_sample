# -*- coding: utf-8 -*-

import hashlib
import os
import shutil
import tarfile

import artifacts

# singleton
PACKAGES_HOME_PATH = os.getenv('PACKAGES_HOME_PATH', '/share/modules').split(':')
PACKAGES = {}

def package_search_pathes(list):
    artifacts.PACKAGES_HOME_PATH = list

def install_package(artifact, arch, here):
    """
    search for artifact and untar the corresponding archive file.

    artifacts are search in the a list of packages home directory. The first valid occurence found is installed.

    :param artifact: an artifacts.Artifact instance
    :param arch: a valid target processor architecture (x86, ...)
    :param here: path to the installation directory.
    :return: True if successfull
    """

    status = False

    assert isinstance(artifact, artifacts.Artifact), "{}.install_package expects a Artifact instance, you passed {}".format(
                          __name__,
                          artifact.__class__.__name__
                      )

    package = artifacts.Package(artifact, target_arch=arch)
    if package.id() not in PACKAGES.keys():
        for packages_home in artifacts.PACKAGES_HOME_PATH:
            if package.id() not in PACKAGES.keys():
                try:
                    archive_file = os.path.join(packages_home, package.archive())
                    assert os.path.isfile(archive_file), "archive file '{}' not found here {}.".format(
                        package.archive(),
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
                    status = True

                except AssertionError as err:
                    print(err)
    else:
        print("artifact '{}' for architecture {} already deployed here '{}'.".format(
            artifact.id(),
            arch,
            here))
    return status

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

    status = False
    try:
        basename = os.path.basename(archive)
        dirname  = os.path.dirname(archive)

        package = artifacts.Package(basename)

        source_archive        = os.path.join(dirname, package.archive())
        source_archive_digest = os.path.join(dirname, package.archive_digest())
        target_archive        = os.path.join(to, package.archive())
        target_archive_digest = os.path.join(to, package.archive_digest())

        if package.artifact.is_snapshot():
            check_integrity(source_archive, source_archive_digest)
            shutil.copy(source_archive, target_archive)
            shutil.copy(source_archive_digest, target_archive_digest)
            print ("copied {} to {}".format(package.id(),target_archive))
            status = True

        elif not package.artifact.is_snapshot():
            if not os.path.isfile(target_archive):
                check_integrity(source_archive, source_archive_digest)
                shutil.copy(source_archive, target_archive)
                shutil.copy(source_archive_digest, target_archive_digest)
                print("copied {} to {}".format(package.id(), target_archive))
                status = True

            else:
                print ("stable package '{}' found here '{}', package will NOT be copied".format(
                    package.id(),
                    to
                ))

    except AssertionError as err:
        print("won't copy '{}', {}".format(archive, err))

    except Exception as err:
        print("function {}.copy_package('{}') failed, {}".format(__name__, archive, err))
        raise Exception(err)

    return status

def remove_all_artifacts_found(here):
    """
    remove recursively the given directory.

    :param here: path to a directory to remove
    :return:
    """
    shutil.rmtree(here, ignore_errors=True)

def check_integrity(archive_file, digest_file):
    """
    calculate a digest for the archive file and compares the result with the digest found in the digest file.

    An AssertionError is thrown if the digests don't match.

    :param archive_file: a compressed tape archive
    :param digest_file: a file that contains the digest to check against
    """

    with open(digest_file) as digest_file_reader:
        target_md5_digest = digest_file_reader.readline().split()[0]

    md5_digest_calculator = hashlib.md5()
    with open(archive_file, "rb") as archive_reader:
        for bytes in iter(lambda: archive_reader.read(4096), b""):
            md5_digest_calculator.update(bytes)

    source_md5_digest = md5_digest_calculator.hexdigest()
    assert (source_md5_digest == target_md5_digest), "integrity control of '{}' failed (digest: '{}', expected: '{}')".format(archive_file,source_md5_digest, target_md5_digest)
