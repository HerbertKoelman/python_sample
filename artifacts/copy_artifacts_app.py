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
                            required=False,
                            help='copy found artifacts here')

        parser.add_argument("items",
                            metavar='base directory to search or archive file',
                            nargs=argparse.REMAINDER,
                            help='base directory to search for artifacts or archive file')

        arguments = parser.parse_args()

        if arguments.items is None or len(arguments.items) == 0:
            parser.print_usage()
            raise Exception("missing item list")
        else:
            if arguments.packages_home_dir is not None:
                repository = arguments.packages_home_dir
            else:
                repository = arguments.items[len(arguments.items) - 1]
                arguments.items.pop()

            assert os.path.isdir(repository), "{} is not a directory.".format(repository)

            for item in arguments.items:
                if os.path.isfile(item):
                    artifacts.copy_package(item, repository)
                elif os.path.isdir(item):
                    print("-------------- searching base dir: ", item, " -----------------")
                    for archive in glob.glob(os.path.join(item, "**", "*.tar.gz"), recursive=True):
                        artifacts.copy_package(archive, repository)
                else:
                    raise AssertionError("'{}' is neither a file nor a directory.".format(item))

    except AssertionError as err:
        print("error: {} failed. {}".format(parser.prog, err))

    except Exception as err:
        traceback.print_tb(err.__traceback__, limit=1, file=sys.stdout)
        print("error: {} failed. {}".format(parser.prog, err))

    return exit_status

if __name__ == '__main__':
    sys.exit(main())