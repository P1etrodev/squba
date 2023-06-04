import json
import os
from source.tools import Preview


def dive(args):
    from source.tools import AlertModes, alert

    alert('This mode is a work in progress, will be released soon.',
          mode=AlertModes.INFO)

    # for root, dirs, files in os.walk(args.directory):
    #     preview = Preview(root)
    #     print(preview)
    #     for d in dirs:
    #         preview = Preview(root, d)
    #         print(preview)
    #     for f in files:
    #         preview = Preview(root, f)
    #         print(preview)
