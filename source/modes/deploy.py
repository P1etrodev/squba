def deploy(args):
    from os import mkdir
    from os.path import exists
    from source.tools import clean_path, alert, AlertModes
    import shutil

    file_split: list[str] = args.filename.split(".")
    extension = file_split.pop()
    new_filename = "".join(file_split) + ("_copy." if args.origin else ".") + extension
    dest = clean_path(args.dest, new_filename)

    if args.is_dir:
        if args.origin:
            shutil.copytree(args.origin, dest)
        else:
            mkdir(dest)
    else:
        if args.origin:
            try:
                if exists(dest):
                    if args.force:
                        shutil.copy(args.origin, dest)
                        alert("Copied (overwritten).", mode=AlertModes.SUCCESS)
                    else:
                        alert(
                            "The file already exists. Please use --force to deploy anyways (will overwrite).",
                            mode=AlertModes.WARNING,
                        )
                else:
                    shutil.copy(args.origin, dest)
                    alert("Copied.", mode=AlertModes.SUCCESS)
            except FileNotFoundError:
                alert("Origin file does not exist.", mode=AlertModes.ERROR)
        else:
            if not exists(dest):
                with open(dest, "w"):
                    pass
                alert(f'"{dest}" created successfully.', mode=AlertModes.SUCCESS)
            else:
                if args.force:
                    with open(dest, "w"):
                        pass
                    alert(f'"{dest}" created successfully.', mode=AlertModes.SUCCESS)
                else:
                    alert(
                        "The file already exists. Please use --force to deploy anyways (will overwrite).",
                        mode=AlertModes.WARNING,
                    )
