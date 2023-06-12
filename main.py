from os.path import dirname
from os import getcwd
import sys
from source.modes._mode_parser import parse_mode

from source.tools import alert, clean_path
from source.tools import LazyImport

argparse = LazyImport('argparse')


def __main():
    parser = argparse.ArgumentParser(prog="sq")
    parser.add_argument('-v', '--version',
                        action='version', version='Squba 1.0')
    parser.add_argument('-r', '--root', action='store_true', default=False,
                        help='Get the root directory where Squba is installed')

    subparsers = parser.add_subparsers(dest="mode")

    #! Dive args
    dive_parser = subparsers.add_parser(
        "dive", help="Explore a directory")
    dive_parser.add_argument(
        '-p', "--path", type=clean_path, help="The path to the directory you want to explore", default=getcwd()
    )
    dive_parser.add_argument(
        "-d",
        "--max-depth",
        type=int,
        default=3,
        help="The max depth of the diving process. Defaults to 3",
        metavar="",
    )
    filters_group = dive_parser.add_argument_group('filters')
    filters_group.add_argument(
        "-t",
        "--terms",
        nargs='+',
        default=[],
        help="A list of terms to highlight",
        metavar="",
    )
    filters_group.add_argument(
        "-x",
        "--extensions",
        nargs='+',
        default=[],
        help="A list of extensions to highlight",
        metavar="",
    )

    #! Deploy args
    deploy_parser = subparsers.add_parser(
        "deploy", help="Create a file/folder")
    deploy_parser.add_argument(
        "filename", type=str, help="The name of the new file/folder",
        metavar="",
    )
    deploy_parser.add_argument(
        "-d", "--dest", type=clean_path, help="The destination path", required=True,
        metavar="",
    )
    deploy_parser.add_argument(
        "-o",
        "--origin",
        type=clean_path,
        help="The path to the original file/folder (use in case you want to copy something)",
        metavar="",
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
        default=getcwd(),
        metavar="",
    )
    purge_filters = purge_parser.add_mutually_exclusive_group(required=True)
    purge_filters.add_argument(
        "--terms", "-t", action="append", help="A list of terms to look for", default=[],
        metavar="",
    )
    purge_filters.add_argument(
        "--extensions",
        "-e",
        nargs='+',
        help="A list of extensions to look for",
        default=[],
        metavar="",
    )
    purge_filters.add_argument(
        '--all', '-a', action="store_true", help='Delete all files',
    )
    purge_parser.add_argument(
        "--ignore-terms",
        "-it",
        nargs='+',
        help="A list of terms to ignore",
        default=[],
        metavar="",
    )
    purge_parser.add_argument(
        "--ignore-files",
        "-if",
        nargs='+',
        help="A list of files to ignore",
        default=[],
        metavar="",
    )

    #! Populate args
    populate_parser = subparsers.add_parser(
        "populate", help="Bulk file/folder creation"
    )
    populate_parser.add_argument(
        '--dest', '-d', type=str, help="Where to write the files", default=getcwd(),
        metavar="",
    )
    populate_parser.add_argument(
        "--files",
        "-f",
        nargs='+',
        required=True,
        help="A list of files to create. Use file.txt*[number] to create multiple copies of the same file",
        metavar="",
    )

    #! Sonar args
    sonar_parser = subparsers.add_parser(
        "sonar", help="Monitor your system resources in real time"
    )
    sonar_parser.add_argument(
        '--network', action=argparse.BooleanOptionalAction, default=True, metavar="")
    sonar_parser.add_argument(
        '--resources', action=argparse.BooleanOptionalAction, default=True, metavar="")
    sonar_parser.add_argument(
        '--disks', action=argparse.BooleanOptionalAction, default=True, metavar="")

    args = parser.parse_args()

    root_path = dirname(sys.executable) if getattr(
        sys, 'frozen', False) else dirname(__file__)

    if args.root:
        alert(root_path, mode='info')
    else:
        from pathlib import Path
        args.root_path = Path(root_path)
        if args.mode:
            parse_mode(args)
        else:
            parser.print_help()


if __name__ == "__main__":
    __main()
