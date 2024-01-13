import asyncio

class Shell():
    def __init__(self, command: str) -> None:
        self.command = command

    async def create_shell(self) -> None:
        process = await asyncio.create_subprocess_shell(
            cmd=self.command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            shell=True
        )
        self._stdout, self._stderr = await process.communicate()
        self._returncode = process.returncode

    @property
    async def stdout(self) -> str:
        await self.create_shell()
        return self._stdout.decode(encoding='utf-8', errors='ignore')

    @property
    async def stderr(self) -> str:
        await self.create_shell()
        return self._stderr.decode(encoding='utf-8', errors='ignore')

    @property
    async def returncode(self) -> int:
        await self.create_shell()
        return self._returncode
