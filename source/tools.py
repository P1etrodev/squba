from colorama import Fore


def to_gb(bytes):
    return bytes * 10 ** -9


def display_content(content, color, start='', end='\n'):
    print(start + color + content + Fore.RESET, end=end)


def clean_path(*args, **kwargs) -> str:
    from os.path import join

    return join(*args).replace("\\", "/").replace("//", "/")


class AlertModes:
    DEFAULT = "default"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"


def alert(message, mode="default", sep=False) -> None:
    modes = {
        "default": Fore.RESET,
        "info": Fore.BLUE,
        "warning": Fore.YELLOW,
        "error": Fore.RED,
        "success": Fore.GREEN,
    }
    separator = "-" * len(message)
    if sep:
        print(modes[mode] + separator + Fore.RESET)
    print(modes[mode] + mode.upper() + ": " + message + Fore.RESET)
    if sep:
        print(modes[mode] + separator + Fore.RESET)


class Preview:
    def __init__(self, root, name=""):
        from pathlib import Path
        from os.path import join

        self.name = name
        self.root = root
        self.absolute = join(self.root, self.name).replace("\\", "/")
        self.path_data = Path(join(root, name))
        self.icon = self.get_icon()
        if not self.path_data.is_dir():
            self.ext = self.name.split(".").pop()
        if self.name == "":
            self.identation = ""
        else:
            self.identation = self.get_identation()
        self.show = self.identation + f"{self.icon} {self.name}"

    def get_icon(self) -> str:
        from json import load

        with open("source/config.json", "r", encoding="utf-8") as conf:
            config = load(conf)
            icons = config.get("icons")
            default_icons = config.get("default_icons")

        if self.path_data.is_dir():
            return default_icons.get("folder")

        for icon, extensions in icons.items():
            if self.ext in extensions:
                return icon

        return default_icons.get("unknown_file")

    def get_identation(self) -> str:
        return "  " * (self.absolute.count("/") % 2)

    def __str__(self):
        return self.show
