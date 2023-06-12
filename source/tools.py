import importlib
from os import listdir
from os.path import join, isdir
import re
from colorama import Fore
from collections import deque


class LazyImport:
    def __init__(self, module_name: str):
        self.module_name = module_name
        self._module: any | None = None  # type: ignore

    def __getattr__(self, attr: str):
        if self._module is None:
            self._module = importlib.import_module(self.module_name)
        return getattr(self._module, attr)


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
        "info": Fore.CYAN,
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
    def __init__(self, fichier: str, root='', level=0, term_pattern=None, ext_pattern=None):
        from pathlib import Path
        from os.path import join

        absolute = join(root, fichier)
        path_obj = Path(absolute)

        self.name = path_obj.name.replace(path_obj.suffix, '')
        self.ext = path_obj.suffix.replace('.', '')
        self.full_name = path_obj.name
        self.level = level
        self.term_match = re.match(term_pattern, self.full_name,
                                   re.IGNORECASE) if term_pattern else None
        self.ext_match = re.match(ext_pattern, self.full_name,
                                  re.IGNORECASE) if ext_pattern else None
        self.absolute = clean_path(absolute)
        self.is_dir = path_obj.is_dir()
        self.icon = self.get_icon()
        self.indent = self.get_indent()

    def get_icon(self) -> str:
        from json import load
        from os.path import splitext

        if splitext(__file__)[1] == 'py':
            config_file = 'source/config.json'
        else:
            config_file = 'C:/Users/Pietro/AppData/Local/Programs/Squba/lib/source/config.json'

        with open(config_file, "r", encoding="utf-8") as conf:
            config = load(conf)
            icons = config.get("icons")
            default_icons = config.get("default_icons")

        if self.is_dir:
            return default_icons.get("folder")

        for icon, extensions in icons.items():
            if self.ext in extensions:
                return icon

        return default_icons.get("unknown_file")

    def get_indent(self) -> str:
        return "  " * self.level

    def __str__(self):
        term_match_prefix = Fore.LIGHTGREEN_EX if self.term_match else ''
        ext_match_prefix = Fore.MAGENTA if self.ext_match else ''
        return f'{self.indent}{self.icon} ' + term_match_prefix + self.name + ('/' if self.is_dir else '') + Fore.RESET + ('.' if not self.is_dir and re.match(r'^.*\..*$', self.full_name) else '') + ext_match_prefix + self.ext + Fore.RESET


def get_content(args, level=0, max_level=3, term_pattern=None, ext_pattern=None):
    q = deque()
    if level == 0:
        q.append(Preview(args.path))
    if level > max_level:
        return q
    if level != max_level:
        list_dir = listdir(args.path)
        list_dir.sort()
        ignore_file = args.root_path.joinpath('.sqignore')
        with open(ignore_file, 'r') as f:
            for fichier in list_dir:
                if fichier.startswith('.') or fichier in f.read().split('\n'):
                    continue
                absolute = join(args.path, fichier)
                q.append(Preview(absolute, level=level + 1,
                                 term_pattern=term_pattern, ext_pattern=ext_pattern))
                if isdir(absolute):
                    q.append(get_content(absolute, level + 1, max_level=max_level,
                                         term_pattern=term_pattern, ext_pattern=ext_pattern))
    return q


def show_content(q: deque):
    while len(q) > 0:
        e = q.popleft()
        if isinstance(e, deque):
            show_content(e)
        else:
            print(e)
