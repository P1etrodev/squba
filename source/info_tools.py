from dataclasses import dataclass

from cpuinfo import get_cpu_info
from psutil import cpu_count, cpu_freq, net_if_addrs, virtual_memory
from requests import get
from rich.panel import Panel
from wmi import WMI

from source.tools import to_gb

computer = WMI()


def get_os_name():
	try:
		return computer.Win32_OperatingSystem()[0].Name.encode('utf-8').split(b'|')[0].decode()
	except Exception:
		return 'Not identified'


def get_os_version():
	try:
		os_info = computer.Win32_OperatingSystem()[0]
		return ' '.join([os_info.Version, os_info.BuildNumber])
	except Exception:
		return 'Not identified'


def get_gpus_data():
	try:
		return '\n'.join(
			[f'[red{i if i > 0 else ""} bold]GPU {i}: {gpu_info.Name.upper()}[/red{i if i > 0 else ""} bold]' for i, gpu_info
				in
				enumerate(computer.Win32_VideoController())]
		)
	except Exception:
		return 'Not identified'


def get_public_ip():
	try:
		ip = get('https://api.ipify.org').content.decode('utf8')
		return ip
	except Exception:
		return 'Undefined'


def get_cpu_name():
	try:
		return get_cpu_info().get('brand_raw')
	except Exception:
		return 'Not identified'


def get_memory():
	svem = virtual_memory()
	memory = to_gb(svem.total)
	return f'{memory:.2f} GB'


def get_cpu_freq():
	return f'{cpu_freq().max:.1f}Mhz'


def get_private_ip():
	ip = net_if_addrs()
	private_ip = ''
	for interface_name, interface_addresses in ip.items():
		if interface_name == 'Ethernet':
			private_ip = list(
				filter(lambda x: all(symbol not in x.address for symbol in [':', '-']), interface_addresses)
			).pop().address
			break
	return private_ip


SystemData = Panel(
	f'''
[green3 bold]{get_os_name()}[/green3 bold]
[light_blue bold]{get_os_version()}[/light_blue bold]
			''', title = 'SYSTEM', border_style = 'orange_red1', expand = True,  # box = box.SIMPLE_HEAD
)


@dataclass
class CPU:
	model: str = get_cpu_name()
	threads: int = cpu_count(logical = True)
	cores: int = cpu_count(logical = False)
	freq: str = get_cpu_freq()


HardwareData = Panel(
	f'''
[gold1 bold]CPU MODEL: {CPU.model}[/gold1 bold]
[purple bold]CPU CORES: {CPU.cores}[/purple bold]
[cyan bold]CPU THREADS: {CPU.threads}[/cyan bold]
[white bold]CPU FREQ: {CPU.freq}[/white bold]

{get_gpus_data()}

[blue bold]MEMORY: {get_memory()}[/blue bold]
''', title = 'HARDWARE', border_style = 'green3', expand = True
)

NetworkData = Panel(
	f'''
[red3 bold]PRIVATE: {get_private_ip()}[/red3 bold]
[green3 bold]PUBLIC: {get_public_ip()}[/green3 bold]
			''', title = 'NETWORK', border_style = 'blue_violet', expand = True
)

pc_info = SystemData, HardwareData, NetworkData
