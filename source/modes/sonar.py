from html import unescape
from os import system
from time import sleep
from colorama import Fore

import psutil

from source.tools import display_content, to_gb


def sonar(args):
    BLOCK = unescape('&block;')
    BARS = 50
    CENTER_SYMBOL = ' '
    if args.network:
        last_received = psutil.net_io_counters().bytes_recv
        last_sent = psutil.net_io_counters().bytes_sent
        last_total = last_received + last_sent
    try:
        while True:
            system('cls')
            if args.resources:
                COLOR_CODE = Fore.CYAN
                title = 'RESOURCES'.center(BARS, CENTER_SYMBOL)
                display_content(title, COLOR_CODE, start='\n', end='\n\n')

                cpu_usage = psutil.cpu_percent()
                cpu_percent = (cpu_usage / 100.0)
                cpu_bar = BLOCK * int(cpu_percent * BARS) + '-' * \
                    (BARS - int(cpu_percent * BARS))

                display_content(
                    f'CPU: |{cpu_bar}| {cpu_usage:.2f}%', COLOR_CODE, end='\n\n')

                memory = psutil.virtual_memory()
                mem_percent = (memory.percent / 100.0)
                mem_bar = BLOCK * int(mem_percent * BARS) + '-' * \
                    (BARS - int(mem_percent * BARS))

                display_content(
                    f'MEM: |{mem_bar}| {memory.percent:.2f}% ({to_gb(memory.used):.1f} GB / {to_gb(memory.total):.1f} GB)', COLOR_CODE, end='\n\n')

            if args.disks:
                COLOR_CODE = Fore.GREEN
                title = 'DISKS'.center(BARS, CENTER_SYMBOL)
                display_content(title, COLOR_CODE, start='\n', end='\n\n')

                for disk in psutil.disk_partitions():
                    device = disk.device
                    device_data = psutil.disk_usage(device)
                    disk_usage = device_data.percent
                    disk_percent = (disk_usage / 100.0)
                    disk_bar = BLOCK * int(disk_percent * BARS) + '-' * \
                        (BARS - int(disk_percent * BARS))
                    disk_name = device.replace(':\\', '')
                    display_content(
                        f'DISK {disk_name}: |{disk_bar}| {disk_usage:.2f}% ({to_gb(device_data.used):.1f} GB / {to_gb(device_data.total):.1f} GB)', COLOR_CODE, end='\n\n')

            if args.network:
                COLOR_CODE = Fore.YELLOW
                title = 'NETWORK'.center(BARS, CENTER_SYMBOL)
                display_content(title, COLOR_CODE, start='\n', end='\n\n')

                bytes_received = psutil.net_io_counters().bytes_recv
                bytes_sent = psutil.net_io_counters().bytes_sent
                bytes_total = bytes_received + bytes_sent

                new_received = (bytes_received - last_received) * 0.001
                new_sent = (bytes_sent - last_sent) * 0.001  # type: ignore
                new_total = (bytes_total - last_total) * 0.001  # type: ignore

                up_arrow = unescape('&uarr;')
                down_arrow = unescape('&darr;')
                total_symbol = unescape('&harr;')

                content = f'{down_arrow} {new_received:.1f} Kb | {up_arrow} {new_sent:.1f} Kb | {total_symbol} {new_total:.1f} Kb'.center(
                    BARS, CENTER_SYMBOL)

                display_content(
                    content, COLOR_CODE, end='\n\n')

                last_received = bytes_received
                last_sent = bytes_sent
                last_total = bytes_total

            content = 'Press CTRL+C to stop'.center(BARS, CENTER_SYMBOL)
            display_content(content, Fore.RED, start='\n\n\n\n')
            sleep(0.5)
    except KeyboardInterrupt:
        system('cls')
