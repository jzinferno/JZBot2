from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import random, string

async def EditBtns(cq, **args):
    try:
        await cq.message.edit_text(**args)
    except:
        pass

genpasswd_router = Router()

def genpasswd(length=8, types=[True, False, False, False]) -> str:
    password_characters = ''
    if types[0]:
        password_characters += string.ascii_lowercase
    if types[1]:
        password_characters += string.ascii_uppercase
    if types[2]:
        password_characters += string.digits
    if types[3]:
        password_characters += string.punctuation
    return ''.join(random.choice(password_characters) for i in range(length))

def genPasswdBtns(values=['<abc>', 'ABC', '123', '!@#', '8']):
    return InlineKeyboardMarkup(inline_keyboard = [[
        InlineKeyboardButton(text=values[0], callback_data='gp_0'),
        InlineKeyboardButton(text=values[1], callback_data='gp_1')
    ],
    [
        InlineKeyboardButton(text=values[2], callback_data='gp_2'),
        InlineKeyboardButton(text=values[3], callback_data='gp_3')
    ],
    [
        InlineKeyboardButton(text='-', callback_data='gp_m'),
        InlineKeyboardButton(text=values[4], callback_data='gp_empty'),
        InlineKeyboardButton(text='+', callback_data='gp_p')
    ],
    [
        InlineKeyboardButton(text='Generate', callback_data='gp_gen')
    ]])

@genpasswd_router.message(Command('genpasswd'))
async def command_genpasswd(message: Message) -> None:
    await message.reply(text="Generated: " + genpasswd(), reply_markup=genPasswdBtns())

@genpasswd_router.callback_query(lambda c: c.data in ['gp_0', 'gp_1', 'gp_2', 'gp_3', 'gp_p', 'gp_m', 'gp_gen'])
async def genpasswd_callback_query(cq: CallbackQuery):
    button_texts = []
    types_active = []
    message_text = cq.message.text
    for row in cq.message.reply_markup.inline_keyboard:
        for button in row:
            if len(button_texts) < 4:
                button_texts.append(button.text)
                if button.text.startswith('<') and button.text.endswith('>'):
                    types_active.append(True)
                else:
                    types_active.append(False)
            else:
                if button.text not in ['-', '+', 'Generate']:
                    button_texts.append(button.text)
                    break

    if cq.data == 'gp_0':
        if types_active[0] is True:
            types_active[0] = False
            button_texts[0] = 'abc'
        else:
            types_active[0] = True
            button_texts[0] = '<abc>'
    elif cq.data == 'gp_1':
        if types_active[1] is True:
            types_active[1] = False
            button_texts[1] = 'ABC'
        else:
            types_active[1] = True
            button_texts[1] = '<ABC>'
    elif cq.data == 'gp_2':
        if types_active[2] is True:
            types_active[2] = False
            button_texts[2] = '123'
        else:
            types_active[2] = True
            button_texts[2] = '<123>'
    elif cq.data == 'gp_3':
        if types_active[3] is True:
            types_active[3] = False
            button_texts[3] = '!@#'
        else:
            types_active[3] = True
            button_texts[3] = '<!@#>'
    elif cq.data == 'gp_m':
        new = int(button_texts[4]) - 1
        if new >= 2:
            button_texts[4] = str(new)
    elif cq.data == 'gp_p':
        new = int(button_texts[4]) + 1
        if new <= 50:
            button_texts[4] = str(new)
    else:
        if True in types_active:
            message_text = "Generated: " + genpasswd(length=int(button_texts[4]), types=types_active)
    await EditBtns(cq, text=message_text, reply_markup=genPasswdBtns(button_texts))
