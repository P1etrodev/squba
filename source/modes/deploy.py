from shutil import rmtree
from source.queries import DeployQuery
from typing import Union


def deploy(args: Union[any,  DeployQuery]):  # type: ignore
    from os import mkdir
    from os.path import exists
    from source.tools import clean_path, alert, AlertModes
    import shutil

    if not args.is_dir:
        file_split: list[str] = args.filename.split(".")
        extension = file_split.pop()
        new_filename = "".join(file_split) + \
            ("_copy." if args.origin else ".") + extension
    else:
        new_filename = args.filename
    dest = clean_path(args.dest, new_filename)

    if args.is_dir:
        if args.origin:
            if exists(dest) and args.force:  # type: ignore
                shutil.rmtree(dest)
            shutil.copytree(args.origin, dest)
            if not repr(args) == 'SqubaQuery':
                alert('File copied successfully.', mode=AlertModes.SUCCESS)
        else:
            if exists(dest) and args.force:
                shutil.rmtree(dest)
            mkdir(dest)
            if not repr(args) == 'SqubaQuery':
                alert('Directory copied successfully.', mode=AlertModes.SUCCESS)
    else:
        if args.origin:
            try:
                if exists(dest):
                    if args.force:
                        shutil.copy(args.origin, dest)
                        if not repr(args) == 'SqubaQuery':
                            alert("Copied (overwritten).",
                                  mode=AlertModes.SUCCESS)
                    else:
                        if not repr(args) == 'SqubaQuery':
                            alert(
                                "The file already exists. Please use --force to deploy anyways (will overwrite).",
                                mode=AlertModes.WARNING,
                            )
                else:
                    shutil.copy(args.origin, dest)
                    if not repr(args) == 'SqubaQuery':
                        alert("Copied.", mode=AlertModes.SUCCESS)
            except FileNotFoundError:
                if not repr(args) == 'SqubaQuery':
                    alert("Origin file does not exist.", mode=AlertModes.ERROR)
        else:
            if not exists(dest):
                with open(dest, "w"):
                    pass
                if not repr(args) == 'SqubaQuery':
                    alert(f'"{dest}" created successfully.',
                          mode=AlertModes.SUCCESS)
            else:
                if args.force:
                    with open(dest, "w"):
                        pass
                    if not repr(args) == 'SqubaQuery':
                        alert(f'"{dest}" created successfully.',
                              mode=AlertModes.SUCCESS)
                else:
                    if not repr(args) == 'SqubaQuery':
                        alert(
                            "The file already exists. Please use --force to deploy anyways (will overwrite).",
                            mode=AlertModes.WARNING,
                        )
