from os import mkdir


def populate(args):
    from source.tools import clean_path, alert, AlertModes

    creation_count = 0

    for f in args.files:
        if "*" in f:
            filedata: list[str] = f.split("*")
            filename: str = filedata[0]
            count = int(filedata[-1])

            for x in range(count):
                full_path = clean_path(
                    args.dest,
                    (filename.replace(".", f"_{x+1}."))
                    if "." in filename
                    else filename + f"_{x+1}",
                )
                if filename.startswith("%"):
                    full_path = full_path.replace("%", "")
                    mkdir(full_path)
                else:
                    with open(full_path, "w"):
                        pass
                creation_count += 1
        else:
            full_path = clean_path(args.dest, f)
            if filename.startswith("%"):
                full_path = full_path.replace("%", "")
                mkdir(full_path)
            else:
                with open(full_path, "w"):
                    pass
            creation_count += 1

    alert(f"{creation_count} files created.", mode=AlertModes.SUCCESS)
