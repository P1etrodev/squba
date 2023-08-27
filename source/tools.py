import sys
from html import unescape
from json import load
from pathlib import Path
from typing import Literal, TypeAlias

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.tree import Tree


frozen: bool = hasattr(sys, 'frozen')
location = Path(sys.executable).parent if frozen else Path(__file__).parent.parent

Modes: TypeAlias = Literal["error", "info", "success", "squba"]


class Symbols:
	up_arrow = unescape('&uarr;')
	down_arrow = unescape('&darr;')
	total_symbol = unescape('&harr;')
	block = unescape('&block;')


# noinspection PyPep8Naming
def Message(msg: str, mode: Modes):
	console = Console()
	
	colors = {
		'error': 'red1',
		'info': 'blue',
		'squba': 'cyan',
		'success': 'green3'
	}
	
	color = colors.get(mode)
	title = Text(mode.capitalize(), style = color)
	text = Text(msg, style = color)
	panel = Panel(text, border_style = color, title = title, title_align = 'left')
	
	console.line()
	console.print(panel)
	console.line()


def to_gb(_bytes):
	return _bytes * 10 ** -9


def iconize(path: Path, terms_pattern, extensions_pattern) -> str:
	with location.joinpath('config.json').open(mode = 'rb') as conf:
		config = load(conf)
		icons = config.get("icons")
		default_icons = config.get("default_icons")
	
	if path.is_dir():
		iconized_file = Text(f'{default_icons.get("folder")} {path.name}')
		if extensions_pattern:
			iconized_file.highlight_regex(re_highlight = extensions_pattern, style = 'green3 bold')
		if extensions_pattern:
			iconized_file.highlight_regex(extensions_pattern, 'purple bold')
		return iconized_file
	
	for icon, ext in icons.items():
		if isinstance(ext, str) and path.suffix[1:] == ext:
			iconized_file = Text(f'{icon} {path.name}')
			if extensions_pattern:
				iconized_file.highlight_regex(re_highlight = extensions_pattern, style = 'green3 bold')
			if terms_pattern:
				iconized_file.highlight_regex(re_highlight = terms_pattern, style = 'purple bold')
			return iconized_file
		elif path.suffix[1:] in ext:
			iconized_file = Text(f'{icon} {path.name}')
			if extensions_pattern:
				iconized_file.highlight_regex(re_highlight = extensions_pattern, style = 'green3 bold')
			if terms_pattern:
				iconized_file.highlight_regex(re_highlight = terms_pattern, style = 'purple bold')
			return iconized_file
	
	iconized_file = Text(f'{default_icons.get("unknown_file")} {path.name}')
	if extensions_pattern:
		iconized_file.highlight_regex(re_highlight = extensions_pattern, style = 'green3 bold')
	return iconized_file


def generate_tree(
		path: Path, tree = None, level: int = 0, max_depth: int = 3, terms_pattern = None, extensions_pattern = None
):
	if not tree:
		tree = Tree(
			iconize(
				path, extensions_pattern = extensions_pattern,
				terms_pattern = terms_pattern
			)
		)
	
	if level > max_depth:
		return tree
	
	with location.joinpath('.sqignore').open('r') as sqignore:
		ignored = [i.replace('\n', '') for i in sqignore.readlines()]
		
		for leaf in path.glob('*'):
			if leaf.name in ignored:
				continue
			if leaf.is_dir():
				tree.add(
					generate_tree(
						path = leaf, level = level + 1, max_depth = max_depth, extensions_pattern = extensions_pattern,
						terms_pattern = terms_pattern
					)
				)
			else:
				tree.add(
					iconize(
						leaf, extensions_pattern = extensions_pattern,
						terms_pattern = terms_pattern
					)
				)
	
	return tree
