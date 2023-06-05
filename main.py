from argparse import ArgumentParser, BooleanOptionalAction
from source.modes._mode_parser import parse_mode

from source.tools import alert, clean_path
from os.path import realpath, dirname
import sys


def main():
    parser = ArgumentParser(prog="sq")
    parser.add_argument('-v', '--version',
                        action='version', version='Squba 0.5')
    parser.add_argument('-r', '--root', action='store_true', default=False,
                        help='Get the root directory where Squba is installed')

    subparsers = parser.add_subparsers(dest="mode")

    #! Dive args
    dive_parser = subparsers.add_parser(
        "dive", help="Explore a directory (WIP)")
    dive_parser.add_argument(
        "path", type=str, help="The path to the directory you want to explore"
    )
    dive_parser.add_argument(
        "-d",
        "--depth",
        type=int,
        default=0,
        help="The depth of the diving process",
        metavar="",
    )
    dive_parser.add_argument(
        "-s",
        "--search",
        nargs="+",
        default=[],
        help="A list of terms to look for",
        metavar="",
    )
    dive_parser.add_argument(
        "-e",
        "--exclude",
        nargs="+",
        default=[],
        help="A list of terms to ignore",
        metavar="",
    )

    #! Deploy args
    deploy_parser = subparsers.add_parser(
        "deploy", help="Create a file/folder")
    deploy_parser.add_argument(
        "filename", type=str, help="The name of the new file/folder"
    )
    deploy_parser.add_argument(
        "-d", "--dest", type=clean_path, help="The destination path", required=True
    )
    deploy_parser.add_argument(
        "-o",
        "--origin",
        type=clean_path,
        help="The path to the original file/folder (use in case you want to copy something)",
    )
    deploy_parser.add_argument(
        "-f", "--force", action="store_true", help="Force the file overwriting"
    )
    deploy_parser.add_argument(
        "-dir",
        "--is-dir",
        action="store_true",
        help="Whether a directory should be created",
    )

    #! Purge args
    purge_parser = subparsers.add_parser(
        "purge", help="Bulk file/folder deletion")
    purge_parser.add_argument(
        '--path', '-p',
        type=str,
        help="The path where to look for files with the provided terms/extensions",
        default='.'
    )
    purge_filters = purge_parser.add_mutually_exclusive_group(required=True)
    purge_filters.add_argument(
        "--terms", "-t", action="append", help="A list of terms to look for", default=[]
    )
    purge_filters.add_argument(
        "--extensions",
        "-e",
        nargs="+",
        help="A list of extensions to look for",
        default=[],
    )
    purge_filters.add_argument(
        '--all', '-a', action="store_true", help='Delete all files'
    )
    purge_parser.add_argument(
        "--ignore-terms",
        "-it",
        nargs="+",
        help="A list of terms to ignore",
        default=[],
    )
    purge_parser.add_argument(
        "--ignore-files",
        "-if",
        nargs="+",
        help="A list of files to ignore",
        default=[],
    )

    #! Populate args
    populate_parser = subparsers.add_parser(
        "populate", help="Bulk file/folder creation"
    )
    populate_parser.add_argument(
        '--dest', '-d', type=str, help="Where to write the files", default='.'
    )
    populate_parser.add_argument(
        "--files",
        "-f",
        nargs="+",
        required=True,
        help="A list of files to create. Use file.txt*[number] to create multiple copies of the same file",
    )

    #! Sonar args
    sonar_parser = subparsers.add_parser(
        "sonar", help="Monitor your system resources in real time"
    )
    sonar_parser.add_argument(
        '--network', action=BooleanOptionalAction, default=True)
    sonar_parser.add_argument(
        '--resources', action=BooleanOptionalAction, default=True)
    sonar_parser.add_argument(
        '--disks', action=BooleanOptionalAction, default=True)

    args = parser.parse_args()

    if args.root:
        for value in sys.path:
            if 'Squba' in value:
                alert(value, mode='info')
                break
    else:
        if args.mode:
            if args.mode not in ['populate', 'deploy', 'sonar']:
                args.path = realpath('.') if args.path == '.' else args.path

            parse_mode(args)
        else:
            parser.print_help()


if __name__ == "__main__":
    main()
