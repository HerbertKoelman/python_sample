# Object

[![Build Status](https://travis-ci.com/HerbertKoelman/python_sample.svg?branch=master)](https://travis-ci.com/HerbertKoelman/python_sample)

This is a very simple dependency handling system. It's based on naming conventions and plain archive files.

> Normally, you should use thinks like [conan](https://conan.io) to handle dependencies. But, if for some obscur reason this is not an option, then 
> this can ease the pain.

A plain software build is relying on
1. source code (the one you write) 
2. libraries that needs to be identified and versionned

A software build might in turn produce a library used by yourself or someone else. The following figure illustrate the point.:w


```shell script
                    <source code>
                          A
                          |
                    [cmake build] -> <package>.tar.gz -> [artifact-copy] -> /your/repository
                          |
                          V
/your/repository  <-[artifact-deploy]
```

This module comes as commands 
- `artifact-copy` : move packages into your repository in safe way
- `artifact-deploy` : deploy packages listed in a requirment file into your workspace.

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

# How it's done

Requirements are listed in a file in which the deploy command expects to find a root entry *requires*.

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

The command `artifact-deploy` uses such a yaml file to list the packages your project's requires. For each entry found, 
the program expects to find an archive in one of the pathes listed by the variable `PACKAGES-HOME_PATH`. A package archive name
is expected to have this form: `<name>[-<os>]-<semver>[-snapshot]-<target arch>.tar.gz`.

Where
- name: speaks for itself
- os: the operating system the package was built for (Darwin, ...) - optional
- semver: semantic version (more on [semver](http://semver.org) here)
- snapshot: build type (either snapshot or stable)
- target arch: target CPU (x86, armv7, ...)

When `artifact-deploy` finds a package, a digest is calculated and checked against the content of a digest file (using MD5).

> **WARN** a digest file is expected to be named `<name>[-<os>]-<semver>[-snapshot]-<target arch>.tar.gz.md5` and MUST 
> exist.

```shell script
$ artifact-deploy --install-dir /your/workspace --target-arch x86 requirements.yml 
deploy artifacts found in ['requirements.yml'] here /tmp/deps
installed 'artifact-qnx-2.3.4-snapshot' found here '/your/repsitory' for 'x86', here '/your/workspace'
artifact-deploy deployed 1 artifacts.
$
```

When you have built new packages, you can copy them to your repository directory this way.

```shell script
$ artifact-copy cmake-build/*.tar.gz /your/repository
copied cmake-build/artifact-qnx-2.3.4-snapshot-x86.tar.gz to /your/repository/.
package cmake-build/cpp-pthread-Darwin-1.11.0-x86.tar.gz is stable and exists in /your/repository/, it will NOT be copied.

```

# How you can help

More soon...
