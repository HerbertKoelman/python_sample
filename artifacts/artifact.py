# -*- coding: utf-8 -*-

import platform
import semantic_version
import artifacts


class Artifact:

    KNOWN_BUILD_TYPES = ['snapshot', 'stable']

    def __init__(self, name: str, build_type: str = None, version = None, os: str = None, description: str = None):
        """
        initialize an Artifact description instance.

        we initialize an instance ethier by setting the attributes passed as parameters or by parsing the name string. the
        parsing is triggered when the version parameter is None.

        :param name: artifact name or description string.
        :param build_type: does this instance represent a stable or snapshot version (default is 'snapshot'
        :param version: artifact's semantic version number (semver)
        :param os: the OS this artifact was built for (can be None).
        :param description: a short description of what it does (can be None).
        """

        self.name        = name
        self.os          = os
        self.description = description
        self.build_type  = None # initialize attribute it will be set later

        if version is None:
           self.parse_description_string(name, build_type)

        else:
            self.version    = semantic_version.Version(version)
            self.build_type = self.check_build_type_value(build_type)

        # TODO we might consider removing this test.
        assert self.name is not None and self.version is not None and self.build_type is not None, \
            "failed to initialize Artifact ({},{},{})".format(
                name,
                version,
                build_type)

    def parse_description_string(self, description_string, build_type = None):
        """
        A description string should lok like this 'artifact_name[-os]-<sem ver version>[-snapshot]'.

        This string is parsed and each attr found is used to initialize class instance.

        The build type parameter overides any value that was found in the descriptino string

        :param description_string: description string where each descirption is a token.
        :param build_type: 'snapshot' or 'stable'
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

        if version_position == last_token:
            tokens.pop() # remove last element
            self.build_type = self.check_build_type_value('stable')

        # there is ONE token just after the version token, we will consider this to be the build type
        elif version_position == (last_token - 1):
            self.build_type = self.check_build_type_value(tokens[last_token].lower())

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

        # if build_type parameter is given, then it ocerides the actual found value.
        if build_type is not None: self.build_type = Artifact.check_build_type_value(build_type)

    @staticmethod
    def check_build_type_value(build_type):

        if build_type is None:
            build_type = 'snapshot'
        else:
            build_type = build_type.lower()

        assert build_type in Artifact.KNOWN_BUILD_TYPES, "artifact build type '{}' is not supported (expected to be in {})".format(
            build_type,
            Artifact.KNOWN_BUILD_TYPES
        )

        return build_type

    def id(self):
        """
        :return: unique identification string
        """
        id = self.name
        if self.os is not None:
            id += "-{os}".format(os=self.os)

        id += "-{version}".format(version=self.version)

        if self.build_type == 'snapshot':
            id += "-{build_type}".format(build_type=self.build_type)

        return id

    def is_snapshot(self):
        """
        :return: True if this is a snapshot version (unstable)
        """
        return self.build_type == 'snapshot'

    def desc(self):
        """
        :return: a short description string (all attributes are displayed)
        """
        if self.description is None:
            return "{name} / {version} (os: {os}, build type: {build_type})".format(
                name=self.name,
                version=self.version,
                os=self.os,
                build_type=self.build_type
            )
        else:
            return "{name} / {version} (os: {os}, build type: {build_type}): {description}".format(
                name=self.name,
                version=self.version,
                os=self.os,
                build_type=self.build_type,
                description=self.description
            )

    def __str__(self):
        return self.id()

    def __eq__(self, other):
        if isinstance(other, str):
            return self.id() == other
        # TODO this can prabably be removed
        # elif isinstance(other, Artifact):
        #     return self.id() == other.id()
