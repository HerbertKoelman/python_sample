# Object

This is a very simple dependency handling system. It's based on naming conventions and uses a plain FS to store and search for arftifacts.

The modules handles:
- The deployment of artifacts listed in a YAML file into a given directory. It searches for packages into a list of directories.
- The copy of artifacts found in a FS tree into a given artifacts directory

An artfact is anything that is any code, library or program packaged into a _compressed tape archive_ (tar.gz). Artifacts are listed 
into a YAML file under the key *requires*. The requires YAML structure can have two forms.

```yaml
# This is a sample requirement files
requires:
  - common-qnx-1.2.3-snapshot
  - ipcm-api-qnx-2.2.3
  - bsp-qnx-3.2.3
  - double-qnx-1.0.0
``` 
or
```yaml
# This is a sample requirement files
requires:
  stable:
    - openssl-qnx-2.2.3
    - cpp-pthread-qnx-3.2.3
    - double-qnx-1.0.0
  snapshot:
    - snapshot-lib-qnx-1.2.3
```

This python program uses:
- pyyaml: a yaml parser (more on [PyYAML](https://pypi.org/project/PyYAML/) here)
- semantic version: a module that handles [SemVer]() versions (more on [semantic_version](https://pypi.org/project/semantic-version/) here) 

# What is does

## Artifact deployment

The *deployer.py* Python program handles the following steps:
1. searches required artifact packages (tar.gz) into a list of directories
2. checks that the MD5 digest found in the digest file is eaqual to the digest calculated from the tape archive that contains the artifact.
3. extract from the checked artifact into the a target directory the following:
   - lib : libraries
   - include : header files (*.h, *.hpp)
   - bin : program files

## Artifact copy

The *copy.py* Python program moves artifact tape archives into a target directory. If a *stable* artifact is found in the target directory, 
then the archive is not moved. Only *snapshot* artifacts are  *ALWAYS* moved, replacing the xisting archive by the one found. 