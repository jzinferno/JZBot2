from aiogram import Dispatcher

from .SysInfo import sysinfo_router
from .GenPasswd import genpasswd_router
from .TicTacToe import tictactoe_router

dp = Dispatcher()

dp.include_routers(
    sysinfo_router,
    genpasswd_router,
    tictactoe_router
)
