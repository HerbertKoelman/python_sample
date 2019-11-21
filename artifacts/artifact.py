# -*- coding: utf-8 -*-

import platform
import semantic_version
import artifacts


class Artifact:

    KNOWN_BUILD_TYPES = ['snapshot', 'stable']

    def __init__(self, name: str, build_type: str = None, version = None, os: str = None, description: str = None):
        """
        initialize an Artifact description instance.

        :param name: artifact name or description string.
        :param build_type: does this instance represent a stable or snapshot version
        :param version: artifact's semantic version number (semver)
        :param os: the OS this artifact was built for.
        :param source_arch: the CPU this artifact was instantiated (x86, armv7, ...)
        :param description: a short description of what it does.

        """
        try:
            assert name is not None, "missing name attribute/parameter, failed to initialize class Artefact."

            self.name = name
            self.os = os
            self.description = description
            self.build_type = build_type

            if version is None: # and build_type is None:
               self.parse_artifact_description_string(name)

            else:
                self.version = semantic_version.Version(version)

            # TODO suppress this self.package = Package(self)

            assert self.version is not None, "failed to set class Artefact's attribute version, initialization of Artefact {} failed".format(name)

        except ValueError as err:
            raise ValueError("failed to initialize artefact [{}], {}".format(name, err))

    def parse_artifact_description_string(self, description_string):
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

        # init return variables
        name       = ''
        version    = None
        build_type = None
        os         = None

        # what token stores the version info ?
        version_position = 0
        for token in tokens:
            if semantic_version.validate(token):
                version = semantic_version.Version(token)
                break

            version_position += 1

        # version is the last token, we shall consider
        if version_position == last_token:
            tokens.pop(last_token)

        # there is ONE token just after the version token, we will consider this to be the build type
        elif version_position == (last_token - 1):
            build_type = tokens[last_token].lower()
            assert build_type in Artifact.KNOWN_BUILD_TYPES, \
                "in '{}' was found a build type '{}'}' which is not a valid value. Accepted values are {}".format(
                    description_string,
                    build_type,
                    Artifact.KNOWN_BUILD_TYPES)

            tokens.pop(last_token)
            tokens.pop(last_token -1)

        if len(tokens) > 1:
            last_token = len(tokens) - 1
            if tokens[ last_token ] in artifacts.package.KNOWN_OS:
                os = tokens[last_token]
                tokens.pop(last_token)

        _sep = ''
        for token in tokens:
            name += _sep + token
            _sep = seperator

        assert name is not None and version is not None, "failed to parse artifact description string '{}'".format(description_string)

        self.name = name
        self.version=version
        self.os = os

        if build_type is not None:
            self.build_type = build_type

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
                build_type=self.build_type_display_name()
            )
        else:
            return "{name} / {version} (os: {os}, build type: {build_type}): {description}".format(
                name=self.name,
                version=self.version,
                os=self.os,
                build_type=self.build_type_display_name(),
                description=self.description
            )

    def build_type_display_name(self):
        if self.build_type is None:
            return 'stable'
        else:
            return self.build_type

    def __str__(self):
        return self.id()

    def __eq__(self, other):
        if isinstance(other, str):
            return self.id() == other
        elif isinstance(other, Artifact):
            return self.id() == other.id()
