import argparse
import sys
import os
import traceback
import artifacts

def main():
    """Handles the deployment of artifacts."""

    parser = argparse.ArgumentParser(
        prefix_chars='-',
        description='deploy/install the requirements found in each given YAML file'
    )

    try:
        parser.add_argument("--force", dest="force",
                            action='store_true',
                            required=False,
                            help='empty the installation directory before deploying artifacts')
        parser.add_argument("--install-dir",
                            dest="install_dir",
                            required=True,
                            help='deploy required artifacts here')
        parser.add_argument("--target-arch",
                            dest="target_arch",
                            required=True,
                            help='deploy required artifacts for this CPU architecture')
        parser.add_argument("--packages-home",
                            dest="packages_home_dir",
                            required=False,
                            help='deploy required artifacts here')

        parser.add_argument("files", nargs=argparse.REMAINDER, help='YAML files to parses')

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
            print("-------------- ", file, " -----------------")
            for artefact in artifacts.requirements.load_requirements_from(file):
                artifacts.repository.install_package(artefact, arch=arguments.target_arch, here=arguments.install_dir )

    except AssertionError as err:
        print("error: {} failed. {}".format(parser.prog, err))
        sys.exit(-99)
    except Exception as err:
        traceback.print_tb(err.__traceback__, limit=5, file=sys.stdout)
        print("error: {} failed. {}".format(parser.prog, err))
        sys.exit(-99)

if __name__ == '__main__':
    main()
