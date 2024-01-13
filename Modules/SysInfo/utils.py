from jzbot.shell import Shell
import platform
import aiofiles
import socket
import getpass
import psutil
import uptime

class SysInfo():
    def __init__(self) -> None:
        self.windows = platform.system().lower() == 'windows'
        self.unknown = 'Unknown'

    def readable(self, num, suffix='B'):
        for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
            if abs(num) < 1024.0:
                return '%3.1f%s%s' % (num, unit, suffix)
            num /= 1024.0
        return '%.1f%s%s' % (num, 'Yi', suffix)

    async def sysinfo_cpu(self) -> str:
        if self.windows:
            return (await Shell('wmic cpu get name').stdout).split('\n')[1].strip() or self.unknown
        else:
            async with aiofiles.open('/proc/cpuinfo', mode='r') as f:
                async for line in f:
                    if line.startswith(('model name', 'Hardware', 'Processor')):
                        return line.split(':')[-1].strip()
        return self.unknown

    async def sysinfo_gpu(self) -> str:
        if self.windows:
            return (await Shell('wmic path win32_VideoController get name').stdout).split('\n')[1].strip() or self.unknown
        else:
            for line in (await Shell('lspci').stdout).split('\n'):
                if any(gpu in line for gpu in [' VGA ', ' 3D ', ' Display ', ' Non-VGA ']):
                    return line.split(':')[-1].strip()
        return self.unknown

    async def sysinfo_os(self) -> str:
        result = self.unknown
        try:
            if self.windows:
                result = (await Shell('wmic os get caption').stdout).split('\n')[1].strip() or self.unknown
            else:
                async with aiofiles.open('/etc/os-release', mode='r') as f:
                    async for line in f:
                        if line.startswith('PRETTY_NAME='):
                            result = line.split('=')[-1].replace('\"', '').strip()
        except:
            pass
        return result

    async def sysinfo_neofetch(self) -> str:
        return '\n'.join([line for line in (await Shell('neofetch --stdout').stdout).split('\n') if ':' in line]) or self.unknown

    async def sysinfo_uname(self) -> str:
        return await Shell('uname -a').stdout or self.unknown

    def sysinfo_arch(self) -> str:
        return platform.uname().machine

    def sysinfo_kernel(self) -> str:
        return platform.uname().release

    def sysinfo_user(self) -> str:
        return getpass.getuser()

    def sysinfo_hostname(self) -> str:
        return socket.gethostname()

    def sysinfo_ip(self) -> str:
        return socket.gethostbyname(socket.gethostname())

    def sysinfo_ram(self) -> str:
        ram = psutil.virtual_memory()
        return f'{self.readable(ram.used)} / {self.readable(ram.total)} ({round(ram.used / ram.total * 100, 2)}%)'

    def sysinfo_swap(self) -> str:
        swap = psutil.swap_memory()
        return f'{self.readable(swap.used)} / {self.readable(swap.total)} ({round(swap.used / swap.total * 100, 2)}%)'

    def sysinfo_uptime(self) -> str:
        hours, remainder = divmod(int(uptime.uptime()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        def includeS(text: str, num: int):
            return f"{num} {text}{'' if num == 1 else 's'}"

        d = includeS('day', days)
        h = includeS('hour', hours)
        m = includeS('minute', minutes)
        s = includeS('second', seconds)

        if days:
            output = f'{d}, {h}, {m} and {s}'
        elif hours:
            output = f'{h}, {m} and {s}'
        elif minutes:
            output = f'{m} and {s}'
        else:
            output = s

        return output
