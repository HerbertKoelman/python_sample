import argparse
import glob
import os
import sys
import traceback
import artifacts

def main():
    parser = argparse.ArgumentParser(
        prefix_chars='-',
        description='deploy/install the requirements found in each given YAML file'
    )

    try:
        # parser.add_argument("--force", dest="force",
        #                     action='store_true',
        #                     required=False,
        #                     help='copy artifact even if a copy is found in target directory')
        parser.add_argument("--packages-home",
                            dest="packages_home_dir",
                            required=True,
                            help='copy found artifacts here')

        parser.add_argument("base_dirs", nargs=argparse.REMAINDER, help='artifact search base directories')

        arguments = parser.parse_args()

        if arguments.base_dirs is None or len(arguments.base_dirs) == 0:
            parser.print_usage()
            raise Exception("missing base directories")

        for base_dir in arguments.base_dirs:
            print("-------------- base dir: ", base_dir, " -----------------")
            for archive in glob.glob(os.path.join(base_dir, "**", "*.tar.gz"), recursive=True):
                artifacts.copy_package(archive, arguments.packages_home_dir)

    except AssertionError as err:
        print("error: {} failed. {}".format(parser.prog, err))
        sys.exit(-99)

    except Exception as err:
        traceback.print_tb(err.__traceback__, limit=1, file=sys.stdout)
        print("error: {} failed. {}".format(parser.prog, err))
        sys.exit(-99)

if __name__ == '__main__':  # nécessaire que si on veut eviter que ce code soit systématiquement exécuté. Que ce soit comme import ou programme
    main()