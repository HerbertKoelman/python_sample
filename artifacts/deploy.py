import argparse
import sys
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
                            help='empty the installation directory')
        parser.add_argument("--install-dir",
                            dest="install_dir",
                            required=True,
                            help='deploy required artefacts here')
        parser.add_argument("--target-arch",
                            dest="target_arch",
                            required=True,
                            help='deploy required artefacts for this CPU architecture')
        parser.add_argument("--packages-home",
                            dest="packages_home_dir",
                            required=False,
                            help='deploy required artefacts here')

        parser.add_argument("files", nargs=argparse.REMAINDER, help='YAML files to parses')

        arguments = parser.parse_args()

        if arguments.files is None or len(arguments.files) == 0:
            parser.print_help()
            raise Exception("missing requirement files")
        
        print("deploy artifacts found in {} here {}".format(arguments.files, arguments.install_dir))

        if arguments.install_dir is not None and arguments.force:
            artifacts.remove_all_artifacts_found(arguments.install_dir)

        for file in arguments.files:
            print("-------------- ", file, " -----------------")
            for artefact in artifacts.requirements.load_requirements_from(file):
                artifacts.repository.install_package(artefact, arch=arguments.target_arch, here=arguments.install_dir )

    except Exception as err:
        err.with_traceback()
        print("error: {} failed. {}".format(parser.prog, err))
        sys.exit(-99)

if __name__ == '__main__':
    main()
