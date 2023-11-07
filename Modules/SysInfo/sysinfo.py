from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from .utils import SysInfo as SIU
import platform

sysinfo_router = Router()

async def EditBtns(cq, **args):
    try:
        await cq.message.edit_text(**args)
    except:
        pass

sysInfoAllButtons = InlineKeyboardMarkup(
    inline_keyboard = [[
        InlineKeyboardButton(text='Arch', callback_data='arch'),
        InlineKeyboardButton(text='OS', callback_data='os')
    ],
    [
        InlineKeyboardButton(text='User', callback_data='user'),
        InlineKeyboardButton(text='Hostname', callback_data='hostname')
    ],
    [
        InlineKeyboardButton(text='IP', callback_data='ip'),
        InlineKeyboardButton(text='Uptime', callback_data='uptime')
    ],
    [
        InlineKeyboardButton(text='CPU', callback_data='cpu'),
        InlineKeyboardButton(text='GPU', callback_data='gpu')
    ],
    [
        InlineKeyboardButton(text='RAM', callback_data='ram'),
        InlineKeyboardButton(text='Swap', callback_data='swap')        
    ]]
)
if platform.system() == 'Linux':
    sysInfoAllButtons.inline_keyboard.insert(1, [
        InlineKeyboardButton(text='Kernel', callback_data='kernel'),
        InlineKeyboardButton(text='Uname', callback_data='uname')])
    sysInfoAllButtons.inline_keyboard.append([
        InlineKeyboardButton(text='Neofetch', callback_data='neofetch')])

sysInfoBackButton = InlineKeyboardMarkup(
    inline_keyboard = [[
        InlineKeyboardButton(text='Back', callback_data='back')
    ]]
)

@sysinfo_router.message(Command('sysinfo'))
async def command_sysinfo(message: Message) -> None:
    await message.reply(text='Select system information:', reply_markup=sysInfoAllButtons)

@sysinfo_router.callback_query(lambda c: c.data in ['arch', 'os', 'kernel', 'uname', 'user', 'hostname', 'ip', 'uptime', 'cpu', 'gpu', 'ram', 'swap', 'neofetch', 'back'])
async def sysinfo_callback_query(cq: CallbackQuery):
    if cq.data == 'arch':
        await EditBtns(cq, reply_markup=sysInfoBackButton, text=SIU().sysinfo_arch())
    elif cq.data == 'os':
        await EditBtns(cq, reply_markup=sysInfoBackButton, text=await SIU().sysinfo_os())
    elif cq.data == 'kernel' and platform.system() == 'Linux':
        await EditBtns(cq, reply_markup=sysInfoBackButton, text=SIU().sysinfo_kernel())
    elif cq.data == 'uname' and platform.system() == 'Linux':
        await EditBtns(cq, reply_markup=sysInfoBackButton, text=await SIU().sysinfo_uname())
    elif cq.data == 'user':
        await EditBtns(cq, reply_markup=sysInfoBackButton, text=SIU().sysinfo_user())
    elif cq.data == 'hostname':
        await EditBtns(cq, reply_markup=sysInfoBackButton, text=SIU().sysinfo_hostname())
    elif cq.data == 'ip':
        await EditBtns(cq, reply_markup=sysInfoBackButton, text=SIU().sysinfo_ip())
    elif cq.data == 'uptime':
        await EditBtns(cq, reply_markup=sysInfoBackButton, text=SIU().sysinfo_uptime())
    elif cq.data == 'cpu':
        await EditBtns(cq, reply_markup=sysInfoBackButton, text=await SIU().sysinfo_cpu())
    elif cq.data == 'gpu':
        await EditBtns(cq, reply_markup=sysInfoBackButton, text=await SIU().sysinfo_gpu())
    elif cq.data == 'ram':
        await EditBtns(cq, reply_markup=sysInfoBackButton, text=SIU().sysinfo_ram())
    elif cq.data == 'swap':
        await EditBtns(cq, reply_markup=sysInfoBackButton, text=SIU().sysinfo_swap())
    elif cq.data == 'neofetch' and platform.system() == 'Linux':
        await EditBtns(cq, reply_markup=sysInfoBackButton, text=await SIU().sysinfo_neofetch())
    else:
        await EditBtns(cq, reply_markup=sysInfoAllButtons, text='Select system information:')
