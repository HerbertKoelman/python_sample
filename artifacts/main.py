# -*- coding: utf-8 -*-

import artifacts
import argparse

"""
This is the main command that dispatches commands.
"""

def artifacts_command():
    parser = argparse.ArgumentParser(
        prefix_chars='-',
        formatter_class=argparse.RawTextHelpFormatter,
        description='handles artifacts (deploy, list, copy, search, ...).',
        epilog="program version: {version}".format(version=artifacts.__version__)

    )
if __name__ == '__main__':
    artifacts_command()
