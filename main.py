from os.path import dirname
from os import getcwd
import sys
from pathlib import Path
from source.modes._mode_parser import parse_mode

from source.tools import alert, clean_path
from source.tools import LazyImport
from argparse import ArgumentParser, SUPPRESS, BooleanOptionalAction

# argparse = LazyImport('argparse')

root_path = dirname(sys.executable) if getattr(
    sys, 'frozen', False) else dirname(__file__)

current_dir = getcwd()


def __main():
    parser = ArgumentParser(prog="sq")
    parser.add_argument('-v', '--version',
                        action='version', version='Squba 1.1')
    parser.add_argument('-r', '--root', action='store_true', default=False,
                        help='get the root directory where Squba is installed')
    parser.add_argument(
        '--root-path', default=root_path)

    subparsers = parser.add_subparsers(dest="mode")

    #! Dive args
    dive_parser = subparsers.add_parser(
        "dive", help="explore a directory")
    dive_parser.add_argument(
        '-p', "--path", type=clean_path, help="the path to the directory you want to explore", default=current_dir
    )
    dive_parser.add_argument(
        "-d",
        "--max-depth",
        type=int,
        default=3,
        help="the max depth of the diving process; defaults to 3",
        metavar="",
    )
    filters_group = dive_parser.add_argument_group('filters')
    filters_group.add_argument(
        "-t",
        "--terms",
        nargs='+',
        default=[],
        help="a list of terms to highlight",
        metavar="",
    )
    filters_group.add_argument(
        "-x",
        "--extensions",
        nargs='+',
        default=[],
        help="a list of extensions to highlight",
        metavar="",
    )

    #! Purge args
    purge_parser = subparsers.add_parser(
        "purge", help="bulk file/folder deletion")
    purge_parser.add_argument(
        '--path', '-p',
        type=str,
        help="the path where to look for files with the provided terms/extensions",
        default=current_dir,
        metavar="",
    )
    purge_filters = purge_parser.add_mutually_exclusive_group(required=True)
    purge_filters.add_argument(
        "--terms", "-t", action="append", help="a list of terms to look for", default=[],
        metavar="",
    )
    purge_filters.add_argument(
        "--extensions",
        "-e",
        nargs='+',
        help="a list of extensions to look for",
        default=[],
        metavar="",
    )
    purge_filters.add_argument(
        '--all', '-a', action="store_true", help='delete all files',
    )
    purge_parser.add_argument(
        "--ignore-terms",
        "-it",
        nargs='+',
        help="a list of terms to ignore",
        default=[],
        metavar="",
    )
    purge_parser.add_argument(
        "--ignore-files",
        "-if",
        nargs='+',
        help="a list of files to ignore",
        default=[],
        metavar="",
    )

    #! Populate args
    populate_parser = subparsers.add_parser(
        "populate", help="bulk file/folder creation"
    )
    populate_parser.add_argument(
        '--dest', '-d', type=str, help="where to write the files", default=current_dir,
        metavar="",
    )
    populate_parser.add_argument(
        "--files",
        "-f",
        nargs='+',
        required=True,
        help="a list of files to create; use file.txt*[number] to create multiple copies of the same file",
        metavar="",
    )

    #! Sonar args
    sonar_parser = subparsers.add_parser(
        "sonar", help="monitor your system resources in real time"
    )
    sonar_parser.add_argument(
        '--network', action=BooleanOptionalAction, default=True, metavar="")
    sonar_parser.add_argument(
        '--resources', action=BooleanOptionalAction, default=True, metavar="")
    sonar_parser.add_argument(
        '--disks', action=BooleanOptionalAction, default=True, metavar="")

    args = parser.parse_args()

    if args.root:
        alert(args.root_path, mode='info')
    else:
        if args.mode:
            parse_mode(args)
        else:
            parser.print_help()


if __name__ == "__main__":
    __main()
