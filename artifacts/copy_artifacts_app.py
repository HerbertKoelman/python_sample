import argparse
import glob
import os
import sys
import traceback
import artifacts

def main():

    exit_status = -99

    parser = argparse.ArgumentParser(
        prefix_chars='-',
        formatter_class=argparse.RawTextHelpFormatter,
        description='copy artifacts in your repository directory',
        epilog="""
The program searches for compressed archive files check thier integrity and copies them to your packages home directory. 
Archive file names follow this naming rule <name>[-<os>]-<semver>[-snapshot]-<target arch>.tar.gz.

program version: {version}
                """.format(version=artifacts.__version__)
    )

    try:
        mandatory_arguments = parser.add_argument_group('mandatory arguments')
        mandatory_arguments.add_argument("--packages-home",
                            dest="packages_home_dir",
                            metavar='repository directory',
                            required=True,
                            help='copy found artifacts here')

        parser.add_argument("base_dirs",
                            metavar='base directory to search or archive file',
                            nargs=argparse.REMAINDER,
                            help='base directory to search for artifacts or archive file')

        arguments = parser.parse_args()

        if arguments.base_dirs is None or len(arguments.base_dirs) == 0:
            parser.print_usage()
            raise Exception("missing base directories")

        for base_dir in arguments.base_dirs:
            if os.path.isfile(base_dir):
                artifacts.copy_package(base_dir, arguments.packages_home_dir)
            elif os.path.isdir(base_dir):
                print("-------------- searching base dir: ", base_dir, " -----------------")
                for archive in glob.glob(os.path.join(base_dir, "**", "*.tar.gz"), recursive=True):
                    artifacts.copy_package(archive, arguments.packages_home_dir)

    except AssertionError as err:
        print("error: {} failed. {}".format(parser.prog, err))

    except Exception as err:
        traceback.print_tb(err.__traceback__, limit=1, file=sys.stdout)
        print("error: {} failed. {}".format(parser.prog, err))

    return exit_status

if __name__ == '__main__':
    sys.exit(main())