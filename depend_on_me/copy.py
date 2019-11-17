import argparse
# import depend_on_me
import glob
import os
import sys
import utils
# from .utils import *
from .argv_argc import *

if __name__ == '__main__':  # nécessaire que si on veut eviter que ce code soit systématiquement exécuté. Que ce soit comme import ou programme

    parser = argparse.ArgumentParser(
        prefix_chars='-',
        description='deploy/install the requirements found in each given YAML file'
    )

    try:
        args = argv_argc.copy(parser)

        for base_dir in args.base_dirs:
            print("-------------- base dir: ", base_dir, " -----------------")
            for archive in glob.glob(os.path.join(base_dir, "**", "*.tar.gz"), recursive=True):
                utils.copy_package(archive, args.packages_home_dir)

    except Exception as err:
        print("error: {} failed. {}".format(parser.prog, err))
        sys.exit(-99)
