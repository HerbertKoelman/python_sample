# -*- coding: utf-8 -*-

import platform
import semantic_version
import artifacts


class Artifact:
    """
    Describes something crafted by a developper to make your life easier.
    """

    KNOWN_BUILD_TYPES = ['snapshot', 'stable']

    def __init__(self, name: str, build_type: str = None, version = None, os: str = None, source_arch: str = None, description: str = None):
        """
        Artifact description class.

        The default packaging is a TAR.GZ file.

        If the versin and builr_type properties are not passed, then we consider name to be an artifact description string. This
        description string is parsed and version and build type infos are searched for.

        :param name: artifact name.
        :param build_type: does this instance represent a stable or snapshot version
        :param version: artifact's semantic vzersion number (semver)
        :param os: the OS this artifact was built for.
        :param source_arch: the CPU this artifact was built for (x86, armv7, ...)
        :param description: a short description of what it does.

        """
        try:
            assert name is not None, "missing name attribute/parameter, failed to initialize class Artefact."

            self.name = name
            self.os = os
            self.description = description
            if source_arch is None:
                self.source_arch = platform.machine()

            else:
                self.source_arch = source_arch

            if version is None: # and build_type is None:
                self.name, self.version, self.build_type, self.os = self.parse_artifact_description_string(name)

            else:
                self.version = semantic_version.Version(version)
                self.build_type = build_type

            # TODO suppress this self.package = Package(self)

            assert self.version is not None, "failed to set class Artefact's attribute version, initialization of Artefact {} failed".format(name)

        except ValueError as err:
            raise ValueError("failed to initialize artefact [{}], {}".format(name, err))

    def parse_artifact_description_string(self, description_string):
        """
        A description string is made of tokens arranged like this:
        name_of-artefact-<sem ver version>[-snapshot]

        The name of the artefact MUST be seperated by a valid semantic version string. There can be ONLY and ONLY one optional
        token after the version token: snapshot. If an artefact is not a snapshot version it is considered a stable one.

        Everything that on left side of the versin token is considered to be the artifact's name.

        For example the description string 'common-qnx-1.2.3-SNAPSHOT' will be regonized as "common-qnx (version: 1.2.3, arch: x86_64, build type: snapshot)"

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

        return name, version, build_type, os

    def id(self):
        id = self.name
        if self.os is not None:
            id += "-{os}".format(os=self.os)

        id += "-{version}".format(version=self.version)

        if self.build_type == 'snapshot':
            id += "-{build_type}".format(build_type=self.build_type)

        # TODO suppress this id += "-{arch}".format(arch=self.source_arch)

        return id

    def is_snapshot(self):
        return self.build_type == 'snapshot'

    def summary(self):
        print("name: ", self.name)
        print("OS: ", self.os)
        print("arch: ", self.source_arch)
        print("version: {} ({})".format(self.version, self.build_type_display_name()))
        print("description --------------------------------------------------------")
        print(self.description)

    def build_type_display_name(self):
        if self.build_type is None:
            return 'stable'
        else:
            return self.build_type

    def __str__(self):

        return "{name} (version: {version}, os: {os}, arch: {arch}, build type: {build_type})".format(
            name=self.name,
            version=self.version,
            os=self.os,
            arch= self.source_arch,
            build_type=self.build_type_display_name())

    def __eq__(self, other):
        if isinstance(other, str):
            return self.id() == other
        elif isinstance(other, Artifact):
            return self.id() == other.id()
