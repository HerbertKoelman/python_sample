import argparse, os, sys

def deployment(parser):
    """
    Parse commande line arguments used to deploy artifacts.
    :param description: program description string.
    :return: found arguments.
    """

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

    return arguments

def copy(parser):
    """
    Copy artifacts to a given directory.
    :param description: program description string.
    :return: found arguments.
    """

    parser.add_argument("--force", dest="force",
                        action='store_true',
                        required=False,
                        help='copy artiufact even if a copy is found in target directory')
    parser.add_argument("--packages-home",
                        dest="packages_home_dir",
                        required=True,
                        help='copy found artifacts here')

    parser.add_argument("base_dirs", nargs=argparse.REMAINDER, help='artifact search base directories')

    arguments = parser.parse_args()

    if arguments.base_dirs is None or len(arguments.base_dirs) == 0:
        parser.print_help()
        raise Exception("missing base directories")

    return arguments