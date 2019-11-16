import os
import utils
import re

KNOWN_ARCHS = ['x86', 'x86_64', 'armv7']
KNOWN_OS    = ['qnx', 'linux',  'darwin']

class Package:
    """
    handles artefacts container (tar.gz)
    """

    def __init__(self, artifact: utils.Artifact, target_arch = None):

        assert artifact is not None, "artifact is a required init argument"

        if isinstance(artifact, utils.Artifact):
            assert target_arch in KNOWN_ARCHS, "target architecture '{}' is not supported, failed to initialize Package class".format(target_arch)

        elif isinstance(artifact, str):
            artifact, target_arch = self.parse_package_description_string(artifact)

        self.artifact = artifact
        self._target_arch  = target_arch

    def parse_package_description_string(self, description_string):

        assert description_string.endswith(".tar.gz"), "package description string '{}' is expected to end with {}.".format(description_string, self.type())

        description_string = re.sub("{}$".format(re.escape(self.type())), '', description_string)

        seperator = '-'
        tokens = description_string.split(seperator)
        number_of_tokens = len(tokens)
        last_token = number_of_tokens - 1

        # init return variables
        artifact = None
        arch     = None
        arch_position = 0
        for token in tokens:
            if token in utils.KNOWN_ARCHS:
                arch = token
                break
            arch_position += 1

        tokens = tokens[0:arch_position]
        artifact = utils.Artifact('-'.join(tokens))

        assert arch is not None, "package description string doesn't mention a valid processor architecture, expected to in {}.".format(utils.KNOWN_ARCHS)

        return artifact, arch

    def target_arch(self, arch = None):
        if arch is None:
            return self._target_arch
        else:
            assert arch in KNOWN_ARCHS, "target architecture '{}' is not supported, failed to initialize Package class".format(arch)
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
        return "{}-{}".format(self.artifact.id(), self.target_arch())

    def _summary(self):
        return "artifact {}:\n- {}\n- {} (digest)".format(self.artifact, self.archive(), self.archive_digest())

    def __str__(self):
        return self.id()
