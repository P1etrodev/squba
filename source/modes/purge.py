def purge(args):
    from source.tools import clean_path, AlertModes, alert
    from os.path import exists, isdir
    from os import remove, listdir
    from shutil import rmtree

    count = 0

    for f in listdir(args.path):
        file_path = clean_path(args.path, f)
        if args.all:
            try:
                rmtree(file_path)
            except:
                remove(file_path)
            count += 1
            continue
        else:
            if not f in args.ignore_files and not any(
                [term in f for term in args.ignore_terms]
            ):
                if any([term in f for term in args.terms]) or any(
                    [f.endswith(ext) for ext in args.extensions]
                ):
                    try:
                        rmtree(file_path)
                    except:
                        remove(file_path)
                    count += 1
    alert(f"{count} files removed.", mode=AlertModes.SUCCESS)
