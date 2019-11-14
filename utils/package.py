import utils, os, semantic_version, hashlib, tarfile

KNOWN_ARCHS = ['x86', 'x86_64', 'armv7']
KNOWN_OS    = ['qnx', 'linux',  'darwin']

class Package:
    """
    handles artefacts container (tar.gz)
    """

    def __init__(self, artifact: utils.Artifact, target_arch):
        assert artifact is not None, "artifact is a required init argument"
        assert target_arch in KNOWN_ARCHS, "target architecture '{}' is not supported, failed to initialize Package class".format(target_arch)
        self.artifact = artifact
        self._target_arch  = target_arch

    def target_arch(self, arch = None):
        if arch is None:
            return self._target_arch
        else:
            assert arch in KNOWN_ARCHS, "target architecture '{}' is not supported, failed to initialize Package class".format(arch)
            self._target_arch = arch

    def archive(self):
        return "{}.{}".format(self.id(), self.type())

    def archive_digest(self):
        return"{}.md5".format(self.archive())

    def type(self):
        return "tar.gz"

    def description(self):
        return "compressed tape archive"

    def id(self):
        return "{}-{}".format(self.artifact.id(), self.target_arch())

    def _summary(self):
        return "artifact {}:\n- {}\n- {} (digest)".format(self.artifact, self.archive(), self.archive_digest())

    def __str__(self):
        return self.id()

