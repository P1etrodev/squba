import sys
from pathlib import Path
from re import match
from time import sleep
from typing import List

from psutil import net_io_counters
from rich import box
from rich.console import Console, Group
from rich.live import Live
from rich.table import Table
from rich.traceback import install
from typer import Option, Typer
from typing_extensions import Annotated

from source.info_tools import pc_info
from source.sonar_tools import get_scan
from source.tools import Message, Symbols, generate_tree

install()

__version__ = '2.0'

global location

frozen: bool = hasattr(sys, 'frozen')
location = Path(sys.executable).parent if frozen else Path(__file__).parent

current_dir = Path.cwd()

console: Console = Console()
Squba = Typer()


@Squba.command()
def version():
	console.line()
	console.print(f'version: {__version__}', style = 'cyan bold')
	console.line()


@Squba.command()
def info():
	status = console.status('Scanning PC...', spinner_style = 'spring_green3')
	
	status.start()
	sleep(1)
	
	status.update('Scanning network...')
	sleep(1)
	
	status.update('Making it prettier...')
	
	sleep(1)
	
	status.stop()
	
	console.line()
	console.print(*pc_info)
	console.line()


@Squba.command(short_help = 'dive into de depths of a directory')
def dive(
		directory: Annotated[Path, Option('--directory', '-d')] = Path.cwd(),
		terms: Annotated[List[str], Option('--term', '-t')] = None,
		extensions: Annotated[List[str], Option('--extension', '-e')] = None,
		max_depth: Annotated[int, Option('--max-depth', '-m')] = 3
):
	terms_pattern = None
	extensions_pattern = None
	
	if terms:
		terms = '|'.join(terms)
		terms_pattern = rf'({terms})'
	if extensions:
		extensions = '|'.join(extensions)
		extensions_pattern = rf'({extensions})$'
	
	status = console.status('Generating tree...', spinner_style = 'cyan')
	
	status.start()
	
	files_tree = generate_tree(
		directory, terms_pattern = terms_pattern, extensions_pattern = extensions_pattern, max_depth = max_depth
	)
	
	status.stop()
	
	console.line()
	console.print(files_tree)
	console.line()


@Squba.command()
def populate(
		directory: Annotated[Path, Option('--directory', '-d')] = Path.cwd(),
		folders: Annotated[List[str], Option('--folder', '-fo')] = None,
		files: Annotated[List[str], Option('--file', '-fi')] = None
):
	total_folder_count = 0
	total_files_count = 0
	
	if directory.is_dir():
		if folders is not None:
			for folder_name in folders:
				
				if match(r'^\w+\*\d+$', folder_name):
					name, count = folder_name.split('*')
					count = int(count)
					total_folder_count += count
					
					for i in range(1, count + 1):
						folder = directory.joinpath(f'{name}_{i}')
						folder.mkdir(exist_ok = True)
				
				else:
					Message('All folders must have the following format -> folder_name*amount', 'error')
					quit()
		
		if files is not None:
			for file_name in files:
				
				if match(r'^\w+\.[a-zA-Z0-9]+\*\d+$', file_name):
					name, count = file_name.split('*')
					count = int(count)
					total_files_count += count
					
					for i in range(1, count + 1):
						new_file_name = name.replace('.', f'_{i}.')
						file = directory.joinpath(new_file_name)
						with file.open('w'):
							pass
				
				else:
					Message('All files must have the following format -> file_name.extension*amount', 'error')
					quit()
		
		Message(f'{total_folder_count} folders and {total_files_count} files created.', 'success')
	
	else:
		Message(f'{directory} is not a directory.', 'error')


@Squba.command()
def purge(
		directory: Annotated[Path, Option('--directory', '-d')] = Path.cwd(),
		terms: Annotated[List[str], Option('--terms', '-t')] = None,
		extensions: Annotated[List[str], Option('--extensions', '-e')] = None,
		_all: Annotated[bool, Option('--all', '-a')] = False,
):
	status = console.status(
		f'Searching by {len(terms)} terms and {len(extensions)} extensions...', spinner_style = 'red1'
	)
	total_deleted_count = 0
	terms = '|'.join(terms)
	extensions = '|'.join(extensions)
	
	status.start()
	sleep(1)
	status.update('Deleting...')
	sleep(1)
	
	for element in directory.glob('*'):
		if element.is_dir():
			if _all or (terms and match(terms, element.name)):
				try:
					element.rmdir()
					total_deleted_count += 1
				except OSError:
					Message(f"Failed to delete directory '{element}'.", 'error')
			continue
		
		if _all or (terms and match(terms, element.stem)) or (extensions and element.suffix[1:] in extensions):
			try:
				element.unlink()
				total_deleted_count += 1
			except OSError:
				Message(f"Failed to delete file '{element}'.", "error")
	
	status.stop()
	
	Message(f'{total_deleted_count} elements deleted.', 'success')


# noinspection PyGlobalUndefined
@Squba.command()
def sonar():
	with Live(get_scan(), refresh_per_second = 4) as live:
		console.clear()
		# NETWORK
		last_received = net_io_counters().bytes_recv
		last_sent = net_io_counters().bytes_sent
		last_total = last_received + last_sent
		
		try:
			while True:
				bytes_received = net_io_counters().bytes_recv
				bytes_sent = net_io_counters().bytes_sent
				bytes_total = bytes_received + bytes_sent
				
				new_received = (bytes_received - last_received) * 0.001
				new_sent = (bytes_sent - last_sent) * 0.001
				new_total = (bytes_total - last_total) * 0.001
				
				last_received = bytes_received
				last_sent = bytes_sent
				last_total = bytes_total
				
				NETWORK = Table('Received', 'Sent', 'Total', box = box.SIMPLE)
				
				down = f'[purple3]{Symbols.down_arrow} {new_received:.1f} Kb[/purple3]'
				up = f'[spring_green3]{Symbols.up_arrow} {new_sent:.1f} Kb[/spring_green3]'
				total = f'[gold1]{Symbols.total_symbol} {new_total:.1f} Kb[/gold1]'
				
				NETWORK.add_row(down, up, total)
				
				live.update(Group(get_scan(), NETWORK))
		except KeyboardInterrupt:
			pass


if __name__ == '__main__':
	Squba()
