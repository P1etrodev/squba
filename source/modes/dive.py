from source.tools import get_content, show_content


def dive(args):
    WIP = True

    if not WIP:
        from source.tools import AlertModes, alert

        alert('This mode is a work in progress, will be released soon.',
              mode=AlertModes.INFO)

    else:
        positive_terms = '|'.join(args.terms) if args.terms != [] else None
        positive_ext = '|'.join(
            args.extensions) if args.extensions != [] else None

        term_pattern = rf'^(.*)({positive_terms})(.*)\.(.*)$' if positive_terms != [
        ] else None
        ext_pattern = rf'^.*\.({positive_ext})$' if positive_ext != [] else None

        content = get_content(
            args, max_level=args.max_depth, term_pattern=term_pattern, ext_pattern=ext_pattern)

        show_content(content)
