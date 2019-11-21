# Object

[![Build Status](https://travis-ci.com/HerbertKoelman/python_sample.svg?branch=master)](https://travis-ci.com/HerbertKoelman/python_sample)

This is a very simple dependency handling system. It's based on naming conventions and plain archive files.

The modules handles:
- The deployment of artifacts listed in a YAML file into a given directory. It searches for packages into a list of directories.
- The copy of artifacts found in a FS tree into a given artifacts directory

When used in a CI and/or development context, the `artifact-copy` command moves your stuff into a given directory which then is 
considered as an artifact repository. When you need one of your artifacts, you can use the command artifact-deploy to install 
the artifact's content somewhere in your workspace. The artifacts are generally copied via a Jenkins script (pipeline or else). 
One can use CMake to search for dependencies and extract them in the build directory and make the artifact's content 
available for your build recipes.

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

> FYI more in ` ./requirements.txt` 

# How to use it

The dependency handler can be build and packaged via this command:

```shell script
$ python3 setup.py sdist
running sdist
running egg_info
...
copying artifacts.egg-info/top_level.txt -> artifacts-0.1/artifacts.egg-info
Writing artifacts-0.1/setup.cfg
Creating tar archive
removing 'artifacts-0.1' (and everything under it)
```

This package is installed with the following command:

```shell script
$ pip install ./dist/artifacts-0.1.tar.gz
Processing ./dist/artifacts-0.1.tar.gz
Requirement already satisfied: PyYAML==5.1.2 in ./venv/lib/python3.7/site-packages (from artifacts==0.1) (5.1.2)
Requirement already satisfied: semantic-version==2.8.2 in ./venv/lib/python3.7/site-packages (from artifacts==0.1) (2.8.2)
Installing collected packages: artifacts
  Running setup.py install for artifacts: started
    Running setup.py install for artifacts: finished with status 'done'
Successfully installed artifacts-0.1
```

That's it :-)

# What is does

## Artifact deployment

The *deployer.py* Python program handles the following steps:
1. read from a file a list of requirements (the form of )[name]-[OS]-[SemVer version])
1. searches required artifact packages into a list of directories
2. checks that the MD5 digest found in the digest file is equal to the digest calculated from the tape archive that contains the artifact.
3. extract artifact's archive content into the a target directory.

An artifact archive uselly contains something like this:
   - lib : libraries
   - include : header files (*.h, *.hpp)
   - bin : program files

```shell script
$ artifacts-deploy -h
usage: artifact-deploy [-h] [--force] --install-dir INSTALL_DIR --target-arch
                       TARGET_ARCH [--packages-home PACKAGES_HOME_DIR]
                       ...

deploy/install the requirements found in each given YAML file

positional arguments:
  files                 YAML files to parses

optional arguments:
  -h, --help            show this help message and exit
  --force               empty the installation directory before deploying
                        artifacts
  --install-dir INSTALL_DIR
                        deploy required artifacts here
  --target-arch TARGET_ARCH
                        deploy required artifacts for this CPU architecture
  --packages-home PACKAGES_HOME_DIR
                        deploy required artifacts here
``` 

## Artifact copy

The *copy.py* Python program moves artifact tape archives into a target directory. If a *stable* artifact is found in the target directory, 
then the archive is not moved. Only *snapshot* artifacts are  *ALWAYS* moved, replacing the xisting archive by the one found.

```shell script
$ artifac-copy -h
usage: artifact-copy [-h] --packages-home PACKAGES_HOME_DIR ...

deploy/install the requirements found in each given YAML file

positional arguments:
  base_dirs             artifact search base directories

optional arguments:
  -h, --help            show this help message and exit
  --packages-home PACKAGES_HOME_DIR
                        copy found artifacts here
```
