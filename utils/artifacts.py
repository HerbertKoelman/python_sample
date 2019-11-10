import platform

class Artifact:

    def __init__(self, name: str, build_type: str = "Release", version = None, arch: str = None, description: str = None):

        self.version = version
        tokens = name.split('-')

        if len(tokens) == 2:
            self.name = tokens[0]
            self.version = tokens[1]
        else:
            self.name = name

        self.build_type = build_type
        self.description = description

        if arch is None:
            self.arch = platform.machine()
        else:
            self.arch = arch

        assert self.version is not None, "missing Artefact version parameter, failed to initialize Artefact {}".format(name)

    def id(self):
        return "{name}-{version}-{arch}".format(name=self.name, version=self.version, arch=self.arch)

    def __str__(self):
        return "{name} (version: {version}, arch: {arch}, build type: {build_type})".format(version=self.version, name=self.name, arch= self.arch, build_type=self.build_type)

class Package:
    """
    handles artefacts container (tar.gz)
    """

    def __init__(self, artifact: Artifact):
        self.artifact = artifact
        self.archive        = "{}.tar.gz".format(artifact.id())
        self.archive_digest = "{}.md5".format(self.archive)

    def __str__(self):
        return "Artefact {}:\n- {}\n- {} (digest)".format(self.artifact, self.archive, self.archive_digest)

class Packages:
    """
    Handles the storing of artifact packages:
    - The default implementation uses a FS backend
    """

    def __init__(self, packages_home):
        if isinstance(packages_home, str):
            self.search_pathes = packages_home.split(';')
        elif isinstance(packages_home, list):
            self.search_pathes = packages_home
        else:
            raise TypeError("failed to create an instance Packages, packages_home parameter can only be of type str or list")

        self.package_index = {}

    def search_for(self, package: Package):
        print("Search for package: {}\nFull information\n{}".format(package.artifact.name, package))