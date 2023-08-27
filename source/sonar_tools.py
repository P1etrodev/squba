from psutil import cpu_percent, disk_partitions, disk_usage, virtual_memory
from rich import box
from rich.table import Table
from rich.text import Text

from source.tools import Symbols, to_gb

global last_received, last_sent, last_total
# noinspection PyRedeclaration
last_received = last_sent = last_total = 0


# noinspection PyUnusedLocal
def get_scan():
	BARS = 50
	
	# RESOURCES
	RESOURCES_TABLE = Table('Resource', 'Status', 'Usage', 'Usage %', box = box.SIMPLE)
	
	style = 'gold1 b'
	cpu_usage = cpu_percent()
	percent = (cpu_usage / 100.0)
	cpu_bar = Symbols.block * int(percent * BARS) + '-' * (BARS - int(percent * BARS))
	cpu_status = f'|{cpu_bar}|'
	
	RESOURCES_TABLE.add_row(Text('CPU', style), Text(cpu_status, style), '', Text(f'{cpu_usage:.2f}%', style))
	
	# MEMORY
	style = 'red3 b'
	memory = virtual_memory()
	mem_percent = (memory.percent / 100.0)
	mem_bar = Symbols.block * int(mem_percent * BARS) + '-' * (BARS - int(mem_percent * BARS))
	mem_display = f'|{mem_bar}|'
	mem_usage = f'{to_gb(memory.used):.1f} GB / {to_gb(memory.total):.1f} GB'
	
	RESOURCES_TABLE.add_row(
		Text('MEM', style), Text(mem_display, style), Text(mem_usage, style), Text(f'{memory.percent:.2f}%', style)
	)
	
	# DISKS
	for i, disk in enumerate(disk_partitions()):
		style = f'deep_sky_blue{i + 1} b'
		device = disk.device
		device_data = disk_usage(device)
		usage = device_data.percent
		disk_percent = (usage / 100.0)
		disk_letter = device.replace(':\\', ':')
		disk_name = f'DISK {disk_letter}'
		disk_bar = Symbols.block * int(disk_percent * BARS) + '-' * (BARS - int(disk_percent * BARS))
		disk_status = f'|{disk_bar}|'
		
		RESOURCES_TABLE.add_row(Text(disk_name, style), Text(disk_status, style), '', Text(f'{usage}%', style))
	
	return RESOURCES_TABLE
