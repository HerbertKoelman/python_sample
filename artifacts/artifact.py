# -*- coding: utf-8 -*-

import platform
import semantic_version
import artifacts


class Artifact:

    KNOWN_BUILD_TYPES = ['snapshot', 'stable']

    def __init__(self, name: str, build_type: str = 'snapshot', version = None, os: str = None, description: str = None):
        """
        initialize an Artifact description instance.

        we initialize an instance ethier by setting the attributes passed as parameters or by parsing the name string. the
        parsing is triggered when the version parameter is None

        :param name: artifact name or description string.
        :param build_type: does this instance represent a stable or snapshot version
        :param version: artifact's semantic version number (semver)
        :param os: the OS this artifact was built for (can be None).
        :param description: a short description of what it does (can be None).
        """

        self.name        = name
        self.os          = os
        self.description = description

        if version is None: # and build_type is None:
           self.parse_description_string(name)

        else:
            self.version = semantic_version.Version(version)
            self.build_type(build_type)

        assert self.name is not None and self.version is not None and self.build_type() is not None, \
            "failed to initialize Artifact ({})".format(
                name,
                version,
                build_type)

    def parse_description_string(self, description_string):
        """
        A description string should lok like this 'artifact_name[-os]-<sem ver version>[-snapshot]'.

        This string is parsed and each attr found is used to initialize class instance.

        :param description_string: description string where each descirption is a token.
        :return: name, version, build_type, os

        """
        seperator        = '-'
        tokens           = description_string.split(seperator)
        number_of_tokens = len(tokens)
        last_token = number_of_tokens - 1

        # what token stores the version info ?
        version_position = 0
        for token in tokens:
            if semantic_version.validate(token):
                self.version = semantic_version.Version(token)
                break

            version_position += 1

        # version is the last token, we shall consider
        if version_position == last_token:
            tokens.pop() # remove last element
            self.build_type('stable')

        # there is ONE token just after the version token, we will consider this to be the build type
        elif version_position == (last_token - 1):
            self.build_type(tokens[last_token].lower())

            tokens.pop() # remove last element
            tokens.pop() # remove last element

        if len(tokens) > 1:
            last_token = len(tokens) - 1
            if tokens[ last_token ] in artifacts.package.KNOWN_OS:
                self.os = tokens[last_token]
                tokens.pop() # remove last element

        _sep = ''
        self.name = '' # make sure that name is empty
        for token in tokens:
            self.name += _sep + token
            _sep = seperator

    def build_type(self,build_type = None):

        if build_type is None and self._build_type is None: self._build_type = 'snapshot'

        if build_type is None:
            return self._build_type
        else:
            assert build_type in Artifact.KNOWN_BUILD_TYPES, "artifact build type '{}' is not supported (expected to be in {})".format(
                build_type,
                Artifact.KNOWN_BUILD_TYPES
            )
            self._build_type = build_type.lower()

    def id(self):
        """
        :return: unique identification string
        """
        id = self.name
        if self.os is not None:
            id += "-{os}".format(os=self.os)

        id += "-{version}".format(version=self.version)

        if self._build_type == 'snapshot':
            id += "-{build_type}".format(build_type=self._build_type)

        return id

    def is_snapshot(self):
        """
        :return: True if this is a snapshot version (unstable)
        """
        return self._build_type == 'snapshot'

    def desc(self):
        """
        :return: a short description string (all attributes are displayed)
        """
        if self.description is None:
            return "{name} / {version} (os: {os}, build type: {build_type})".format(
                name=self.name,
                version=self.version,
                os=self.os,
                build_type=self.build_type()
            )
        else:
            return "{name} / {version} (os: {os}, build type: {build_type}): {description}".format(
                name=self.name,
                version=self.version,
                os=self.os,
                build_type=self.build_type(),
                description=self.description
            )

    def __str__(self):
        return self.id()

    def __eq__(self, other):
        if isinstance(other, str):
            return self.id() == other
        elif isinstance(other, Artifact):
            return self.id() == other.id()
