from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

async def EditBtns(cq, **args):
    try:
        await cq.message.edit_text(**args)
    except:
        pass

tictactoe_router = Router()

def ticTacToeBtns(values=['?', '?', '?', '?', '?', '?', '?', '?', '?']):
    return InlineKeyboardMarkup(inline_keyboard = [[
        InlineKeyboardButton(text=values[0], callback_data='ttt_0'),
        InlineKeyboardButton(text=values[1], callback_data='ttt_1'),
        InlineKeyboardButton(text=values[2], callback_data='ttt_2')
    ],
    [
        InlineKeyboardButton(text=values[3], callback_data='ttt_3'),
        InlineKeyboardButton(text=values[4], callback_data='ttt_4'),
        InlineKeyboardButton(text=values[5], callback_data='ttt_5')
    ],
    [
        InlineKeyboardButton(text=values[6], callback_data='ttt_6'),
        InlineKeyboardButton(text=values[7], callback_data='ttt_7'),
        InlineKeyboardButton(text=values[8], callback_data='ttt_8')
    ]])

@tictactoe_router.message(Command('tictactoe'))
async def command_tictactoe(message: Message) -> None:
    await message.reply(text='tictactoe', reply_markup=ticTacToeBtns())

@tictactoe_router.callback_query(lambda c: c.data in ['ttt_0', 'ttt_1', 'ttt_2', 'ttt_3', 'ttt_4', 'ttt_5', 'ttt_6', 'ttt_7', 'ttt_8'])
async def tictactoe_callback_query(cq: CallbackQuery):
    button_texts = []
    for row in cq.message.reply_markup.inline_keyboard:
        for button in row:
            button_texts.append(button.text)

    if button_texts.count('x') > button_texts.count('o'):
        symbol = 'o'
    else:
        symbol = 'x'

    if cq.data.startswith('ttt_') and button_texts[int(cq.data[-1])] == '?':
        button_texts[int(cq.data[-1])] = symbol

    await EditBtns(cq, text='tictactoe', reply_markup=ticTacToeBtns(button_texts))
