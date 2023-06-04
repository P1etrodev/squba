def parse_mode(args):
    from source.modes.dive import dive
    from source.modes.deploy import deploy
    from source.modes.purge import purge
    from source.modes.populate import populate
    from source.modes.sonar import sonar

    eval(args.mode)(args)
