# -*- coding: utf-8 -*-

import argparse
import sys
import traceback

import artifacts


def main():
    """Handles the deployment of artifacts."""
    parser = argparse.ArgumentParser(
        prefix_chars='-',
        formatter_class=argparse.RawTextHelpFormatter,
        description='deploy/install the requirements found in each given file',
        epilog="""
The program searches for requirement entries in either a text or yaml file. For each entry, it searches for a package
that satifies the requirment. If a match is found and the package's integrity is verified, it is installed into your 
workspace directory.

A requirement is a formatted string of the form <name>[-<os>]-<semver>[-snapshot]. The parts in the square baces are 
optional. For each requirement found in the given files, the programs searches PACKAGES_HOME_PATH for an archive named 
like this <name>[-<os>]-<semver>[-snapshot]-<target arch>.tar.gz.

program version: {version}
                """.format(version=artifacts.__version__)

    )

    try:

        parser.add_argument("--force", dest="force",
                            action='store_true',
                            required=False,
                            help='empty the installation directory before deploying artifacts')
        parser.add_argument("--packages-home",
                            dest="packages_home_dir",
                            required=False,
                            help='deploy required artifacts here (default value is ''/share/modules'')')

        mandatory_group = parser.add_argument_group('mandatory arguments')
        mandatory_group.add_argument("--install-dir",
                            dest="install_dir",
                            required=True,
                            metavar='workspace',
                            help='install packages here')
        mandatory_group.add_argument("--target-arch",
                            dest="target_arch",
                            choices=artifacts.KNOWN_ARCHS,
                            required=True,
                            help='deploy only packages that can runon this CPU architecture')

        parser.add_argument("files", nargs=argparse.REMAINDER, metavar='file1...', help='requirement files to parses, can be a YAML or text file')

        arguments = parser.parse_args()

        if arguments.files is None or len(arguments.files) == 0:
            parser.print_help()
            raise Exception("missing requirement files")

        if arguments.packages_home_dir is not None:
            artifacts.package_search_pathes([arguments.packages_home_dir])

        print("deploy artifacts found in {} here {}".format(arguments.files, arguments.install_dir))

        if arguments.install_dir is not None and arguments.force:
            artifacts.remove_all_artifacts_found(arguments.install_dir)

        for file in arguments.files:
            # TODO remove this print("-------------- ", file, " -----------------")
            counter = 0
            for artefact in artifacts.requirements.load_requirements_from(file):
                if artifacts.repository.install_package(artefact, arch=arguments.target_arch, here=arguments.install_dir ):
                    counter += 1
        print ("{} deployed {} artifacts.".format(parser.prog, counter))

    except AssertionError as err:
        print("error: {} failed. {}".format(parser.prog, err))
        sys.exit(-99)
    except Exception as err:
        traceback.print_tb(err.__traceback__, limit=5, file=sys.stdout)
        print("error: {} failed. {}".format(parser.prog, err))
        sys.exit(-99)

if __name__ == '__main__':
    main()
