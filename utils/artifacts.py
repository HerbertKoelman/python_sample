import platform
import utils.deploy

class Package:
    pass

class Artifact:
    """
    Un truc fait par un dévéloppeur.

    En informatique, un artéfact computationnel est le résultat obtenu par l'homme par l'usage d'outils ou de principes
    reliés aux domaines de l'informatique, du multimédia ou de la pensée computationnelle. Un artéfact computationnel
    peut être un programme, un script, un microprocesseur, une image, un jeu, une vidéo, une page Web, etc.
    """

    def __init__(self, name: str, build_type: str = None, version = None, os: str = None, target_arch: str = None, description: str = None):

        self.version = version
        self.build_type = build_type
        self.os = os

        tokens = name.split('-')

        if len(tokens) == 2:
            self.name = tokens[0]
            self.version = tokens[1]
        elif len(tokens) == 3:
            self.name = tokens[0]
            self.version = tokens[1]
            self.build_type=tokens[2]
        elif len(tokens) == 4:
            self.name = tokens[0]
            self.os = tokens[1]
            self.version = tokens[3]
            self.build_type=tokens[4]
        else:
            self.name = name

        self.description = description

        if target_arch is None:
            self.target_arch = platform.machine()
        else:
            self.target_arch = target_arch

        self.package = Package(self)

        assert self.version is not None, "missing Artefact version parameter, failed to initialize Artefact {}".format(name)

    def id(self):
        return "{name}-{version}-{arch}".format(name=self.name, version=self.version, arch=self.target_arch)

    def summary(self):
        print("name: ", self.name)
        print("OS: ", self.os)
        print("arch: ", self.target_arch)
        print("version: {} ({})".format(self.version, self.build_type))
        print("description --------------------------------------------------------")
        print(self.description)

    def __str__(self):
        return "{name} (version: {version}, arch: {arch}, build type: {build_type})".format(version=self.version, name=self.name, arch= self.target_arch, build_type=self.build_type)

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

    def add(self, artifact: Artifact):
        self.package_index[artifact.id()] = artifact

    def deploy(self, artifact: Artifact, here):
        utils.deploy.check_archive_integrity(artifact.package.archive)

    def search_for(self, item):
        if isinstance(item, Package):
            print("Search for package: {}\nFull information\n{}".format(item.artifact.name, item))
        if isinstance(item, Artifact):
            print("Search for package: {}\nFull information\n{}".format(item.name, item.package))


# singleton
PACKAGES_HOME = '/share/modules'
PACKAGES = Packages(PACKAGES_HOME)
