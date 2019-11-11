import platform, os, sys, semantic_version

class Artifact:
    """
    Un truc fait par un dévéloppeur.

    En informatique, un artéfact computationnel est le résultat obtenu par l'homme par l'usage d'outils ou de principes
    reliés aux domaines de l'informatique, du multimédia ou de la pensée computationnelle. Un artéfact computationnel
    peut être un programme, un script, un microprocesseur, une image, un jeu, une vidéo, une page Web, etc.
    """

    KNOWN_BUILD_TYPES = ['snapshot', 'stable']
    KNOWN_OS          = ['qnx', 'linux', 'darwin']

    def __init__(self, name: str, build_type: str = None, version = None, os: str = None, target_arch: str = None, description: str = None):
        """
        Artifact description class.

        The default packaging is a TAR.GZ file.

        If the versin and builr_type properties are not passed, then we consider name to be an artifact description string. This
        description string is parsed and version and build type infos are searched for.

        :param name: artifact name.
        :param build_type: does this instance represent a stable or snapshot version
        :param version: artifact's semantic vzersion number (semver)
        :param os: the OS this artifact was built for.
        :param target_arch: the CPU this artifact was built for (x86, armv7, ...)
        :param description: a short description of what it does.
        """
        try:
            assert name is not None, "missing name attribute/parameter, failed to initialize class Artefact."

            self.name = name
            self.os = os
            self.description = description
            if target_arch is None:
                self.target_arch = platform.machine()
            else:
                self.target_arch = target_arch

            if version is None: # and build_type is None:
                self.name, self.version, self.build_type, self.os = self.parse_artifact_description_string(name)
            else:
                self.version = semantic_version.Version(version)
                self.build_type = build_type

            self.package = Packaging(self)

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
                   "in %r was found a build type %r which is not a valid value. Accepted values are %" \
                   % (description_string, build_type, Artifact.KNOWN_BUILD_TYPES)

            tokens.pop(last_token)
            tokens.pop(last_token -1)

        if len(tokens) > 1:
            last_token = len(tokens) - 1
            if tokens[ last_token ] in Artifact.KNOWN_OS:
                os = tokens[last_token]
                tokens.pop(last_token)

        _sep = ''
        for token in tokens:
            name += _sep + token
            _sep = seperator

        return name, version, build_type, os

    def id(self):
        id = self.name
        if self.os is not None:
            id += "-{os}".format(os=self.os)

        id += "-{version}".format(version=self.version)

        if self.build_type == 'snapshot':
            id += "-{build_type}".format(build_type=self.build_type)

        id += "-{arch}".format(arch=self.target_arch)

        return id


    def summary(self):
        print("name: ", self.name)
        print("OS: ", self.os)
        print("arch: ", self.target_arch)
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
            arch= self.target_arch,
            build_type=self.build_type_display_name())

    def __eq__(self, other):
        if isinstance(other, str):
            return self.id() == other
        elif isinstance(other, Artifact):
            return self.id() == other.id()


class Packaging:
    """
    handles artefacts container (tar.gz)
    """

    def __init__(self, artifact: Artifact):
        self.artifact = artifact

    def archive(self):
        return "{}.tar.gz".format(self.artifact.id())

    def archive_digest(self):
        return"{}.tar.gz.md5".format(self.artifact.id())

    def type(self):
        return "tar.gz"

    def description(self):
        return "compressed tape archive"

    def __str__(self):
        return "artifact {}:\n- {}\n- {} (digest)".format(self.artifact, self.archive(), self.archive_digest())

class Packages:
    """
    Handles the storing of artifact packages:
    - The default implementation uses a file system as backend
    """

    PACKAGES_INDEX = {}
    PACKAGES_PATH  = ['/share/modules']

    def __init__(self, packages_home = None):

        if packages_home is None:
            packages_home = os.getenv('PACKAGES_HOME')

        if isinstance(packages_home, str):
            PACKAGES_PATH = packages_home.split(';')
        elif isinstance(packages_home, list):
            PACKAGES_PATH = packages_home
        else:
            raise TypeError("failed to create an instance Packages, packages_home parameter can only be of type str or list")

        assert len(PACKAGES_PATH) > 0 , "no valid artifact search path was found, did you set anv variable PACKAGES_HOME ?"

    def regsiter(self, artifact: Artifact):
        Packages.PACKAGES_INDEX[artifact.id()] = artifact

    def deploy(self, artifact: Artifact, here):
        print("deply", artifact)

    def search_for(self, item):
        if isinstance(item, Packaging):
            print("Search for package: {}\nFull information\n{}".format(item.artifact.name, item))
        if isinstance(item, Artifact):
            print("Search for package: {}\nFull information\n{}".format(item.name, item.package))

# singleton
PACKAGES_HOME = '/share/modules'
PACKAGES = Packages(PACKAGES_HOME)
