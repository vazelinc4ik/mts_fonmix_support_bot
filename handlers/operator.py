from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from constants import (
    OPERATOR_MESSAGE,
    CONTACTS_MESSAGE,
    ON_START_BUTTONS
)
from utils import generate_kb


router = Router()

@router.message(F.text.lower() == 'перейти в чат-бота с оператором')
async def operator_chat(message: Message):
    await message.answer(
        text=OPERATOR_MESSAGE,
        reply_markup=generate_kb(
            buttons=ON_START_BUTTONS,
            adjustment=[1, 2]
        )
    )
    
@router.message(F.text.lower()== 'наши контакты')
async def contact(message: Message):
    await message.answer(
        text=CONTACTS_MESSAGE,
        reply_markup=generate_kb(
            buttons=ON_START_BUTTONS,
            adjustment=[1, 2]
        )
    )