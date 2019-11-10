import sys, os, platform

def artifact(artifact, here, arch = None):
    """
    searches PACKAGES_HOME for artefacts and deploy thier content in a given target directory.

    :param artifact: artefact name (should include version information)
    :param here: target directory
    :param arch: target CPU architecture you want to deply (defaults to the arch you're running on)
    :return:
    """
    if arch is None:
        arch = platform.machine()

    print("Deploying {} for {} here {}".format(artifact, arch, here))

def check_archive_integrity(archive):
    print("Checking archive {}'s integrity".format(archive))