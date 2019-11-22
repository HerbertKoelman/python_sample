# -*- coding: utf-8 -*-

import re

import artifacts

KNOWN_ARCHS = ['x86', 'x86_64', 'armv7']
KNOWN_OS    = ['qnx', 'linux',  'darwin']

class Package:
    """
    handles artefacts container (tar.gz)
    """

    def __init__(self, artifact, target_arch = None):
        """
        initialize a package instance.

        :param artifact: a description string or an Artifact instance.
        :param target_arch: processor type.
        """

        if isinstance(artifact, artifacts.Artifact):
            self.artifact = artifact
            self.target_arch(target_arch)

        elif isinstance(artifact, str):
            self.parse_description_string(artifact)

        else:
            raise AssertionError("failed to initialize Package instance (type: {})".format(artifact.__class__))

        assert self.artifact is not None and self.target_arch() is not None, \
            "failed to initialize Package ({}, {})".format(
                artifact,
                target_arch
            )

    def parse_description_string(self, description_string):

        assert description_string.endswith(".tar.gz"), "package description '{}' doesn't end with '{}'.".format(description_string, self.type())

        description_string = re.sub("{}$".format(re.escape(self.type())), '', description_string)

        seperator = '-'
        tokens = description_string.split(seperator)
        number_of_tokens = len(tokens)
        last_token = number_of_tokens - 1

        arch_position = 0
        for token in tokens:
            if token in KNOWN_ARCHS:
                self.target_arch(token)
                break

            arch_position += 1

        tokens = tokens[0:arch_position]
        self.artifact = artifacts.Artifact('-'.join(tokens))

    def target_arch(self, arch = None):
        if arch is None:
            return self._target_arch
        else:
            assert arch in KNOWN_ARCHS, "package target architecture '{}' is not supported ({})".format(
                arch,
                self.id()
            )
            self._target_arch = arch

    def archive(self):
        return "{}{}".format(self.id(), self.type())

    def archive_digest(self):
        return"{}.md5".format(self.archive())

    def type(self):
        return ".tar.gz"

    def description(self):
        return "compressed tape archive"

    def id(self):
        if self.artifact is not None:
            return "{}-{}".format(self.artifact.id(), self.target_arch())
        else:
            return "artifact attr is None, not a valid Package instance"

    def _summary(self):
        return "artifact {}:\n- {}\n- {} (digest)".format(self.artifact, self.archive(), self.archive_digest())

    def __str__(self):
        return self.id()
